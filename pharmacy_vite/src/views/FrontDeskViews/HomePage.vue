<script setup>
    import router from '../../router';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    
    const patientsData = ref([]);
    const isLoaded = ref([false])

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 3000 });
    }

    if (store.state.isRegistered) {
    
        axios.get('')
        .then( (response) => {
            patientsData.value = response.data;
            isLoaded.value[0] = true;
        })
        .catch( (error) => {
            warn("Error getting unverified users data.", "Please check the status of the server or try reloading.")
        })
    } else {
        warn('Please log in to access this page.')
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
                        <Colum field="appointment_number" header="Appointment Number" style="width: 30%" sortable></Colum> <!-- the value for field attribute has to be changed and find a way to presort the table using this table-->
                    </DataTable>


                    <div v-else-if="patientsData.length == 0 && isLoaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no recent patients in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="Add Patient" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AddPatient' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>