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

    const specializationName = ref([]);
    
    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    if (store.state.isRegistered === "true") {
        axios.get(`/administrator/getSpecializations/`)
        .then( (response) => {
            data.value = response.data
            length.value = data.value.length
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

    const sendDeleteRequest = () => {
        deletionDialog.value = false;

        let idArray = []

        for (let i = 0; i < selected.value.length; i++) {
            idArray.push(selected.value[i]['id'])
        }

        axios.post('/administrator/deleteSpecializations/', { ids: idArray })
        .then( (response) => {
            data.value = data.value.filter(val => !selected.value.includes(val));
            selected.value = null;

            warn('success', 'Successfully deleted specializations!', '');
        })
        .catch( (error) => {
            warn('warn', 'Unsuccesful in deleting specializations.', 'Please try again.');
        })
    }

    const onRowEditSave = (event) => {
        let { newData, index } = event;

        // Updating the local instance
        data.value[index] = newData;

        console.log(data.value[index])
        
        // Sending a request to the backend to update the instance. 
        axios.post('/administrator/editSpecializations/', {
            ...data.value[index]
        })
        .then( (response) => {
            warn('success', 'Successfully edited specializations.', '')
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in editing specializations.', 'Please try again.')
        })  
    }

    const submit = () => {
        if (!specializationName.value) {
            warn('warn', 'Specialization Name field should be filled with the name of the specialization.', '');
            return;
        }

        axios.post('/administrator/addSpecializations/', {
            'specialization': specializationName.value
        })
        .then( (response) => {
            warn('success', 'Succesfully added specialization.', '')
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in adding specialization', '')
        })
    }
</script>

<template>
    <Toast />
    <div class="top-container flex flex-column justify-content-center align-items-center mt-4" v-if="data.length >= 0">
        <div class="container">
            <div class="centered">
                <h1 class="text-3xl font-bold m-3">View Specializations</h1>    
            </div>

            <div class="flex flex-column" v-if="data.length > 0">
                <div class="card">
                    <DataTable v-model:editingRows="editingRows" v-model:selection="selected" :value="data" editMode="row" dataKey="id" @row-edit-save="onRowEditSave" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]"
                    resizableColumns columnResizeMode="fit" tableStyle="min-width: 50rem" class="p-datatable-sm" 
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
                        
                        <Column field="specialization" header="Specialization Name">
                            <template #editor="{ data, field }">
                                <InputText v-model="data[field]" class="w-full p-inputtext-sm" />
                            </template>
                        </Column>

                        <Column field="number" header="Number of doctors under this specialization">
                            <template #editor="{ data, field }">
                                <InputNumber v-model.number="data[field]" :min="0" class="w-full p-inputnumber-sm" disabled/>
                            </template>
                        </Column>

                        <Column :rowEditor="true" :style="{ minWidth: '8rem' }" bodyStyle="text-align:center"></Column>
                    </DataTable>
                </div>
            </div>
            <div class="flex justify-center space-x-4 mt-8">
                <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeletion" :disabled="!selected || !selected.length" v-if="data.length > 0"/>
                <Button label="Add Specialization" icon="pi pi-plus" severity="success" @click="$router.push({ name: 'AddSpecialization' })"/>  
            </div>
        </div>

        
    </div>

    <div v-else>
        <h1 class="text-3xl font-bold m-3">There are no specializations registered in the system.</h1>
    </div>
        
    <div class="flex flex-column align-items-center justify-content-center">
        <h1 class="text-xl font-bold mt-10">Add Specializations</h1>  

        <div class="flex flex-row mt-2">
            <InputText id="name" placeholder="Specialization Name *" v-model.trim="specializationName"/>
            <Button label="Submit" @click.prevent="submit" class="ml-2"/>
        </div>
    </div>

    <Dialog v-model:visible="deletionDialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to delete the selected specializations?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="deletionDialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendDeleteRequest"/>
        </template>
    </Dialog>


</template>