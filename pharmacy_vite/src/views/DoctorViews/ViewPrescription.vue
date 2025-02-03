<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, computed } from 'vue';
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
    const appointment_id = route.query.id;

    const prescription_details = ref(null);
    const lab_tests_data = ref([]); 
    const appointment_details = ref(null);

    const name = ref('');
    const gender = ref('');
    const age = ref('');

    const unlisted_lab_tests_length = ref(0);
    const listed_lab_tests_length = ref(0);

    const unlisted_medicines_length = ref(0);
    const listed_medicines_length = ref(0);

    // Track API requests
    const is_loaded = ref([false, false, false]);
    const are_all_requests_made = computed(() => is_loaded.value.every(status => status));

    if (is_registered.value === 'true') {

        axios.post('/doctor/getPrescriptionID/', {
            'appointment_id': appointment_id
        })    
        .then( (response) => {
            const prescription_id = response.data

            axios.post('/doctor/getCompletedPrescriptions/', { 
                'prescription_id': prescription_id
            })
            .then(response => {
                is_loaded.value[0] = true;
                prescription_details.value = response.data;
                console.log(prescription_details.value)

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
                })
                .catch(() => warn('warn', 'Error getting appointment details.', 'Please try again.'));

                // Get lab test details using Promise.all
                const labTestRequests = prescription_details.value.lab_tests.map(test => 
                    axios.post('/doctor/getLabTestsDetailsForID/', { id: test.id })
                );

                Promise.all(labTestRequests)
                    .then(responses => {
                        lab_tests_data.value = responses.map(res => res.data);
                        console.log(lab_tests_data.value)
                        is_loaded.value[2] = true;
                    })
                    .catch(() => warn('warn', 'Error getting lab test details.', 'Please try again.'));
            })
            .catch( (error) => {
                warn('warn', 'Error getting prescription details.', error);
            });
        })
    } else {
        warn('warn', 'Please log in to access this page.', '');
    }
    
    const submit = () => {
        
    }
</script>

<template>
    <Toast />

    <div class="centered" v-if="is_registered === 'true'">
        <h1 class="text-3xl font-bold m-3">Prescription for {{ name }} ({{ age }}{{ gender }})</h1>
    </div>

    <div class="flex flex-column ml-5 mr-5" v-if="are_all_requests_made">
        <Divider type="solid" align="left">
            <h1 class="text-l font-bold">Medicines</h1>
        </Divider>
        
        <Divider type="solid" align="left">
            <h1 class="text-l font-bold">Lab Tests</h1>
        </Divider>

        <div v-if="listed_lab_tests_length > 0">
            <ul>
                <li v-for="test in lab_tests_data" :key="id" class="ml-4">
                    {{ test.name }}
                </li>
            </ul>
        </div>

        <div v-if="unlisted_lab_tests_length > 0">
            <ul>
                <li v-for="test in prescription_details?.unlisted_lab_tests" :key="test.id" class="ml-4">
                    {{ test?.name }}
                </li>
            </ul>
        </div>

        <Button id="submit" label="Submit" @click.prevent="submit"/>
    </div>
</template>