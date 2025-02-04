<script setup>
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const unverified_users_data = ref([]);
    const medicine_inventory_data = ref([]);
    const employees_data = ref([]);
    const lab_tests_data = ref([]);
    const specializations_data = ref([]);

    // Ordered this way: unverified users, employees, medicines, labtests
    const is_loaded = ref([false, false, false, false, false]);

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    const is_registered = ref(store.state.is_registered)

    if (is_registered.value === 'true') {
        axios.get('administrator/verifyEmployees/')
        .then( (response) => {
            unverified_users_data.value = response.data;
            is_loaded.value[0] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting unverified users data.", error)
        })

        axios.get('administrator/getEmployees/')
        .then( (response) => {
            employees_data.value = response.data;
            is_loaded.value[1] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting employees data.", error)
        })

        // To get data for inventory
        axios.get('/administrator/getMedicines/')
        .then( (response) => {
            medicine_inventory_data.value = response.data;
            is_loaded.value[2] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting medicines data.", error)
        })

        axios.get('/administrator/getLabTests/')
        .then( (response) => {
            lab_tests_data.value = response.data;
            is_loaded.value[3] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting lab tests data.", error)
        })

        axios.get('/administrator/getSpecializations/')
        .then( (response) => {
            specializations_data.value = response.data;
            is_loaded.value[4] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting specializations data.", error)
        })
    } else { 
        warn('warn', "Log in using an admin account to access this page.", '');
    }
</script>

<template>
    <Toast/>
    <div class="flex flex-row space-y-2" v-if="is_registered === 'true'">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bold m-2">Employees</h1>
                    <DataTable v-if="is_loaded[0] & employees_data.length > 0" :value="employees_data" removableSort :rows="3" paginator tableStyle="min-width: 22rem">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                    </DataTable>

                    <div v-else-if="employees_data.length == 0 && is_loaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no employees in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="View or Delete Employees" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AdministratorViewEmployees' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>

            <div>
                <div class="card ml-5">
                    <h1 class="text-l font-bold m-2">Verify Employees</h1>
                    <DataTable v-if="is_loaded[1] & unverified_users_data.length > 0" :value="unverified_users_data" removableSort :rows="2" paginator tableStyle="min-width: 22rem">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                    </DataTable>

                    <div v-else-if="is_loaded[1] & unverified_users_data.length === 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        All employees verified!
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered" v-if="unverified_users_data.length > 0">
                        <Button label="Verify Employees" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AdministratorVerifyEmployees' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bold m-2">Medicines</h1>
                    <DataTable v-if="is_loaded[2] & medicine_inventory_data.length > 0" :value="medicine_inventory_data" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                        <Column field="medicine.name" header="Name" style="width: 30%" sortable></Column>
                        <Column field="stock" header="Stock" style="width: 30%" sortable></Column>
                        <Column field="expiration_date" header="Expiration Date" style="width: 40%" :sortable="true"></Column>
                    </DataTable>

                    <div v-else-if="is_loaded[2] & medicine_inventory_data.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no medicines in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="Edit or Add Medicines" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AdministratorViewMedicines' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>

            <div>
                <div class="card ml-5">
                    <h1 class="text-l font-bold m-2">Lab Tests</h1>
                    <DataTable v-if="is_loaded[3] & lab_tests_data.length > 0" :value="lab_tests_data" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                        <Column field="name" header="Name"/>
                        <Column field="provider" header="Provider"/>
                    </DataTable>

                    <div v-else-if="is_loaded[3] & lab_tests_data.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no labtests in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="Edit or Add Lab Tests" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AdministratorViewLabTests' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bold m-2">Specializations</h1>
                    <DataTable v-if="is_loaded[4] & specializations_data.length > 0" :value="specializations_data" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                        <Column field="specialization" header="Specialization" style="width: 30%" sortable></Column>
                        <Column field="number" header="Number of doctors" style="width: 70%" sortable></Column>
                    </DataTable>

                    <div v-else-if="is_loaded[4] & specializations_data.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no specializations in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="Edit or Add Specializations" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AdministratorViewSpecializations' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>