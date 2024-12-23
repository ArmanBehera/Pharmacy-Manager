<script setup>
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import '../../styles/styles.css';

    const unverifiedUsersData = ref([]);
    const medicineInventoryData = ref([]);
    const employeesData = ref([]);

    const store = useStore();
    store.dispatch('initializeStore');

    if (store.getters.isRegistered) {

        axios.get('administrator/verifyEmployees/')
        .then( (response) => {
            unverifiedUsersData.value = response.data
        })
        .catch( (error) => {
            console.log("Error getting unverified users data.")
        })

        axios.get('administrator/viewEmployees/')
        .then( (response) => {
            employeesData.value = response.data
        })
        .catch( (error) => {
            console.log("Error getting employees data")
        })

        // To get data for inventory
        axios.get('/administrator/viewMedicines/')
        .then( (response) => {
            medicineInventoryData.value = response.data
        })
        .catch( (error) => {
            console.log("Error getting medicines data")
        })
    }
</script>

<template>
    <div class="flex flex-row space-y-2">
        <div class="flex flex-column">
            <div class="mb-4">
                <div class="card ml-5">
                    <DataTable :value="employeesData" datakey="id" removableSort :rows="3" paginator tableStyle="min-width: 22rem" v-if="employeesData.length != 0">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                    </DataTable>
                    
                    <div v-if="employeesData.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no employees in this system.
                    </div>

                    <div class="centered">
                        <Button label="View Employees" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'ViewEmployees' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>

            <div>
                <div class="card ml-5">
                    <DataTable :value="unverifiedUsersData" datakey="id" removableSort :rows="2" paginator tableStyle="min-width: 22rem" v-if="unverifiedUsersData.length != 0">
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                    </DataTable>

                    <div v-if="unverifiedUsersData.length === 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        All users verified!
                    </div>

                    <div class="centered" v-if="unverifiedUsersData.length != 0">
                        <Button label="Verify Employees" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'VerifyEmployees' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>

        <div>
            <div>
                <div class="card ml-5">
                    <DataTable :value="medicineInventoryData" datakey="id" removableSort :rows="3" paginator sortField="stock" :sortOrder="1" tableStyle="min-width: 22rem" v-if="medicineInventoryData.length != 0">
                        <Column field="name" header="Name" style="width: 30%" sortable></Column>
                        <Column field="stock" header="Stock" style="width: 30%" sortable></Column>
                        <Column field="expiration_date" header="Expiration Date" style="width: 40%" :sortable="true"></Column>
                    </DataTable>

                    <div v-if="medicineInventoryData.length == 0" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
                        There are no medicines in this system.
                    </div>

                    <div class="centered">
                        <Button label="View or Add Medicines" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'ViewMedicines' })" style="margin: 0.5rem"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>