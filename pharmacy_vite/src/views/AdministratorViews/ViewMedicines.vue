<script setup>
    import { ref, watch } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';
    import { capitalize } from '../../helpers';

    const toast = useToast();

    const store = useStore();
    store.dispatch('initializeStore');

    const usertype = store.state.usertype
    const usertype2 = capitalize(usertype);

    const deletion_dialog = ref();
    const selected_rows = ref()
    const medicines_data = ref([]);
    const length = ref(-1);
    const search_medicine_name = ref();
    
    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    const getMedicineWithoutFilter = () => {
        axios.get(`/${usertype}/getMedicines/`)
        .then( (response) => {
            medicines_data.value = response.data
            length.value = medicines_data.value.length
            console.log(medicines_data.value)
        })
        .catch( (error) => {
            warn('warn', 'Log in using an admin account to access this page.', '')
        })
    }

    if (store.state.is_registered === "true") {
        getMedicineWithoutFilter();
    }
    else {
        warn('warn', 'Log in using an admin account to access this page.', '')
    }
    
    const confirmDeletion = () => {      
        deletion_dialog.value = true;
    }

    const search = () => {
        if (!search_medicine_name.value) {
            getMedicineWithoutFilter();
            return;
        }

        axios.post(`/${usertype}/getMedicines/`, {
            'name': search_medicine_name.value
        })
        .then( (response) => {
            medicines_data.value = response.data
        })
        .catch( (error) =>{
            warn('warn', 'Error searching for the medicine with the given filter.', 'Please check the status of the server or try reloading.')
        })
    }

    const sendRequest = () => {
        deletion_dialog.value = false;

        let idArray = []

        for (let i = 0; i < selected_rows.value.length; i++) {
            idArray.push(selected_rows.value[i]['id'])
        }

        axios.post('/administrator/deleteMedicines/', { ids: idArray })
        .then( (response) => {
            
            medicines_data.value = medicines_data.value.filter(val => !selected_rows.value.includes(val));
            selected_rows.value = null;

            warn('success', 'Successfully deleted medicines!', '');
        })
        .catch( (error) => {
            warn('warn', 'Unsuccesful in deleting medicines.', 'Please try again.');
        })
    }
</script>

<template>
    <Toast />

    <div class="flex flex-row align-items-center justify-content-center mt-4">
        <InputText class="elements" id="medicine-name" placeholder="Medicine Name" v-model.trim="search_medicine_name"/>
        <Button id="search" label="Search" @click.prevent="search"/>
    </div>

    <div class="top-container mt-4" v-if="medicines_data.length >= 0">
        <div class="container">
            <div class="centered">
                <h1 class="text-3xl font-bold m-3">View Medicines</h1>    
            </div>

            <div v-if="medicines_data.length > 0">
                <div class="card">
                    <DataTable :value="medicines_data" tableStyle="min-width: 50rem" class="p-datatable-sm" sortable
                        v-model:selection="selected_rows"
                        paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]"
                        groupRowsBy="medicine.name" rowGroupMode="rowspan"
                    >
                        <Column selectionMode="multiple" style="width: 5rem"></Column>
                        <Column field="medicine.name" header="Name"/>
                        <Column field="stock" header="Stock"/>
                        <Column field="medicine.price" header="Price"/>
                        <Column field="medicine.manufacturer" header="Manufacturer"/>
                        <Column field="expiration_date" header="Expiration Date"/>
                    </DataTable>
                </div>
            </div>

            <div class="centered" v-if="medicines_data.length == 0">
                <h1 class="text-l font-bold m-2">There are no medicines registered in the system.</h1>
            </div>

            <div class="flex justify-center space-x-4 mt-8">
                <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeletion" :disabled="!selected_rows || !selected_rows.length" v-if="medicines_data.length > 0"/>
                <Button label="Add New Medicine" icon="pi pi-plus" severity="success" @click="$router.push({ name: `${usertype2}AddNewMedicine` })"/> 
                <Button label="Add Stock for Existing Medicine" icon="pi pi-plus" severity="success" @click="$router.push({ name: `${usertype2}AddExistingMedicine` })"/> 
            </div>
        </div>
    </div>

    <div v-else>
        <h1 class="text-3xl font-bold m-3">There are no medicines registered in the system.</h1>
    </div>

    <Dialog v-model:visible="deletion_dialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to delete the selected medicines?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="deletion_dialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendRequest"/>
        </template>
    </Dialog>
</template>