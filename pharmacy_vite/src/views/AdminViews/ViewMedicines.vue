<script setup>
    import { ref } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const toast = useToast();

    const store = useStore();
    store.dispatch('initializeStore');

    const usertype = store.getters.getUserDetails['usertype']

    const deletionDialog = ref();
    const selected = ref()
    const data = ref([]);
    const length = ref(-1);
    const editingRows = ref([]);
    
    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    if (store.state.isRegistered === "true") {
        axios.get(`/${usertype}/getMedicines/`)
        .then( (response) => {
            data.value = response.data
            length.value = data.value.length
            console.log(data.value)
        })
        .catch( (error) => {
            warn('warn', 'Log in using an admin account to access this page.', '')
        })
    }
    else {
        warn('warn', 'Log in using an admin account to access this page.', '')
    }

    const confirmDeletion = () => {      
        deletionDialog.value = true;
    }

    const onRowEditSave = (event) => {
        let { newData, index } = event;

        data.value[index] = newData;

        axios.post('/administrator/viewMedicines/', {
             "id": newData.id,
             "name": newData.name,
             "manufacturer": newData.manufacturer,
             "expiration_date": newData.expiration_date,
             "price": newData.price,
             "stock": newData.stock,
             "description": newData.description
        });
    };

    const sendRequest = () => {
        deletionDialog.value = false;

        let idArray = []

        for (let i = 0; i < selected.value.length; i++) {
            idArray.push(selected.value[i]['id'])
        }

        axios.post('/administrator/viewMedicines/', { ids: idArray })
        .then( (response) => {
            
            data.value = data.value.filter(val => !selected.value.includes(val));
            selected.value = null;

            warn('success', 'Successfully deleted medicines!', '');
        })
        .catch( (error) => {
            warn('warn', 'Unsuccesful in deleting medicines.', 'Please try again.');
        })
    }
</script>

<template>
    <Toast />
    <div class="top-container" v-if="data.length >= 0">
        <div class="container">
            <div class="centered">
                <h1 class="text-3xl font-bold m-3">View Medicines</h1>    
            </div>

            <div v-if="data.length > 0">
                <div class="card">
                    <DataTable :value="data" resizableColumns columnResizeMode="fit" tableStyle="min-width: 50rem" class="p-datatable-sm" sortable
                     v-model:selection="selected"
                     paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]"
                     v-model:editingRows="editingRows" @row-edit-save="onRowEditSave" editMode="row" dataKey="id" 
                     groupRowsBy="medicine.id" rowGroupMode="rowspan"
                        :pt="{
                            table: { style: 'min-width: 50rem' },
                            column: {
                                bodycell: ({ state }) => ({
                                    style:  state['d_editing'] && 'padding-top: 0.75rem; padding-bottom: 0.75rem'
                                })
                            }
                        }" 
                    >
                        <Column selectionMode="multiple" style="width: 5rem"></Column>

                        <Column field="medicine.name" header="Name">
                            <template #editor="{ data, field }">
                                <InputText v-model="data[field]" class="w-full p-inputtext-sm" />
                            </template>
                        </Column>

                        <Column field="stock" header="Stock">
                            <template #editor="{ data, field }">
                                <InputNumber v-model.number="data[field]" :min="0" disabled class="w-full p-inputnumber-sm" />
                            </template>
                        </Column>

                        <Column field="medicine.price" header="Price">
                            <template #editor="{ data, field }">
                                <InputNumber v-model.number="data[field]" :min="0" class="w-full p-inputnumber-sm" />
                            </template>
                        </Column>
                        
                        <Column field="medicine.manufacturer" header="Manufacturer">
                            <template #editor="{ data, field }">
                                <InputText v-model="data[field]" class="w-full p-inputtext-sm" />
                            </template>
                        </Column>

                        <Column field="expiration_date" header="Expiration Date">
                            <template #editor="{ data, field }">
                                <DatePicker v-model="data[field]" dateFormat="dd/mm/yy" disabled placeholder="Expiration Date" class="p-datepicker-sm w-full" />
                            </template>
                        </Column>

                        <Column field="medicine.description" header="Description">
                            <template #editor="{ data, field }">
                                <InputText v-model="data['field']" class="w-full p-inputtext-sm" :style="{ minWidth: '20rem' }"/>
                            </template>
                        </Column>

                        <Column :rowEditor="true" :style="{ minWidth: '8rem' }" bodyStyle="text-align:center"></Column>
                    </DataTable>
                </div>
            </div>

            <div class="centered" v-if="data.length == 0">
                <h1 class="text-l font-bold m-2">There are no medicines registered in the system.</h1>
            </div>

            <div class="flex justify-center space-x-4 mt-8">
                <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeletion" :disabled="!selected || !selected.length" v-if="data.length > 0"/>
                <Button label="Add Medicines" icon="pi pi-plus" severity="success" @click="$router.push({ name: 'AddMedicines' })"/>  
            </div>
        </div>
    </div>

    <div v-else>
        <h1 class="text-3xl font-bold m-3">There are no medicines registered in the system.</h1>
    </div>

    <Dialog v-model:visible="deletionDialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to delete the selected medicines?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="deletionDialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendRequest"/>
        </template>
    </Dialog>
</template>