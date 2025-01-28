<script setup>
    import router from '../../router';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { convertDateFormat } from '../../helpers';
    
    const patientsData = ref([]);
    const doctorsData = ref([]);
    const noShowPatientsData = ref([]);
    const isLoaded = ref([false, false, false]);

    const deletionDialog = ref(false);

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    const selectedDoctorScheduled = ref();
    const selectedDoctorNoShow = ref();

    const isRegistered = ref(store.state.isRegistered)

    const getPatients = () => {
        axios.post('/frontdesk/getPatientsForDoctor/', { doctor_id: selectedDoctorScheduled.value['id'] })
        .then( (response) => {
            patientsData.value = response.data.map(appointment => ({
                ...appointment,
                'appointment_date': convertDateFormat(appointment.date), 
                'name': `${appointment.patient.first_name} ${appointment.patient.last_name}`
            }));
            isLoaded.value[0] = true;
        })
        .catch( (error) => {
            warn('warn', "Error getting patients data.", "Please check the status of the server or try reloading.")
        })
    }

    if (isRegistered.value === 'true') {
        // Gets all the doctors
        axios.get('/frontdesk/getDoctors/')
        .then( (response) => {
            doctorsData.value = response.data.map(doctor => ({
                ...doctor,
                label: `${doctor.name}: ${doctor.specialization}`
            }));
            
            selectedDoctorScheduled.value = doctorsData.value[0]
            selectedDoctorNoShow.value = doctorsData.value[0]
            isLoaded.value[1] = true;
        })
        .catch( (error) => {
            warn('warn', 'Error getting doctor users data.', 'Please check the status of the server or try reloading.');
        })

        watch(selectedDoctorScheduled, (newVal, oldVal) => {
            try { 
                if (typeof selectedDoctorScheduled.value == 'object') {
                    getPatients();
                }
            }
            catch (error) {
                warn('warn', 'Error getting data for patients.', '')
            }
        })

        axios.get('/frontdesk/noShowUpdate/')
        .then( (response) => {
            noShowPatientsData.value = response.data.map(appointment => ({
                ...appointment,
                'appointment_date': convertDateFormat(appointment.date),
                'name': `${appointment.patient.first_name} ${appointment.patient.last_name}`
            }));
            isLoaded.value[2] = true;
        })
        .catch( (error) => {
            
            warn('warn', 'Error getting patients who did not show up.', '')
        })
    } else {
        warn('warn', 'Please log in to access this page.', '')
    }

    const filteredArrayScheduled = ref([]);
    const filteredArrayNoShow = ref([]);

    const confirmDeletion = () => {      
        deletionDialog.value = true;
    }

    const sendDeleteRequest = () => {
        deletionDialog.value = false;
    }

    const search = (event, fullArray) => {
        setTimeout(() => {
            const query = event.query.toLowerCase(); // User's search input
            // Filter the full array based on the query
            const filtered = fullArray.filter(item =>
                item.label.toLowerCase().includes(query)
            );
            // Update the reactive ref's value
            filteredArrayScheduled.value = filtered;
        }, 50);
    };

    const cancel = (id) => {
        axios.post('frontdesk/cancelAppointment/', {
            'id': id
        })
        .then( (response) => {
            warn('success', 'Successfully cancelled appointment for patient', '')
            getPatients();
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in cancelling appointment for the patient.', 'Please check the status of the server and try reloading the page.')
        })
    }
</script>

<template>
    <Toast/>
    <div class="flex flex-row space-y-2" v-if="isRegistered === 'true'">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bld m-2">Scheduled Appointments</h1>
                    <AutoComplete v-model="selectedDoctorScheduled" optionLabel="label" dropdown :suggestions="filteredArrayScheduled" @complete="(event) => search(event, doctorsData)" class="w-full" forceSelection/>
                    <DataTable v-if="isLoaded[0] & patientsData.length > 0" :value="patientsData" removableSort :rows="5" paginator tableStyle="min-width: 22rem">
                        <Column field="name" header="Name" sortable></Column>
                        <Column field="token_assigned" header="Token" sortable></Column>
                        <Column field="appointment_date" header="Date" sortable></Column>
                        <Column>
                            <template #body="slotProps">
                                <Button severity="danger" label="Cancel Appointment" @click.prevent="cancel(slotProps.data.id)"></Button>
                            </template>
                        </Column>
                    </DataTable>

                    <div v-else-if="patientsData.length == 0 && isLoaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no scheduled patients for this doctor in the system.
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

        <div class="mb-4">
            <div class="card ml-5">
                <h1 class="text-l font-bld m-2">No Show Appointments</h1>
                <AutoComplete v-model="selectedDoctorNoShow" optionLabel="label" dropdown :suggestions="filteredArrayNoShow" @complete="(event) => search(event, doctorsData, filteredArrayNoShow)" class="w-full" forceSelection/>
                <DataTable v-if="isLoaded[2] & noShowPatientsData.length > 0" :value="noShowPatientsData" removableSort :rows="5" paginator tableStyle="min-width: 22rem">
                    <Column field="name" header="Name" sortable></Column>
                    <Column field="token_assigned" header="Token" sortable></Column>
                    <Column field="appointment_date" header="Date" sortable></Column>
                    <Column>
                        <template #body="slotProps">
                            <Button severity="success" label="New Appointment" icon="pi pi-external-link"  iconPos="right" @click.prevent=""></Button>
                        </template>
                    </Column>
                </DataTable>

                <div v-else-if="noShowPatientsData.length == 0 && isLoaded[2]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                    There are no "No-Show" patients for this doctor in the system.
                </div>

                <div class="centered" v-else>
                    <ProgressSpinner/>
                </div>
            </div>
        </div>
    </div>

    <Dialog v-model:visible="deletionDialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to delete the selected lab tests?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="deletionDialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendDeleteRequest"/>
        </template>
    </Dialog>
</template>