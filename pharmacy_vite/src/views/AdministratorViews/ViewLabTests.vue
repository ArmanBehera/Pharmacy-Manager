<script setup>
    import { capitalize, ref } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const toast = useToast();

    const store = useStore();
    store.dispatch('initializeStore');

    const usertype = store.state.usertype
    const usertype2 = capitalize(usertype)

    const deletion_dialog = ref();
    const selected_rows = ref()
    const lab_tests_data = ref([]);
    const length = ref(-1);
    const editing_rows = ref([]);
    
    const search_lab_test_name = ref();

    const warn = (warn, summary, detailed) => {
        toast.add({ severity: warn, summary: summary, detail: detailed, life: 3000 });
    }

    const getLabTestWithoutFilter = () => {
        axios.get(`/${usertype}/getLabTests/`)
        .then( (response) => {
            lab_tests_data.value = response.data
            length.value = lab_tests_data.value.length
        })
        .catch( (error) => {
            warn('warn', 'Log in using an admin account to access this page.', error)
        })
    }

    if (store.state.is_registered === "true") {
        getLabTestWithoutFilter();
    }
    else {
        warn('warn', 'Log in using an admin account to access this page.', '')
    }

    const confirmDeletion = () => {      
        deletion_dialog.value = true;
    }

    const sendDeleteRequest = () => {
        deletion_dialog.value = false;

        let idArray = []

        for (let i = 0; i < selected_rows.value.length; i++) {
            idArray.push(selected_rows.value[i]['id'])
        }

        axios.post(`/${usertype}/deleteLabTests/`, { ids: idArray })
        .then( (response) => {
            lab_tests_data.value = lab_tests_data.value.filter(val => !selected_rows.value.includes(val));
            selected_rows.value = null;

            warn('success', 'Successfully deleted lab tests!', '');
        })
        .catch( (error) => {
            warn('warn', 'Unsuccesful in deleting lab tests.', error);
        })
    }

    const onRowEditSave = (event) => {
        let { newData, index } = event;

        // Updating the local instance
        lab_tests_data.value[index] = newData;

        console.log(lab_tests_data.value[index])
        
        // Sending a request to the backend to update the instance. 
        axios.post('/administrator/editLabTests/', {
            ...lab_tests_data.value[index]
        })
        .then( (response) => {
            warn('success', 'Successfully edited lab tests.', '')
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in editing lab tests.', error)
        })  
    }

    const search = () => {
        if (!search_lab_test_name.value) {
            getLabTestWithoutFilter();
            return;
        }

        axios.post(`/${usertype}/getLabTests/`, {
            'name': search_lab_test_name.value
        })
        .then( (response) => {
            lab_tests_data.value = response.data
        })
        .catch( (error) =>{
            warn('warn', 'Error searching for the medicine with the given filter.', error)
        })
    }
</script>

<template>
    <Toast />

    <div class="flex flex-row align-items-center justify-content-center mt-4">
        <InputText class="elements" id="lab-test-name" placeholder="Lab Test Name" v-model.trim="search_lab_test_name"/>
        <Button id="search" label="Search" @click.prevent="search"/>
    </div>

    <div class="top-container mt-4" v-if="lab_tests_data.length >= 0">
        <div class="container">
            <div class="centered">
                <h1 class="text-3xl font-bold m-3">View Lab Tests</h1>    
            </div>

            <div class="flex flex-column" v-if="lab_tests_data.length > 0">
                <div class="card">
                    <DataTable v-model:editingRows="editing_rows" v-model:selection="selected_rows" :value="lab_tests_data" editMode="row" dataKey="id" @row-edit-save="onRowEditSave" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]"
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
                        
                        <Column field="name" header="Name">
                            <template #editor="{ data, field }">
                                <InputText v-model="data[field]" class="w-full p-inputtext-sm" />
                            </template>
                        </Column>

                        <Column field="test_cost" header="Test Cost">
                            <template #editor="{ data, field }">
                                <InputNumber v-model.number="data[field]" :min="0" class="w-full p-inputnumber-sm" />
                            </template>
                        </Column>

                        <Column field="provider" header="Provider">
                            <template #editor="{ data, field }">
                                <InputText v-model="data[field]" class="w-full p-inputtext-sm" />
                            </template>
                        </Column>

                        <Column :rowEditor="true" :style="{ minWidth: '8rem' }" bodyStyle="text-align:center"></Column>
                    </DataTable>
                </div>
            </div>

            <div v-else>
                <h1 class="centered font-bold m-3">There are no lab tests registered in the system.</h1>
            </div>

            <div class="flex justify-center space-x-4 mt-8">
                <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeletion" :disabled="!selected_rows || !selected_rows.length" v-if="lab_tests_data.length > 0"/>
                <Button label="Add Lab Tests" icon="pi pi-plus" severity="success" @click="$router.push({ name: `${usertype2}AddLabTests` })"/>  
            </div>
        </div>
    </div>

    

    <Dialog v-model:visible="deletion_dialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to delete the selected lab tests?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="deletion_dialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendDeleteRequest"/>
        </template>
    </Dialog>
</template>