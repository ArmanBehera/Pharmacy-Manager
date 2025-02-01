<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { checkDate } from '../../helpers';
    import { format } from 'date-fns';

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
            warn('warn', "Error getting patients data.", "Please check the status of the server or try reloading.")
        })

        axios.get('/frontdesk/getDoctors/')
        .then( (response) => {
            doctors_data.value = response.data.map(doctor => ({
            ...doctor,
            label: `${doctor.name}: ${doctor.specialization}` // Combine name and specialization
        }));
        })
        .catch( (error) => {
            warn('warn', 'Error getting doctor users data.', 'Please check the status of the server or try reloading.');
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
            warn('warn', 'Error in searching for the patient.', 'Please check the status of the server or try reloading.')
        })
    }

    const submit = () => {
        const data = {
            'patient_id': selected_patient.value.id,
            'doctor_id': selected_doctor.value.id,
            'date': format(new Date(appointment_date.value), 'yyyy-MM-dd'),
            'status': 'Scheduled'
        }

        if (!data.patient_id || !data.doctor_id || !data.date) {
            warn('warn', 'All values must be filled.', '')
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
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in making appointment.', 'Please check the status of the server or try reloading.')
        })
    }
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
            <div class="sub-container">
                <Select class="elements" id="doctorChoice" v-model.trim="selected_doctor" :options="doctors_data" optionLabel="label" placeholder="Doctor Assigned*" showClear/>
                <DatePicker v-model="appointment_date" dateFormat="dd/mm/yy" placeholder="Appointment Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
            </div>

            <Button id="submit" label="Submit" @click.prevent="submit"/>
        </div>
    </div>
</template>