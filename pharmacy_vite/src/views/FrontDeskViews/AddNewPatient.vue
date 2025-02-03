<script setup>
    import router from '../../router';
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

    const first_name = ref('');
    const last_name = ref('');
    const primary_phone_number = ref('');
    const secondary_phone_number = ref(''); 
    const age = ref();
    const gender = ref('');
    const gender_choices = ref([
        {gender: 'Male'},
        {gender: 'Female'}, 
        {gender: 'Other'}
    ]);
    const selected_doctor = ref();
    const appointment_date = ref();

    const doctors_data = ref([]);

    if (store.state.is_registered === 'true') {
        
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

    const submit = () => {

        let data = {
            'first_name': first_name.value,
            'last_name': last_name.value,
            'primary_phone_number': primary_phone_number.value,
            'age': age.value,
            'gender': gender.value['gender'],
            'secondary_phone_number': secondary_phone_number.value ? secondary_phone_number.value : '0',
        };

        var filled = true;

        // Checks for any empty fields
        // Do not have to check for null fields since .trim() function already handles undefined values
        for (const key in data) {
            const value = data[key];
            if (key !== 'secondary_phone_number'){
                if (typeof value === 'string' && value.trim() === '') {
                    filled = false;
                    break; // Exit the loop early if an empty field is found
                } else if (typeof value === 'number' && value === 0) {
                    filled = false;
                    break; // Exit the loop early if a zero value is found
                }
            }
        }

        if (!selected_doctor.value) {
            warn('warn', 'Patient has to be assgined a doctor.', 'Select a doctor from the dropdown menu.');
            return;
        }

        if (!checkDate(appointment_date))  {
            warn('warn', 'Error with appointment date.', 'Make sure the date is filled and is today or after today.');
            return;
        }

        if (filled) {
            axios.post('/frontdesk/addNewPatient/', {
                'patient': {
                    ...data
                },
                'doctor': selected_doctor.value.id,
                'date': format(new Date(appointment_date.value), 'yyyy-MM-dd'),
                'status': 'Scheduled',
                'previous_appointment_id': null
            })
            .then( (response) => {
                warn('success', `Token Number: ${response.data.token_assigned}`, 'Successfully added patient.')

                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            })  
            .catch( (error) => {
                warn('warn', 'Failed to add patient into the system.', 'Make sure all the fields are filled appropriately or try reloading this page.')
            })
        } else {
            warn('warn', 'Not all fields are filled.', '')
        }
    }
</script>

<template>
    <div class="flex align-items-center justify-content-center">
        <Toast/>
        <h1 class="text-3xl font-bold m-3">Add New Patient</h1>
    </div>

    <div class="top-container centered">
        <div class="centered">
            <div class="sub-container">
                <InputText class="elements" id="first-name" placeholder="First Name*" v-model.trim="first_name"/>
                <InputText class="elements" id="last-name" placeholder="Last Name*" v-model.trim="last_name"/>
            </div>

            <div class="sub-container">
                <InputText class="elements" id="primary-phone-number" placeholder="Primary Phone Number*" v-model.trim="primary_phone_number"/>
                <InputText class="elements" id="secondary-phone-number" placeholder="Secondary Phone Number" v-model.trim="secondary_phone_number"/>
            </div>

            <div class="sub-container">
                <InputNumber class="elements" id="age" placeholder="Age*" inputId="withoutgrouping" :useGrouping="false" v-model.number="age" :min="0" :max="100" :allowEmpty="true"/>
                <Select class="elements" id="gender" v-model.trim="gender" :options="gender_choices" optionLabel="gender" placeholder="Gender*" showClear/>
            </div>

            <div class="sub-container">
                <Select class="elements" id="doctorChoice" v-model.trim="selected_doctor" :options="doctors_data" optionLabel="label" placeholder="Doctor Assigned*" showClear/>
                <DatePicker v-model="appointment_date" dateFormat="dd/mm/yy" placeholder="Appointment Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
            </div>
        </div>
    </div>
    <Button id="submit" label="Submit" @click.prevent="submit"/>
</template>