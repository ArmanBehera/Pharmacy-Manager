<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { checkDate } from '../../helpers';
    import { format, previousSaturday } from 'date-fns';
    import { convertDateFormat } from '../../helpers';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    const patients_data = ref([]);
    const doctors_data = ref([]);
    const is_loaded = ref([false]);
    const selected_patient = ref();
    const first_name = ref('');
    const last_name = ref('');
    const gender = ref('');
    const selected_doctor = ref();
    const appointment_date = ref();

    const previous_appointment = ref(false);
    const previous_appointments_data = ref(false);
    const selected_previous_appointment = ref();

    if (store.state.is_registered === 'true') {
        axios.post('/frontdesk/getPatients/', {
            'first_name': '',
            'last_name': '',
            'gender': ''
        })
        .then( (response) => {
            patients_data.value = response.data.map(patient => ({
                ...patient,
                name: `${patient.first_name} ${patient.last_name}`
            }));
            is_loaded.value[0] = true;   
        })
        .catch( (error) => {
            warn('warn', "Error getting patients data.", error)
        })

        axios.get('/frontdesk/getDoctors/')
        .then( (response) => {
            doctors_data.value = response.data.map(doctor => ({
            ...doctor,
            label: `${doctor.name}: ${doctor.specialization}` // Combine name and specialization
        }));
        })
        .catch( (error) => {
            warn('warn', 'Error getting doctor users data.', error);
        })
    } else {
        warn('warn', 'Please log in to access this page.', '');
    }

    const search = () => {

        let data = {
            first_name: first_name.value,
            last_name: last_name.value,
            gender: gender.value
        }

        axios.post('/frontdesk/getPatients/', {
            ...data
        })
        .then( (response) => {
            patients_data.value = response.data.map(patient => ({
                ...patient,
                name: `${patient.first_name} ${patient.last_name}`
            }));
        })
        .catch( (error) => {
            warn('warn', 'Error in searching for the patient.', error)
        })
    }

    const submit = () => {
        let data = {}
        
        try {
            data = {
                'patient_id': selected_patient.value.id,
                'doctor_id': !(previous_appointment.value) ? selected_doctor.value.id : -1,
                'date': format(new Date(appointment_date.value), 'yyyy-MM-dd'),
                'status': 'Scheduled',
                'previous_appointment_id': (previous_appointment.value) ? selected_previous_appointment.value : null
            }
        } catch (error) {
            warn('warn', 'Some of the values are not filled.', 'Please fill in all the required values.');
            return;
        }

        if (!checkDate(appointment_date))  {
            warn('warn', 'Error with appointment date.', 'Make sure the date is filled and is today or after today.', '');
            return;
        }

        axios.post('/frontdesk/addExistingPatient/', {
            ...data
        })
        .then( (response) => {
            warn('success', 'Successfully made appointment.', `Token assigned to: ${response.data.token}`)

            setTimeout(() => {
                window.location.reload();
            }, 3000);
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in making appointment.', error)
        })
    }

    const getPreviousAppointments = () => {
        axios.post('/frontdesk/getPreviousAppointments/', {
            'id': selected_patient.value.id
        })
        .then( (response) => {
            previous_appointments_data.value = response.data.map(appointment => ({
                ...appointment,
                label: `${appointment.doctor_name}: ${convertDateFormat(appointment.appointment_date)}`
            }))
        })
        .catch( (error) => {
            warn('warn', 'Failure to access previous appointments of patients.', error)
        })
    }

    watch(previous_appointment, (newVal, oldVal) => {
        if (newVal === true) {
            getPreviousAppointments();
        }
    });

    watch(selected_patient, (newVal, oldVal) => {
        if (previous_appointment.value === true) {
            getPreviousAppointments();
        }
    });
</script>

<template>
    <div class="flex flex-column align-items-center justify-content-center">
        <Toast/>
        <h1 class="text-3xl font-bold m-3">Add Existing Patient</h1>
    </div>

    <div class="flex flex-row align-items-center justify-content-center">
        <InputText class="elements" id="first-name" placeholder="First Name" v-model.trim="first_name"/>
        <InputText class="elements" id="last-name" placeholder="Last Name" v-model.trim="last_name"/>
        <InputText class="elements" id="gender" placeholder="Gender" v-model.trim="gender"/>
        <Button id="search" label="Search" @click.prevent="search"/>
    </div>

    <div class="card m-10">
        <DataTable v-if="is_loaded[0] & patients_data.length > 0" :value="patients_data" datakey="id" removableSort :rows="3" paginator tableStyle="min-width: 22rem" v-model:selection="selected_patient" >
            <Column selectionMode="single" headerStyle="width: 3rem"></Column>
            <Column field="name" header="Name" style="width: 20%" sortable></Column>
            <Column field="age" header="Age" style="width: 20%" sortable></Column>
            <Column field="gender" header="Gender" style="width: 20%;" sortable></Column>
            <Column field="appointment_date" header="Last Appointment date" style="width: 20%" sortable></Column>
        </DataTable>

        <div v-else-if="patients_data.length == 0 && is_loaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
            There are no patients in this system.
        </div>

        <div class="centered" v-else>
            <ProgressSpinner/>
        </div>
    </div>

    <div class="top-container">
        <div class="container">
            <div class="sub-container flex flex-row align-items-center justify-content-center">
                <label for="previous-appointment">Is this a follow-up of previous appointment? </label>
                <Checkbox v-model="previous_appointment" id="previous-appointment" binary class="mr-4" :disabled="!selected_patient"/>
                <Select v-if="!previous_appointment" class="elements" id="doctorChoice" v-model.trim="selected_doctor" :options="doctors_data" optionLabel="label" placeholder="Doctor Assigned*" showClear/>
                <Select v-if="previous_appointment" class="elements" placeholder="Previous Appointment *" v-model.trim="selected_previous_appointment" :options="previous_appointments_data" optionValue="appointment_id" optionLabel="label" showClear/>
                <DatePicker v-model="appointment_date" dateFormat="dd/mm/yy" placeholder="New Appointment Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
                
            </div>
            
            <Button id="submit" label="Submit" @click.prevent="submit"/>
        </div>
    </div>
</template>