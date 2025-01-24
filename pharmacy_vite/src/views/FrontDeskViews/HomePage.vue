<script setup>
    import router from '../../router';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    
    const patientsData = ref([]);
    const doctorsData = ref([]);
    const isLoaded = ref([false]);

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 3000 });
    }

    const selectedDoctor = ref();

    const isRegistered = ref(store.state.isRegistered)

    if (isRegistered.value === 'true') {

        // Gets all the doctors
        axios.get('/frontdesk/getDoctors/')
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

        watch(selectedDoctor, (newVal, oldVal) => {
            try{ 
                if (typeof selectedDoctor.value == 'object') {
                    axios.post('/frontdesk/getPatientsForDoctor/', { doctor_id: selectedDoctor.value['id'] })
                    .then( (response) => {
                        patientsData.value = response.data;
                        isLoaded.value[0] = true;
                    })
                    .catch( (error) => {
                        warn("Error getting patients data.", "Please check the status of the server or try reloading.")
                    })
                }
            }
            catch (error) {
                console.log(error)
            }
        })
    } else {
        warn('Please log in to access this page.')
    }

    const filteredArray = ref();

    const search = (event, fullArray) => {
        setTimeout(() => {
            const query = event.query.toLowerCase(); // User's search input
            const filtered = fullArray.filter(item =>
                item.label.toLowerCase().includes(query) // Filter based on the `label` property
            );
            filteredArray.value = filtered; // Update suggestions dynamically
        }, 50);
    };
</script>

<template>
    <Toast/>
    <div class="flex flex-row space-y-2" v-if="isRegistered === 'true'">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <AutoComplete v-model="selectedDoctor" optionLabel="label" dropdown :suggestions="filteredArray" @complete="(event) => search(event, doctorsData)" class="w-full" forceSelection/>
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

                    <div class="centered">
                        <Button label="Add New Patient" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AddNewPatient' })" style="margin: 0.5rem"/>
                        <Button label="Add Existing Patient" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AddExistingPatient' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>