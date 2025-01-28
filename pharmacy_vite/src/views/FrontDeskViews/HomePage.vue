<script setup>
    import router from '../../router';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { checkDate, convertDateFormat } from '../../helpers';
    import { format } from 'date-fns';
    
    const patientsData = ref([]);
    const doctorsData = ref([]);
    const noShowPatientsData = ref([]);
    const isLoaded = ref([false, false, false]);
    
    // The below variables are for scheduling a new appointment for a patient
    const appointment_date = ref();
    const selectedAppointment = ref();
    const rebookAppointmentDialog = ref(false);

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

    const getPatientsNoShow = () => {
        axios.post('/frontdesk/noShowUpdate/', {
            'doctor_id': selectedDoctorNoShow.value['id']
        })
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

        watch(selectedDoctorNoShow, (newVal, oldVal) => {
            try { 
                if (typeof selectedDoctorNoShow.value == 'object') {
                    getPatientsNoShow();
                }
            }
            catch (error) {
                warn('warn', 'Error getting data for patients.', '')
            }
        })

        
    } else {
        warn('warn', 'Please log in to access this page.', '')
    }

    const filteredArrayScheduled = ref([]);
    const filteredArrayNoShow = ref([]);

    const confirmNewAppointment = (id) => {      
        rebookAppointmentDialog.value = true;
        selectedAppointment.value = id;
    }

    // For patients with 'no-show'
    const sendRebookAppointmentRequest = () => {
        rebookAppointmentDialog.value = false;

        if (!checkDate(appointment_date)) {
            warn('warn', 'Error with appointment date.', 'Make sure the date is filled and is today or after today.');
            return;
        }

        axios.post('/frontdesk/rebookAppointment/', {

            'id': selectedAppointment.value,
            'date': format(new Date(appointment_date.value), 'yyyy-MM-dd')
        })
        .then( (response) => {
            warn('success', 'Successfully created an appointment for the patient.', '')
            getPatientsNoShow();
            getPatients();
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in creating an appointment for the patient.', 'Please check the status of the server or try reloading.')
        })
    }

    const searchScheduled = (event, fullArray) => {
        setTimeout(() => {
            const query = event.query.toLowerCase(); // User's searchScheduled input
            // Filter the full array based on the query
            const filtered = fullArray.filter(item =>
                item.label.toLowerCase().includes(query)
            );
            // Update the reactive ref's value
            filteredArrayScheduled.value = filtered;
        }, 50);
    };

    const searchNoShow = (event, fullArray) => {
        setTimeout(() => {
            const query = event.query.toLowerCase(); // User's searchScheduled input
            // Filter the full array based on the query
            const filtered = fullArray.filter(item =>
                item.label.toLowerCase().includes(query)
            );
            // Update the reactive ref's value
            filteredArrayNoShow.value = filtered;
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
                    <AutoComplete v-model="selectedDoctorScheduled" optionLabel="label" dropdown :suggestions="filteredArrayScheduled" @complete="(event) => searchScheduled(event, doctorsData)" class="w-full" forceSelection/>
                    <DataTable v-if="isLoaded[0] & patientsData.length > 0" :value="patientsData" removableSort :rows="5" paginator tableStyle="min-width: 22rem">
                        <Column field="name" header="Name" sortable></Column>
                        <Column field="token_assigned" header="Token" sortable></Column>
                        <Column field="appointment_date" header="Date" sortable></Column>
                        <Column>
                            <template #body="slotProps">
                                <Button severity="success" label="Rebook Appointment" @click.prevent="confirmNewAppointment(slotProps.data.id)"></Button>
                            </template>
                        </Column>
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
                <AutoComplete v-model="selectedDoctorNoShow" optionLabel="label" dropdown :suggestions="filteredArrayNoShow" @complete="(event) => searchNoShow(event, doctorsData)" class="w-full" forceSelection/>
                <DataTable v-if="isLoaded[2] & noShowPatientsData.length > 0" :value="noShowPatientsData" removableSort :rows="5" paginator tableStyle="min-width: 22rem">
                    <Column field="name" header="Name" sortable></Column>
                    <Column field="token_assigned" header="Token" sortable></Column>
                    <Column field="appointment_date" header="Date" sortable></Column>
                    <Column>
                        <template #body="slotProps">
                            <Button severity="success" label="Rebook Appointment" @click.prevent="confirmNewAppointment(slotProps.data.id)"></Button>
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

    <Dialog v-model:visible="rebookAppointmentDialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex flex-column align-items-center justify-content-center">
            <DatePicker v-model="appointment_date" dateFormat="dd/mm/yy" placeholder="Appointment Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
            <Button label="Submit" icon="pi pi-check" text @click="sendRebookAppointmentRequest" class="mt-4"/>
        </div>
    </Dialog>
</template>