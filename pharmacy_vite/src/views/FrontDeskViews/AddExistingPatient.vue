<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { FilterMatchMode } from '@primevue/core/api';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 3000 });
    }

    const patientsData = ref([]);
    const isLoaded = ref([false]);
    const selectedPatient = ref();

    const first_name = ref('');
    const last_name = ref('');
    const gender = ref('');

    if (store.state.isRegistered) {
        axios.post('/frontdesk/getPatients/', {
            'first_name': '',
            'last_name': '',
            'gender': ''
        })
        .then( (response) => {
            patientsData.value = response.data.map(patient => ({
                ...patient,
                name: `${patient.first_name} ${patient.last_name}`
            }));
            isLoaded.value[0] = true;   
        })
        .catch( (error) => {
            warn("Error getting patients data.", "Please check the status of the server or try reloading.")
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
            patientsData.value = response.data.map(patient => ({
                ...patient,
                name: `${patient.first_name} ${patient.last_name}`
            }));
        })
        .catch( (error) => {
            warn('warn', 'Error in searching for the patient.', '')
        })
    }
</script>

<template>
    <div class="flex flex-column align-items-center justify-content-center">
        <Toast/>
        <h1 class="text-3xl font-bold m-3">Add Existing Patient</h1>
    </div>

    <div class="container">
        <div class="sub-container align-items-center justify-content-center">
            <InputText class="elements" id="first-name" placeholder="First Name" v-model.trim="first_name"/>
            <InputText class="elements" id="last-name" placeholder="Last Name" v-model.trim="last_name"/>
            <InputText class="elements" id="gender" placeholder="Gender" v-model.trim="gender"/>
            <Button id="search" label="Search" @click.prevent="search"/>
        </div>
    </div>

    

    <DataTable v-if="isLoaded[0] & patientsData.length > 0" :value="patientsData" datakey="id" removableSort :rows="3" paginator tableStyle="min-width: 22rem">
        <Column field="name" header="Name" style="width: 20%" sortable></Column>
        <Column field="age" header="Age" style="width: 20%" sortable></Column>
        <Column field="gender" header="Gender" style="width: 20%;" sortable></Column>
        <Column field="token_assigned" header="Token Number" style="width: 20%;" sortable></Column>
        <Column field="appointment_date" header="Last Appointment date" style="width: 20%" sortable></Column>
    </DataTable>

    <div v-else-if="patientsData.length == 0 && isLoaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
        There are no employees in this system.
    </div>

    <div class="centered" v-else>
        <ProgressSpinner/>
    </div>
</template>