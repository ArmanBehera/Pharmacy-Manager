<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, computed, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { useRoute } from 'vue-router';
    import { AutoComplete, InputText } from 'primevue';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();
    const route = useRoute();

    const appointment_details = ref();
    const id =  route.query.id;

    const name = ref('');
    const gender = ref('');
    const age = ref('');

    const medicine_count = ref(1);
    const medicines_data = ref([]);
    const prescribed_medicines = ref([]);
    const frequency_medicines = ref([]);
    const duration_medicines = ref([]);
    const duration_unit = ref([]);
    const duration_unit_choices = ref(['Days', 'Months'])

    const timings = ref([]);
    const custom_timing_descriptions = ref([]);

    const timings_choices = ref(['Before Food', 'After Food', 'Custom'])

    const lab_test_count = ref(1);
    const lab_tests_data = ref([])
    const prescribed_lab_tests = ref([]);

    const unlisted_index_array_medicine = ref([])
    const unlisted_index_array_lab_tests = ref([])

    const additional_information = ref();

    const is_previous_prescription_present = ref(false);

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    const is_registered = ref(store.state.is_registered)

    if (is_registered.value === 'true') {
        axios.post('/doctor/getAppointmentDetail/', {
            'id': id
        })
        .then( (response) => {
            appointment_details.value = response.data;
            console.log(appointment_details.value)
            is_previous_prescription_present.value = appointment_details.value.previous_appointment ? true : false;

            name.value = `${appointment_details.value.patient.first_name} ${appointment_details.value.patient.last_name}`
            gender.value = appointment_details.value.patient.gender === 'Male'? 'M' : 'F'
            age.value = appointment_details.value.patient.age 
        })
        .catch( (error) => {
            warn('warn', 'Error getting appointment details for the patient.', 'Please check the status of the server or try reloading.')
        })

        axios.get('/doctor/getMedicines/')
        .then( (response) => {
            medicines_data.value = response.data
        })
        .catch( (error) => {
            warn('warn', 'Error getting medicines data.', 'Please check the status of the server or try reloading.')
        })

        axios.get('/doctor/getLabTests/')
        .then( (response) => {
            lab_tests_data.value = response.data
        })
        .catch( (error) => {
            warn('warn', 'Error getting lab tests data.', 'Please check the status of the server or try reloading.')
        })
    } else {
        warn('warn', 'Please log in to access this page.', '')
    }

    const filtered_array = ref();

    const search = (event, full_array) => {
        setTimeout(() => {
            if (!event.query.trim().length) {
                filtered_array.value = [...full_array]
            } else {
                filtered_array.value = full_array.filter((element) => {
                    return element.name.toLowerCase().startsWith(event.query.toLowerCase());
                });
            }
        }, 50);
    }

    // Computed function to check if a specific medicine is unlisted
    const isUnlistedMedicine = (index) => {
        return computed(() => {
            const selected_medicine = prescribed_medicines.value[index];
            return selected_medicine && !medicines_data.value.some(medicine => medicine.name === selected_medicine.name);
        });
    };

    // Watch for changes in prescribedMedicines and update indexArrayMedicine
    watch(prescribed_medicines, (new_medicines) => {
        unlisted_index_array_medicine.value = new_medicines
            .map((medicine, index) => ({
                isUnlisted: medicine && !medicines_data.value.some(med => med.name === medicine.name),
                index,
            }))
            .filter(med => med.isUnlisted)
            .map(med => med.index);
    }, { deep: true });

    watch(prescribed_lab_tests, (new_lab_tests) => {
        unlisted_index_array_lab_tests.value = new_lab_tests
            .map((lab_test, index) => ({
                isUnlisted: lab_test && !lab_tests_data.value.some(lab => lab.name === lab_test.name),
                index,
            }))
            .filter(med => med.isUnlisted)
            .map(med => med.index);
    }, { deep: true });


    const submit = () => {
        const listed_medicines = ref([])
        const listed_lab_tests = ref([])

        const unlisted_medicines = ref([])
        const unlisted_lab_tests = ref([])

    
        for (let i = 0; i < medicine_count.value; i++) {
            if (prescribed_medicines.value[i] && frequency_medicines.value[i] && duration_medicines.value[i] && duration_unit.value[i]) {
                if (unlisted_index_array_medicine.value.some(index => index === i)) {
                    if (timings.value[i]) {
                        if (timings.value[i] === 'Custom') {
                            if (!custom_timing_descriptions.value[i]) {
                                warn('warn', 'Medicines assigned with custom timing need to have a description.', '')
                                return;
                            }
                        }
                        unlisted_medicines.value.push({'name': prescribed_medicines.value[i], 'frequency': frequency_medicines.value[i], 'duration_value': duration_medicines.value[i], 'duration_unit': duration_unit.value[i], 'timings': timings.value[i], 'custom_timing_description': custom_timing_descriptions.value[i] ? custom_timing_descriptions.value[i] : ''})
                    } else {
                        warn('warn', 'Assign timing for consumption of medicine.', '')
                        return;
                    }
                } else {
                    listed_medicines.value.push({'medicine': prescribed_medicines.value[i].id, 'frequency': frequency_medicines.value[i], 'duration_value': duration_medicines.value[i], 'duration_unit': duration_unit.value[i], 'status': 'Prescribed'})
                }
            } else {
                if (prescribed_medicines.value.length !== 0) {
                    warn('warn', 'Fill up all the fields for all prescribed medicines.', '');
                    return;
                }
            }
        }
        
        // Make similar checks for lab tests
        for (let i = 0; i < lab_test_count.value; i++) {
            console.log(prescribed_lab_tests.value[i])
            if (prescribed_lab_tests.value[i]){
                if (unlisted_index_array_lab_tests.value.some(index => index === i)) {
                    unlisted_lab_tests.value.push({'name': prescribed_lab_tests.value[i]});
                } else {
                    listed_lab_tests.value.push({'lab_test': prescribed_lab_tests.value[i].id, 'test_date': null, 'test_result': null, 'attachment': null, 'status': 'Prescribed', 'sample_tracking_code': null});
                }
            } else {
                if (prescribed_lab_tests.value.length !== 0) {
                    warn('warn', 'Fill in the name for the lab tests.', '');
                    return;
                }
            }
        }

        if (listed_medicines.value.length === 0 && listed_lab_tests.value.length === 0 && unlisted_medicines.value.length === 0 && unlisted_lab_tests.value.length === 0 && !additional_information.value) {
            warn('warn', 'Please fill in at least one of the fields to make a valid prescription.', '');
            return;
        }

        const medicines_fulfilled = ref(false);
        const lab_tests_completed = ref(false);

        if (listed_medicines.value.length === 0 && unlisted_medicines.value.length === 0) {
            medicines_fulfilled.value = true;
        }

        if (listed_lab_tests.value.length === 0 && unlisted_lab_tests.value.length === 0) {
            lab_tests_completed.value = true;
        }

        // Id of the medicine, followed by the duration and the others
        const prescription_to_send = {
            'appointment': appointment_details.value.id,
            'medicines': listed_medicines.value,
            'lab_tests': listed_lab_tests.value,
            'unlisted_medicines': unlisted_medicines.value,
            'unlisted_lab_tests': unlisted_lab_tests.value,
            'additional_information': additional_information.value ? additional_information.value : '',
            'medicines_fulfilled': medicines_fulfilled.value,
            'lab_tests_completed': lab_tests_completed.value
        }
        
        axios.post('/doctor/addPrescription/', {
            ...prescription_to_send
        })
        .then( (response) => {
            warn('success', 'Successfully added prescription for the patient.', '')
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in adding prescription for the patient.', 'Please check the status of the server or try reloading.')
        })
    }
</script>

<template>
    <Toast/>

    <div class="centered" v-if="is_registered === 'true'">
        <h1 class="text-3xl font-bld m-3">Prescription for {{ name }} ({{ age }}{{ gender }})</h1>
    </div>


    <div class="container mx-auto flex flex-column" v-if="is_registered === 'true'">
        <div class="flex flex-col space-y-4">
            <label class="text-xl font-semibold">Medicines</label>
            <div v-for="n in medicine_count" :key="n" class="flex flex-row items-center space-x-4">
                <AutoComplete :placeholder="`Medicine ${n}*`" v-model="prescribed_medicines[n - 1]" optionLabel="name" dropdown :suggestions="filtered_array" @complete="(event) => search(event, medicines_data )" class="w-full" />
                <InputNumber id="frequency" placeholder="Frequency *" inputId="withoutgrouping" :useGrouping="false" v-model.number="frequency_medicines[n-1]" :min="0" class="p-inputnumber-sm w-full"/>
                <InputNumber id="duration" placeholder="Duration *" inputId="minmaxfraction" :minFractionDigits="1" :maxFractionDigits="2" :useGrouping="false" v-model.number="duration_medicines[n-1]" :min="0" class="p-inputnumber-sm w-full"/>
                <Select v-model="duration_unit[n - 1]" :options="duration_unit_choices" placeholder="Unit *"/>
                <Select v-model="timings[n - 1]" :options="timings_choices" placeholder="Timing for taking the medicine *" v-if="isUnlistedMedicine(n - 1).value"/>
                <Select v-model="timings[n - 1]" :options="timings_choices" placeholder="Timing for taking the medicine" v-else disabled/>
                <InputText v-model.trim="custom_timing_descriptions[n - 1]" id="customTiming" placeholder="Custom Timing Description *" v-if="timings[n - 1] === 'Custom'" class="p-inputtext-sm w-full"/>
            </div>
            <div>
                <Button label="Add Medicine" @click.prevent="medicine_count += 1"/>
                <Button label="Delete Medicine" severity="danger" @click.prevent="medicine_count = medicine_count > 1 ? medicine_count - 1 : medicine_count" class="ml-4"/>
            </div>
        </div>

        <div class="flex flex-col space-y-4 mt-4">
            <label class="text-xl font-semibold">Lab Tests</label>
            <div v-for="n in lab_test_count" :key="n" class="flex flex-row justify-content-center align-items-center space-x-4">
                <AutoComplete :placeholder="`Lab Test ${n}`" v-model="prescribed_lab_tests[n - 1]" optionLabel="name" dropdown :suggestions="filtered_array" @complete="(event) => search(event, lab_tests_data )" class="w-full" />
            </div>
            <div>
                <Button label="Add Lab Test" @click.prevent="lab_test_count += 1"/>
                <Button label="Delete Lab Test" severity="danger" @click.prevent="lab_test_count = lab_test_count > 1 ? lab_test_count - 1 : lab_test_count" class="ml-4"/>
            </div>
        </div>

        <div class="flex flex-col spaace-y-4 mt-4">
            <label class="text-xl font-semibold">Additional Information</label>
            <InputText v-model.trim="additional_information" id="additionalInformation" placeholder="Additional Information" class="mt-2 p-inputtext-sm w-full"/>
        </div>

        <div class="flex flex-col spaace-y-4 mt-4">
            <label class="text-xl font-semibold">Previous Prescriptions</label>
            <router-link v-if="is_previous_prescription_present" class="underline" :to="{ name: 'ViewPrescription', query: { id: appointment_details.previous_appointment } }">Link to Previous Prescription</router-link>
            <label v-else>There are no previous prescriptions.</label>
        </div>

        <div class="flex justify-content-center align-items-center mt-4">
            <Button severity="success" label="Submit" @click.prevent="submit" v-if="is_registered === 'true'"/>
            <Button severity="danger" label="Submit" disabled v-else/>
        </div>
    </div>
</template>