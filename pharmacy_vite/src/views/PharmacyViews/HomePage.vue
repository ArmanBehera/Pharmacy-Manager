<script setup>
    
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const medicine_inventory_data = ref([]);
    const lab_tests_data = ref([]);

    // Ordered this way: unverified users, employees, medicines, labtests
    const is_loaded = ref([false, false]);

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    const is_registered = ref(store.state.is_registered)

    if (is_registered.value === 'true') {
        axios.get('/pharmacy/getMedicines/')
        .then( (response) => {
            medicine_inventory_data.value = response.data;
            is_loaded.value[0] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting medicines data.", "Please check the status of the server or try reloading.")
        })

        axios.get('/pharmacy/getLabTests/')
        .then( (response) => {
            lab_tests_data.value = response.data;
            is_loaded.value[1] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting lab tests data.", "Please check the status of the server or try reloading.")
        })
    } else {
        warn('warn', "Log in using a pharmacy account to access this page.", '');
    }
</script>

<template>
    <Toast/>

    <div class="flex flex-row space-y-2" v-if="is_registered === 'true'">
        <div class="flex flex-column">
            <div class="flex flex-column">
                <div class="card ml-4 mb-4">
                    <h1 class="text-l font-bld m-2">Medicines</h1>
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
                    <h1 class="text-l font-bld m-2">Lab Tests</h1>
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
        </div>
    </div>
</template>