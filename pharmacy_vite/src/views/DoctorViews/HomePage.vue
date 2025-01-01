<script setup>
    
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 3000 });
    }

    if (store.state.isRegistered) {
        axios.get('/frontdesk/addPatient')
        .then( (response) => {
            doctorsData.value = response.data.map(doctor => ({
                ...doctor,
                label: `${doctor.name}: ${doctor.specialization}`
            }));
            
            selectedDoctor.value = doctorsData.value[0]
        })
        .catch( (error) => {
            warn('warn', 'Error getting doctor users data.', 'Please check the status of the server or try reloading.');
        })
    }
    
</script>

<template>
    <Toast/>
    <div class="flex flex-row space-y-2">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <DataTable v-if="isLoaded[0] & patientsData.length != 0" :value="patientsData" datakey="id" removableSort :rows="3" paginator tableStyle="min-width: 22rem">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                        <Column field="token_assigned" header="Token Number" style="width: 30%" sortable></Column>
                        <Column field="appointment_date" header="Date" style="width: 30%;" sortable></Column>
                    </DataTable>
                </div>
            </div>
        </div>
    </div> 
</template>