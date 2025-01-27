<script setup>
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const unverifiedUsersData = ref([]);
    const medicineInventoryData = ref([]);
    const employeesData = ref([]);
    const labTestsData = ref([]);
    const specializationsData = ref([]);

    // Ordered this way: unverified users, employees, medicines, labtests
    const isLoaded = ref([false, false, false, false, false]);

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    const isRegistered = ref(store.state.isRegistered)

    if (isRegistered.value === 'true') {
        axios.get('administrator/verifyEmployees/')
        .then( (response) => {
            unverifiedUsersData.value = response.data;
            isLoaded.value[0] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting unverified users data.", "Please check the status of the server or try reloading.")
        })

        axios.get('administrator/getEmployees/')
        .then( (response) => {
            employeesData.value = response.data;
            isLoaded.value[1] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting employees data.", "Please check the status of the server or try reloading.")
        })

        // To get data for inventory
        axios.get('/administrator/getMedicines/')
        .then( (response) => {
            medicineInventoryData.value = response.data;
            isLoaded.value[2] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting medicines data.", "Please check the status of the server or try reloading.")
        })

        axios.get('/administrator/getLabTests/')
        .then( (response) => {
            labTestsData.value = response.data;
            isLoaded.value[3] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting lab tests data.", "Please check the status of the server or try reloading.")
        })

        axios.get('/administrator/getSpecializations/')
        .then( (response) => {
            specializationsData.value = response.data;
            isLoaded.value[4] = true;
        })
        .catch( (error) => {
            warn("warn", "Error getting specializations data.", "Please check the status of the server or try reloading.")
        })
    }
</script>

<template>
    <Toast/>
    <div class="flex flex-row space-y-2" v-if="isRegistered === 'true'">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bld m-2">Employees</h1>
                    <DataTable v-if="isLoaded[0] & employeesData.length > 0" :value="employeesData" removableSort :rows="3" paginator tableStyle="min-width: 22rem">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                    </DataTable>

                    <div v-else-if="employeesData.length == 0 && isLoaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no employees in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="View or Delete Employees" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'ViewEmployees' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>

            <div>
                <div class="card ml-5">
                    <h1 class="text-l font-bld m-2">Verify Employees</h1>
                    <DataTable v-if="isLoaded[1] & unverifiedUsersData.length > 0" :value="unverifiedUsersData" removableSort :rows="2" paginator tableStyle="min-width: 22rem">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                    </DataTable>

                    <div v-else-if="isLoaded[1] & unverifiedUsersData.length === 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        All employees verified!
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered" v-if="unverifiedUsersData.length > 0">
                        <Button label="Verify Employees" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'VerifyEmployees' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bld m-2">Medicines</h1>
                    <DataTable v-if="isLoaded[2] & medicineInventoryData.length > 0" :value="medicineInventoryData" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                        <Column field="medicine.name" header="Name" style="width: 30%" sortable></Column>
                        <Column field="stock" header="Stock" style="width: 30%" sortable></Column>
                        <Column field="expiration_date" header="Expiration Date" style="width: 40%" :sortable="true"></Column>
                    </DataTable>

                    <div v-else-if="isLoaded[2] & medicineInventoryData.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no medicines in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="Edit or Add Medicines" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'ViewMedicines' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>

            <div>
                <div class="card ml-5">
                    <h1 class="text-l font-bld m-2">Lab Tests</h1>
                    <DataTable v-if="isLoaded[3] & labTestsData.length > 0" :value="labTestsData" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                        <Column field="name" header="Name"/>
                        <Column field="provider" header="Provider"/>
                    </DataTable>

                    <div v-else-if="isLoaded[3] & labTestsData.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no labtests in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="Edit or Add Lab Tests" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'ViewLabTests' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <h1 class="text-l font-bld m-2">Specializations</h1>
                    <DataTable v-if="isLoaded[4] & specializationsData.length > 0" :value="specializationsData" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem">
                        <Column field="specialization" header="Specialization" style="width: 30%" sortable></Column>
                        <Column field="number" header="Number of doctors" style="width: 70%" sortable></Column>
                    </DataTable>

                    <div v-else-if="isLoaded[4] & specializationsData.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no medicines in this system.
                    </div>

                    <div class="centered" v-else>
                        <ProgressSpinner/>
                    </div>

                    <div class="centered">
                        <Button label="Edit or Add Specializations" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'ViewSpecializations' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>