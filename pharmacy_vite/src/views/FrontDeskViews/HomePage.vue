<script setup>
    import router from '../../router';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { checkDate, convertDateFormat } from '../../helpers';
    import { format } from 'date-fns';
    
    const patients_data = ref([]);
    const doctors_data = ref([]);
    const no_show_patients_data = ref([]);
    const is_loaded = ref([false, false, false, false]);
    const unpaid_appointiments_data = ref([]);
    
    // The below variables are for scheduling a new appointment for a patient
    const appointment_date = ref();
    const selected_appointment = ref();

    const rebook_appointment_dialog = ref(false);
    const cancellation_dialog = ref(false);
    const payment_confirmation_dialog = ref(false);

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    const selected_doctor_scheduled = ref();
    const selected_doctor_no_show = ref();
    const selected_doctor_unpaid_appointments = ref();

    const is_registered = ref(store.state.is_registered)

    const getPatients = () => {
        axios.post('/frontdesk/getPatientsForDoctor/', { doctor_id: selected_doctor_scheduled.value['id'] })
        .then( (response) => {
            patients_data.value = response.data.map(appointment => ({
                ...appointment,
                'appointment_date': convertDateFormat(appointment.date), 
                'name': `${appointment.patient.first_name} ${appointment.patient.last_name}`
            }));
            is_loaded.value[0] = true;
        })
        .catch( (error) => {
            warn('warn', "Error getting patients data.", error)
        })
    }

    const getPatientsNoShow = () => {
        axios.post('/frontdesk/noShowUpdate/', {
            'doctor_id': selected_doctor_no_show.value['id']
        })
        .then( (response) => {
            no_show_patients_data.value = response.data.map(appointment => ({
                ...appointment,
                'appointment_date': convertDateFormat(appointment.date),
                'name': `${appointment.patient.first_name} ${appointment.patient.last_name}`
            }));

            is_loaded.value[2] = true;
        })
        .catch( (error) => {
            
            warn('warn', 'Error getting patients who did not show up.', error)
        })
    }

    const getUnpaidAppointments = () => {
        axios.post('/frontdesk/getUnpaidAppointments/', {
            'doctor_id': selected_doctor_unpaid_appointments.value['id']
        })
        .then( (response) => {
            unpaid_appointiments_data.value = response.data
            is_loaded.value[3] = true
        })
        .catch( (error) => {
            warn('warn', 'Error in getting unpaid appointments', error)
        })
    }

    if (is_registered.value === 'true') {
        // Gets all the doctors
        axios.get('/frontdesk/getDoctors/')
        .then( (response) => {
            doctors_data.value = response.data.map(doctor => ({
                ...doctor,
                label: `${doctor.name}: ${doctor.specialization}`
            }));
            
            selected_doctor_scheduled.value = doctors_data.value[0]
            selected_doctor_no_show.value = doctors_data.value[0]
            selected_doctor_unpaid_appointments.value = doctors_data.value[0]
            is_loaded.value[1] = true;
        })
        .catch( (error) => {
            warn('warn', 'Error getting doctor users data.', error);
        })

        watch(selected_doctor_scheduled, (newVal, oldVal) => {
            try { 
                if (typeof selected_doctor_scheduled.value == 'object') {
                    getPatients();
                }
            }
            catch (error) {
                warn('warn', 'Error getting data for patients.', '')
            }
        })

        watch(selected_doctor_no_show, (newVal, oldVal) => {
            try { 
                if (typeof selected_doctor_no_show.value == 'object') {
                    getPatientsNoShow();
                }
            }
            catch (error) {
                warn('warn', 'Error getting data for patients.', error)
            }
        })

        watch(selected_doctor_unpaid_appointments, (newVal, oldVal) => {
            try { 
                if (typeof selected_doctor_unpaid_appointments.value == 'object') {
                    getUnpaidAppointments();
                }
            }
            catch (error) {
                warn('warn', 'Error getting data for unpaid appointments.', error)
            }
        })
    } else {
        warn('warn', 'Please log in to access this page.', '')
    }

    const filtered_array = ref([]);

    const search = (event, fullArray) => {
        setTimeout(() => {
            const query = event.query.toLowerCase(); // User's searchScheduled input
            // Filter the full array based on the query
            const filtered = fullArray.filter(item =>
                item.label.toLowerCase().includes(query)
            );
            // Update the reactive ref's value
            filtered_array.value = filtered;
        }, 50);
    };

    const confirmNewAppointment = (id) => {      
        rebook_appointment_dialog.value = true;
        selected_appointment.value = id;
    }

    // For patients with 'no-show'
    const sendRebookAppointmentRequest = () => {
        rebook_appointment_dialog.value = false;

        if (!checkDate(appointment_date)) {
            warn('warn', 'Error with appointment date.', 'Make sure the date is filled and is today or after today.');
            return;
        }

        axios.post('/frontdesk/rebookAppointment/', {

            'id': selected_appointment.value,
            'date': format(new Date(appointment_date.value), 'yyyy-MM-dd')
        })
        .then( (response) => {
            warn('success', 'Successfully created an appointment for the patient.', '')
            getPatientsNoShow();
            getPatients();
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in creating an appointment for the patient.', error)
        })
    }

    const cancelled_patient_id = ref();
    const cancelled_patient_name = ref();

    const preliminaryCancel = (id, name) => {
        cancellation_dialog.value = true;
        cancelled_patient_id.value = id;
        cancelled_patient_name.value = name;
    }

    const sendCancelRequest = () => {
        axios.post('frontdesk/cancelAppointment/', {
            'id': cancelled_patient_id.value
        })
        .then( (response) => {
            warn('success', 'Successfully cancelled appointment for patient', '')
            getPatients();
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in cancelling appointment for the patient.', error)
        })
    }

    const payment_prescription_id = ref();
    const payment_patient_name = ref();

    const preliminaryPayment = (id, name) => {
        payment_confirmation_dialog.value = true;
        payment_prescription_id.value = id;
        payment_patient_name.value = name;
    }

    const sendPaymentRequest = () => {
        payment_confirmation_dialog.value = false;

        axios.post('/frontdesk/updatePrescription/', {
            'id': payment_prescription_id.value,
            'paid': true
        })
        .then( (response) => {
            warn('success', `Successfully paid for ${payment_patient_name.value}`, '');
            payment_prescription_id.value = null;
            payment_patient_name.value = '';
        })
        .catch( (error) => {
            warn('warn', 'Unsuccesful in payment for the prescription.', error)
            payment_prescription_id.value = null;
            payment_patient_name.value = '';
        })
        
    }
</script>

<template>
    <Toast/>
    <div class="flex flex-row space-y-2" v-if="is_registered === 'true'">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bold m-2">Scheduled Appointments</h1>
                    <AutoComplete v-model="selected_doctor_scheduled" optionLabel="label" dropdown :suggestions="filtered_array" @complete="(event) => search(event, doctors_data)" class="w-full" forceSelection/>
                    <DataTable v-if="is_loaded[0] & patients_data.length > 0" :value="patients_data" removableSort :rows="5" paginator tableStyle="min-width: 22rem">
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
                                <Button severity="danger" label="Cancel Appointment" @click.prevent="preliminaryCancel(slotProps.data.id, `${slotProps.data.name}`)"></Button>
                            </template>
                        </Column>
                    </DataTable>

                    <div v-else-if="patients_data.length == 0 && is_loaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
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

            <div class="card ml-5 mb-4">
                <h1 class="text-l font-bold m-2">No Show Appointments</h1>
                <AutoComplete v-model="selected_doctor_no_show" optionLabel="label" dropdown :suggestions="filtered_array" @complete="(event) => search(event, doctors_data)" class="w-full" forceSelection/>
                <DataTable v-if="is_loaded[2] & no_show_patients_data.length > 0" :value="no_show_patients_data" removableSort :rows="5" paginator tableStyle="min-width: 22rem">
                    <Column field="name" header="Name" sortable></Column>
                    <Column field="token_assigned" header="Token" sortable></Column>
                    <Column field="appointment_date" header="Date" sortable></Column>
                    <Column>
                        <template #body="slotProps">
                            <Button severity="success" label="Rebook Appointment" @click.prevent="confirmNewAppointment(slotProps.data.id)"></Button>
                        </template>
                    </Column>
                </DataTable>

                <div v-else-if="no_show_patients_data.length == 0 && is_loaded[2]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                    There are no "No-Show" patients for this doctor in the system.
                </div>

                <div class="centered" v-else>
                    <ProgressSpinner/>
                </div>
            </div>
        </div>

        <div class="flex flex-column">
            
            
            <div class="card ml-5 mb-4">
                <h1 class="text-l font-bold m-2">Unpaid Appointments</h1>
                <AutoComplete v-model="selected_doctor_unpaid_appointments" optionLabel="label" dropdown :suggestions="filtered_array" @complete="(event) => search(event, doctors_data)" class="w-full" forceSelection/>
                <DataTable v-if="is_loaded[3] && unpaid_appointiments_data.length > 0" :value="unpaid_appointiments_data" removableSort sortField="id" :sortOrder="1" :rows="3" paginator tableStyle="min-width: 22rem">
                    <Column field="id" header="Prescription ID" sortable/>
                    <Column field="patient_name" header="Patient Name" sortable/>
                    <Column field="age" header="Age"/>
                    <Column field="gender" header="Gender"/>
                    <Column field="cost.doctor_cost" header="Doctor Cost"/>
                    <Column field="cost.lab_tests_cost" header="Lab Tests Cost"/>
                    <Column field="cost.medicines_cost" header="Medicines Cost"/>
                    <Column field="cost.total_cost" header="Total Cost"/>
                    
                    <Column>
                        <template #body="slotProps">
                            <Button severity="success" label="Pay" @click.prevent="preliminaryPayment(slotProps.data.id, slotProps.data.patient_name)"/>
                        </template>
                    </Column>
                </DataTable>

                <div v-else-if="unpaid_appointiments_data.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                    There are no prescriptions that are unpaid.
                </div>

                <div class="centered" v-else>
                    <ProgressSpinner/>
                </div>
            </div>
        </div>
    </div>

    <Dialog v-model:visible="rebook_appointment_dialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex flex-column align-items-center justify-content-center">
            <DatePicker v-model="appointment_date" dateFormat="dd/mm/yy" placeholder="Appointment Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
            <Button label="Submit" icon="pi pi-check" text @click="sendRebookAppointmentRequest" class="mt-4"/>
        </div>
    </Dialog>

    <Dialog v-model:visible="cancellation_dialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to cancel the appointment for {{ cancelled_patient_name }}?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="cancellation_dialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendCancelRequest"/>
        </template>
    </Dialog>

    <Dialog v-model:visible="payment_confirmation_dialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to pay for the prescription for {{ payment_patient_name }}?</span>
        </div>
        
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="payment_confirmation_dialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendPaymentRequest"/>
        </template>
    </Dialog>
</template>