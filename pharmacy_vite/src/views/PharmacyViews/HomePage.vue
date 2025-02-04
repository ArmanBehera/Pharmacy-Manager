<script setup>
    
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const medicine_inventory_data = ref([]);
    const lab_tests_data = ref([]);
    const doctors_data = ref([]);
    const completed_medicines_data = ref([])
    const completed_lab_tests_data = ref([])

    // Ordered this way: Medicines inventory data, Lab Tests data, Doctors data, Completed medicines Data, Completed Lab Tests Data
    const is_loaded = ref([false, false, false, false, false]);

    const selected_doctor_prescribed_medicine = ref();
    const selected_doctor_prescribed_lab_test = ref();

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    const is_registered = ref(store.state.is_registered)

    const getPrescriptionsForDoctor = (id, code) => {
        axios.post('/pharmacy/getCompletedPrescriptions/', {
                'doctor_id': id,
                'code': code
            })
            .then( (response) => {
                if (code === 1) {
                    completed_medicines_data.value = response.data
                    is_loaded.value[3] = true; 
                    console.log(completed_medicines_data.value)
                } else if (code === 2) {
                    completed_lab_tests_data.value = response.data
                    is_loaded.value[4] = true;
                    console.log(completed_medicines_data.value)
                }
            })
            .catch( (error) => {
                warn('warn', 'Error getting completed prescriptions data.', error)
            })
    }

    if (is_registered.value === 'true') {
        axios.get('/pharmacy/getMedicines/')
        .then( (response) => {
            medicine_inventory_data.value = response.data;
            is_loaded.value[0] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting medicines data.", error)
        })

        axios.get('/pharmacy/getLabTests/')
        .then( (response) => {
            lab_tests_data.value = response.data;
            is_loaded.value[1] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting lab tests data.", error)
        })

        axios.get('/pharmacy/getDoctors/')
        .then( (response) => {
            doctors_data.value = response.data.map(doctor => ({
                ...doctor,
                label: `${doctor.name}: ${doctor.specialization}`
            }));
            
            selected_doctor_prescribed_medicine.value = doctors_data.value[0]
            selected_doctor_prescribed_lab_test.value = doctors_data.value[0]
            is_loaded.value[2] = true;
        })
        .catch( (error) => {
            warn('warn', 'Error getting doctor users data.', error);
        })

        watch(selected_doctor_prescribed_medicine, (newVal, oldVal) => {
            try {
                if (typeof selected_doctor_prescribed_medicine.value == 'object') {
                    getPrescriptionsForDoctor(newVal.id, 1);
                }
            } catch (error) {
                warn('warn', 'Error getting completed prescriptions data 200.', error)
            }
        })

        watch(selected_doctor_prescribed_lab_test, (newVal, oldVal) => {
            try {
                if (typeof selected_doctor_prescribed_lab_test.value == 'object') {
                    getPrescriptionsForDoctor(newVal.id, 2);
                }
            } catch (error) {
                warn('warn', 'Error getting completed prescriptions data 100.', error)
            }
        })
    } else {
        warn('warn', "Log in using a pharmacy account to access this page.", '');
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

    
</script>

<template>
    <Toast/>

    <div class="flex flex-row space-y-2" v-if="is_registered === 'true'">
        <div class="flex flex-column">
            <div class="card ml-4 mb-4">
                <h1 class="text-l font-bold m-2">Medicines</h1>
                <DataTable v-if="is_loaded[0] & medicine_inventory_data.length > 0" :value="medicine_inventory_data" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                    <Column field="medicine.name" header="Name" style="width: 30%" sortable></Column>
                    <Column field="stock" header="Stock" style="width: 30%" sortable></Column>
                    <Column field="expiration_date" header="Expiration Date" style="width: 40%" :sortable="true"></Column>
                </DataTable>

                <div v-else-if="is_loaded[0] & medicine_inventory_data.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                    There are no medicines in this system.
                </div>

                <div class="centered" v-else>
                    <ProgressSpinner/>
                </div>

                <div class="centered">
                    <Button label="Edit or Add Medicines" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'PharmacyViewMedicines' })" style="margin: 0.5rem"/>
                </div>
            </div>

            <div class="card ml-4">
                <h1 class="text-l font-bold m-2">Lab Tests</h1>
                <DataTable v-if="is_loaded[1] & lab_tests_data.length > 0" :value="lab_tests_data" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                    <Column field="name" header="Name"/>
                    <Column field="provider" header="Provider"/>
                </DataTable>

                <div v-else-if="is_loaded[1] & lab_tests_data.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                    There are no labtests in this system.
                </div>

                <div class="centered" v-else>
                    <ProgressSpinner/>
                </div>

                <div class="centered">
                    <Button label="Edit or Add Lab Tests" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'PharmacyViewLabTests' })" style="margin: 0.5rem"/>
                </div>
            </div>
        </div>

        <div class="flex flex-column">
            <div class="card ml-4 mb-4">
                <h1 class="text-l font-bold m-2">Dispense Prescribed Medicines</h1>
                <AutoComplete v-model="selected_doctor_prescribed_medicine" optionLabel="label" dropdown :suggestions="filtered_array" @complete="(event) => search(event, doctors_data)" class="w-full" forceSelection/>
                <DataTable v-if="is_loaded[3] & completed_medicines_data.length > 0" :value="completed_medicines_data" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                    <Column field="prescription_id" header="ID" sortable></Column>
                    <Column field="name" header="Patient Name"sortable></Column>
                    <Column field="created_at" header="Time Created" sortable></Column>
                    <Column>
                        <template #body="slotProps">
                            <Button severity="success" label="Prescription" icon="pi pi-external-link"  iconPos="right" @click.prevent="$router.push({ name: 'DispenseMedicines', query: { id: slotProps.data.prescription_id } })"></Button>
                        </template>
                    </Column>
                </DataTable>

                <div v-else-if="is_loaded[3] & completed_medicines_data.length == 0" style="min-width: 20rem; padding:1rem">
                    There are no prescriptions that match the given filter.
                </div>

                <div class="centered" v-else>
                    <ProgressSpinner/>
                </div>
            </div>

            <div class="card ml-4 mb-4">
                <h1 class="text-l font-bold m-2">Update Prescribed Lab Tests</h1>
                <AutoComplete v-model="selected_doctor_prescribed_lab_test" optionLabel="label" dropdown :suggestions="filtered_array" @complete="(event) => search(event, doctors_data)" class="w-full" forceSelection/>
                <DataTable v-if="is_loaded[4] & completed_lab_tests_data.length > 0" :value="completed_lab_tests_data" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                    <Column field="prescription_id" header="ID" sortable></Column>
                    <Column field="name" header="Patient Name"sortable></Column>
                    <Column field="created_at" header="Time Created" sortable></Column>
                    <Column>
                        <template #body="slotProps">
                            <Button severity="success" label="Prescription" icon="pi pi-external-link"  iconPos="right" @click.prevent="$router.push({ name: 'UpdateLabTest', query: { id: slotProps.data.prescription_id } })"></Button>
                        </template>
                    </Column>
                </DataTable>

                <div v-else-if="is_loaded[4] & completed_lab_tests_data.length == 0" style="min-width: 20rem; padding:1rem">
                    There are no lab tests that match the given filter.
                </div>

                <div class="centered" v-else>
                    <ProgressSpinner/>
                </div>
            </div>
        </div>
    </div>
</template>