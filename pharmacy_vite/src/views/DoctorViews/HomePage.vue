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

    const patientsData = ref([]);
    const isLoaded = ref([false])

    if (store.state.isRegistered) {
        axios.post('/doctor/getPatients/', {
            doctor_id: store.state.userId
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
    }
</script>

<template>
    <Toast/>
    <div class="flex flex-row space-y-2">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <DataTable v-if="isLoaded[0] & patientsData.length > 0" :value="patientsData" removableSort :rows="3" paginator tableStyle="min-width: 22rem">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                        <Column field="token_assigned" header="Token Number" style="width: 30%" sortable></Column>
                        <Column field="appointment_date" header="Date" style="width: 30%;" sortable></Column>
                    </DataTable>
                    
                    <div v-else-if="patientsData.length == 0 && isLoaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no scheduled patients in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>
                </div>
            </div>
        </div>
    </div> 
</template>