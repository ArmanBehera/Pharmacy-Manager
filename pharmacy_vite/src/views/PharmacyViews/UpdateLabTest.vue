<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, computed } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { useRoute } from 'vue-router';

    const store = useStore();
    store.dispatch('initializeStore');
    const is_registered = ref(store.state.is_registered);

    const toast = useToast();
    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    };

    const route = useRoute();
    const prescription_id = route.query.id;

    const prescription_details = ref(null);
    const lab_tests_data = ref([]); 
    const appointment_details = ref(null);
    const name = ref('');
    const gender = ref('');
    const age = ref('');

    const status = ref([]);
    const status_choices = ['Sample Collected', 'Report Collected', 'Patient Informed'];
    const sample_tracking_codes = ref([]);
    const report_codes = ref([]);

    const lab_tests_completed = ref(false);

    const unlisted_lab_tests_length = ref(0);
    const listed_lab_tests_length = ref(0);

    // Track API requests
    const is_loaded = ref([false, false, false]);
    const are_all_requests_made = computed(() => is_loaded.value.every(status => status));

    if (is_registered.value === 'true') {
        axios.post('/pharmacy/getCompletedPrescriptions/', { 
            'prescription_id': prescription_id
        })
        .then(response => {
            is_loaded.value[0] = true;
            prescription_details.value = response.data;
            console.log(prescription_details.value)

            unlisted_lab_tests_length.value = prescription_details.value.unlisted_lab_tests.length;
            listed_lab_tests_length.value = prescription_details.value.lab_tests.length;

            // Get patient details
            axios.post('/pharmacy/getAppointmentDetail/', { id: prescription_details.value.appointment })
            .then(response => {
                is_loaded.value[1] = true;
                appointment_details.value = response.data;
                name.value = `${appointment_details.value.patient.first_name} ${appointment_details.value.patient.last_name}`;
                gender.value = appointment_details.value.patient.gender === 'Male' ? 'M' : 'F';
                age.value = appointment_details.value.patient.age;
            })
            .catch( (error) => warn('warn', 'Error getting appointment details.', error));

            // Get lab test details using Promise.all
            const labTestRequests = prescription_details.value.lab_tests.map(test => 
                axios.post('/pharmacy/getLabTestsDetailsForID/', { id: test.id })
            );

            Promise.all(labTestRequests)
                .then(responses => {
                    lab_tests_data.value = responses.map(res => res.data);
                    is_loaded.value[2] = true;
                })
                .catch( (error) => warn('warn', 'Error getting lab test details.', error));
        })
        .catch(error => {
            warn('warn', 'Error getting prescription details.', error);
        });
    } else {
        warn('warn', 'Please log in to access this page.', '');
    }
    
    const submit = () => {
        axios.post('/pharmacy/updateLabTests/', {
            'id': prescription_details.value.lab_tests?.map(test => test.id) || [],
            'sample_tracking_code': sample_tracking_codes.value,
            'status': status.value,
            'report_code': report_codes.value
        })

        if (lab_tests_completed.value !== prescription_details.value.lab_tests_completed) {
            axios.post('/pharmacy/updatePrescription/', {
                'id': prescription_id,
                'lab_tests_completed': lab_tests_completed.value
            })
        }
    }


</script>

<template>
    <Toast />

    <div class="centered" v-if="is_registered === 'true'">
        <h1 class="text-3xl font-bold m-3">Prescription for {{ name }} ({{ age }}{{ gender }})</h1>
    </div>

    <div class="flex flex-column ml-5 mr-5" v-if="are_all_requests_made">
        <Divider type="solid" align="left">
            <h1 class="text-l font-bold">Available Lab Tests</h1>
        </Divider>

        <div v-if="listed_lab_tests_length > 0">
            <div v-for="(test, index) in lab_tests_data" :key="test.id" class="ml-5 mr-5 space-y-4">
                <div class="flex flex-row space-x-6 mt-4">
                    <h1 class="text-l font-bold">{{ test?.name }}</h1>
                    <h1 class="text-l font-bold">Sample Required: {{ test?.sample_required }}</h1>
                    <h1 class="text-l font-bold">Provider: {{ test?.provider }}</h1>
                </div>

                <div class="flex flex-row space-x-4">
                    <InputText v-model.trim="sample_tracking_codes[index]" placeholder="Sample Tracking Code" class="p-inputtext-sm w-full" />
                    <InputText v-model.trim="report_codes[index]" placeholder="Report Code" class="p-inputtext-sm w-full"/>
                    <Select class="elements" v-model.trim="status[index]" :options="status_choices" placeholder="Status *" showClear />
                </div>
                <Divider />
            </div>
        </div>

        <Divider type="solid" align="left">
            <h1 class="text-l font-bold">Unavailable Lab Tests</h1>
        </Divider>

        <div v-if="unlisted_lab_tests_length > 0">
            <ul>
                <li v-for="test in prescription_details?.unlisted_lab_tests" :key="test.id" class="ml-4">
                    {{ test?.name }}
                </li>
            </ul>
        </div>
        <div class="flex flex-row m-4">
            <label for="lab-tests-completed">Are all lab tests completed?</label>
            <Checkbox v-model="lab_tests_completed" id="lab-tests-completed" binary class="ml-2 mt-1"/>
        </div>
        
        <Button id="submit" label="Submit" @click.prevent="submit"/>
    </div>
</template>
