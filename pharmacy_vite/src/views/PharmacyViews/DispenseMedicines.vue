<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, computed, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { useRoute } from 'vue-router';

    const store = useStore();
    store.dispatch('initializeStore');
    const is_registered = ref(store.state.is_registered)

    const toast = useToast();
    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    };
    const route = useRoute();

    const prescription_id = route.query.id

    const prescription_details = ref();
    const appointment_details = ref();
    const medicines_data = ref();

    const unlisted_medicines_length = ref(0);
    const listed_medicines_length = ref(0);

    const name = ref();
    const gender = ref();
    const age = ref();

    const are_medicines_fulfilled = ref(false);

    // Prescription details, appointment details
    const is_loaded = ref([false, false, false]);
    const are_all_requests_made = computed(() => is_loaded.value.every(status => status));

    const quantity = ref([]);

    if (is_registered.value === 'true') {
        axios.post('/pharmacy/getCompletedPrescriptions/', { 
            'prescription_id': prescription_id
        })
        .then(response => {
            is_loaded.value[0] = true;
            prescription_details.value = response.data;
            console.log(prescription_details.value)

            unlisted_medicines_length.value = prescription_details.value.unlisted_medicines.length;
            listed_medicines_length.value = prescription_details.value.medicines.length;

            // Get patient details
            axios.post('/pharmacy/getAppointmentDetail/', { id: prescription_details.value.appointment })
            .then(response => {
                is_loaded.value[1] = true;
                appointment_details.value = response.data;
                name.value = `${appointment_details.value.patient.first_name} ${appointment_details.value.patient.last_name}`;
                gender.value = appointment_details.value.patient.gender === 'Male' ? 'M' : 'F';
                age.value = appointment_details.value.patient.age;
            })
            .catch((error) => warn('warn', 'Error getting appointment details.', error));

            const medicine_requests = prescription_details.value.medicines.map(medicine =>
                    axios.post('/pharmacy/getMedicinesDetailsForID/', { id: medicine.id })
                );

                Promise.all(medicine_requests)
                    .then(responses => {
                        medicines_data.value = responses.map(res => res.data)
                        console.log(medicines_data.value)
                        is_loaded.value[2] = true;
                    })
                    .catch((error) => warn('warn', 'Error getting medicines details.', error));
        })
        .catch( (error) => {
            warn('warn', 'Error getting prescription details', error)
        })
        
        
    }

    const submit = () => {
        let update_stock = []

        // Construct update_stock array with proper format
        for (let i = 0; i < medicines_data.value.length; i++) {
            update_stock.push({
                'id': medicines_data.value[i].id, 
                'quantity': quantity.value[i] ? quantity.value[i] : 0
            })
        }

        axios.post('pharmacy/updateStock/', {
            update_stock,  // Send as an array inside an object
            prescription_id
        })
        .then((response) => {
            const data = response.data

            data.forEach((item) => {
                if (item.status === 'updated') {
                    warn('success', `Successfully updated medicine stock for ${item.medicine_name}`, '')
                } else if (item.status === 'unavailable') {
                    warn('warn', `${item.quantity} units of ${item.medicine_name} are unavailable.`, '')
                } else {
                    warn('warn', `Unsuccessful in adding ${item.medicine_name}`, item.status)
                }
            })
        })
        .catch((error) => {
            warn('error', "An error occurred while updating stock.", error)
        })

        if (are_medicines_fulfilled.value !== prescription_details.value.medicines_fulfilled) {
            axios.post('/pharmacy/updatePrescription/', {
                'id': prescription_id,
                'medicines_fulfilled': are_medicines_fulfilled.value
            })
        }
    }

</script>

<template>
    <Toast />

    <div class="flex flex-col items-center p-6">
        <!-- Prescription Header -->
        <h1 v-if="is_registered === 'true'" class="text-3xl font-bold text-center mb-6">
            Prescription for {{ name }} ({{ age }}{{ gender }})
        </h1>

        <div v-if="are_all_requests_made" class="w-full max-w-4xl p-6 shadow-lg rounded-lg">
            <!-- Available Medicines -->
            <Divider type="solid" align="left">
                <h1 class="text-xl font-semibold text-gray-700">Available Medicines</h1>
            </Divider>

            <div v-if="listed_medicines_length > 0" class="grid grid-cols-2 gap-6">
                <div v-for="(medicine, index) in medicines_data" :key="medicine.id" class="bg-gray-100 p-4 rounded-lg shadow-md">
                    <h2 class="text-lg font-semibold text-gray-800">{{ medicine.name }}</h2>
                    <p class="text-gray-600 text-sm">Manufacturer: <span class="font-medium">{{ medicine.manufacturer }}</span></p>
                    <p class="text-gray-600 text-sm">Frequency: <span class="font-medium">{{ prescription_details.medicines[index].frequency }}</span></p>
                    <p class="text-gray-600 text-sm">Duration: <span class="font-medium">{{ prescription_details.medicines[index].duration_value }} {{ prescription_details.medicines[index].duration_unit }}</span></p>

                    <InputNumber id="quantity {{ index }}" placeholder="Quantity *" inputId="withoutgrouping" :useGrouping="false" v-model.number="quantity[index]" :min="0" class="p-inputnumber-sm w-full mt-2" size="small"/>
                </div>
            </div>

            <!-- Unavailable Medicines -->
            <Divider type="solid" align="left">
                <h1 class="text-xl font-semibold text-gray-700">Unavailable Medicines</h1>
            </Divider>

            <div v-if="unlisted_medicines_length > 0" class="bg-gray-100 p-4 rounded-lg shadow-md">
                <ul class="list-disc pl-5 space-y-3">
                    <li v-for="(medicine, index) in prescription_details.unlisted_medicines" :key="medicine.id">
                        <h2 class="text-lg font-semibold text-gray-800">{{ medicine.name }}</h2>
                        <p class="text-gray-600 text-sm">Frequency: <span class="font-medium">{{ medicine.frequency }}</span></p>
                        <p class="text-gray-600 text-sm">Duration: <span class="font-medium">{{ medicine.duration_value }} {{ prescription_details.medicines[index]?.duration_unit }}</span></p>
                    </li>
                </ul>
            </div>
        </div>

        <label>Note: Please give medicines whose expiration date is the earliest.</label>

        <div class="flex items-center mt-6">
            <label for="lab-tests-completed" class="text-gray-700">Are all medicines dispensed?</label>
            <Checkbox v-model="are_medicines_fulfilled" id="lab-tests-completed" binary class="ml-2 mt-1"/>
        </div>
        
        <Button label="Submit" @click.prevent="submit" class="mt-4"/>
    </div>
</template>