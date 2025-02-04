<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, computed, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { useRoute } from 'vue-router';
    import { convertDateFormat } from '../../helpers';

    const store = useStore();
    store.dispatch('initializeStore');
    const is_registered = ref(store.state.is_registered);

    const toast = useToast();
    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    };

    const route = useRoute();
    const appointment_id = ref(route.query.id);

    const prescription_details = ref(null);
    const lab_tests_data = ref([]); 
    const medicines_data = ref([]);
    const appointment_details = ref();

    const name = ref('');
    const gender = ref('');
    const age = ref('');
    const additional_information = ref();

    const unlisted_lab_tests_length = ref(0);
    const listed_lab_tests_length = ref(0);

    const unlisted_medicines_length = ref(0);
    const listed_medicines_length = ref(0);

    // Track API requests
    const is_loaded = ref([false, false, false, false]);
    const are_all_requests_made = computed(() => is_loaded.value.every(status => status));

    const is_previous_prescription_present = ref(false);

    const fetch_data = () => {
        axios.post('/doctor/getPrescriptionID/', {
            'appointment_id': appointment_id.value
        })    
        .then( (response) => {
            const prescription_id = response.data

            axios.post('/doctor/getCompletedPrescriptions/', { 
                'prescription_id': prescription_id
            })
            .then(response => {
                is_loaded.value[0] = true;
                prescription_details.value = response.data;
                additional_information.value = prescription_details.value.additional_information ? prescription_details.value.additional_information : 'No additional information prescribed.';

                unlisted_lab_tests_length.value = prescription_details.value.unlisted_lab_tests.length;
                listed_lab_tests_length.value = prescription_details.value.lab_tests.length;

                unlisted_medicines_length.value = prescription_details.value.unlisted_medicines.length;
                listed_medicines_length.value = prescription_details.value.medicines.length;

                // Get patient details
                axios.post('/doctor/getAppointmentDetail/', { id: prescription_details.value.appointment })
                .then(response => {
                    is_loaded.value[1] = true;
                    appointment_details.value = response.data;
                    name.value = `${appointment_details.value.patient.first_name} ${appointment_details.value.patient.last_name}`;
                    gender.value = appointment_details.value.patient.gender === 'Male' ? 'M' : 'F';
                    age.value = appointment_details.value.patient.age;

                    is_previous_prescription_present.value = appointment_details.value.previous_appointment ? true : false;
                })
                .catch((error) => warn('warn', 'Error getting appointment details.', error));

                // Get lab test details using Promise.all
                const lab_test_requests = prescription_details.value.lab_tests.map(test => 
                    axios.post('/doctor/getLabTestsDetailsForID/', { id: test.id })
                );

                Promise.all(lab_test_requests)
                    .then(responses => {
                        lab_tests_data.value = responses.map(res => res.data);
                        is_loaded.value[2] = true;
                    })
                    .catch((error) => warn('warn', 'Error getting lab test details.', error));

                const medicine_requests = prescription_details.value.medicines.map(medicine =>
                    axios.post('/doctor/getMedicinesDetailsForID/', { id: medicine.id })
                );

                Promise.all(medicine_requests)
                    .then(responses => {
                        medicines_data.value = responses.map(res => res.data)
                        console.log(medicines_data.value)
                        is_loaded.value[3] = true;
                    })
                    .catch((error) => warn('warn', 'Error getting medicines details.', error));
            })
            .catch( (error) => {
                warn('warn', 'Error getting prescription details.', error);
            });
        })
        .catch( (error) => {
            warn('warn', 'Error getting prescription id from the appointment id.', error)
        })
    }

    if (is_registered.value === 'true') {
        fetch_data();
    } else {
        warn('warn', 'Please log in to access this page.', '');
    }
    
    watch(
    () => route.query, 
    (newQuery, oldQuery) => {
        if (newQuery !== oldQuery) {
            window.location.reload();
        }
    }, 
    { deep: true }
    );

</script>

<template>
    <Toast />

    <div v-if="is_registered === 'true'" class="flex flex-col items-center text-center p-6">
        <h1 class="text-3xl font-bold">Prescription for {{ name }} ({{ age }}{{ gender }})</h1>
    </div>

    <div v-if="are_all_requests_made" class="max-w-2xl mx-auto p-6 shadow-lg rounded-lg">
        <div>
            <h2 class="text-xl font-semibold border-b pb-2 mb-4">Medicines</h2>
            <div v-if="listed_medicines_length > 0">
                <ul class="list-disc list-inside space-y-2">
                    <li v-for="n in listed_medicines_length" :key="n">
                        <span class="font-medium">{{ medicines_data[n - 1].name }}</span> - 
                        {{ prescription_details.medicines[n - 1].frequency }}x a day for 
                        {{ prescription_details.medicines[n - 1].duration_value }} 
                        {{ prescription_details.medicines[n - 1].duration_unit }}
                    </li>
                </ul>
            </div>

            <div v-if="unlisted_medicines_length > 0" class="mt-4">
                <ul class="list-disc list-inside space-y-2">
                    <li v-for="n in unlisted_medicines_length" :key="n">
                        <span class="font-medium">{{ prescription_details.unlisted_medicines[n - 1].name }}</span> - 
                        {{ prescription_details.unlisted_medicines[n - 1].frequency }}x a day for 
                        {{ prescription_details.unlisted_medicines[n - 1].duration_value }} 
                        {{ prescription_details.unlisted_medicines[n - 1].duration_unit }}
                    </li>
                </ul>
            </div>
        </div>

        <div class="mt-6">
            <h2 class="text-xl font-semibold border-b pb-2 mb-4">Lab Tests</h2>
            <div v-if="listed_lab_tests_length > 0">
                <ul class="list-disc list-inside space-y-2">
                    <li v-for="n in listed_lab_tests_length" :key="n">
                        <span class="font-medium">{{ lab_tests_data[n - 1].name }}</span> - 
                        Test Date: {{ prescription_details.lab_tests[n - 1].test_date ? prescription_details.lab_tests[n - 1].test_date : 'None' }}, 
                        Status: {{ prescription_details.lab_tests[n - 1].status }}
                        Report Code: {{ prescription_details.lab_tests[n - 1].report_code ? prescription_details.lab_tests[n - 1].report_code : 'None' }}
                    </li>
                </ul>
            </div>

            <div v-if="unlisted_lab_tests_length > 0" class="mt-4">
                <ul class="list-disc list-inside space-y-2">
                    <li v-for="n in unlisted_lab_tests_length" :key="n">
                        <span class="font-medium">{{ prescription_details.unlisted_lab_tests[n - 1].name }}</span>
                    </li>
                </ul>
            </div>
        </div>

        <div class="mt-6" v-if="are_all_requests_made">
            <h2 class="text-xl font-semibold border-b pb-2 mb-4">Additional Information</h2>
            <label class="font-semibold">{{ additional_information }}</label>
        </div>

        <div class="mt-6">
            <h2 class="text-xl font-semibold border-b pb-2 mb-4">Previous Prescription</h2>
            <router-link v-if="is_previous_prescription_present" class="underline" :to="{ name: 'ViewPrescription', query: { id: appointment_details.previous_appointment } }">Link to Previous Prescription</router-link>
            <label v-else>There are no previous prescriptions.</label>
        </div>
    </div>
</template>
