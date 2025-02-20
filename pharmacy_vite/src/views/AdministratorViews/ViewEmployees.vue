<script setup>
    import { ref } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const deletion_dialog = ref();
    const unverification_dialog = ref();

    const data = ref([]);
    const selected = ref();
    

    const store = useStore();
    store.dispatch('initializeStore');

    const is_registered = ref(store.state.is_registered)

    const toast = useToast();
    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    if (is_registered.value === "true") {
        axios.get('/administrator/getEmployees/')
        .then( (response) => {
            data.value = response.data
        })
        .catch( (error) => {
            warn('warn', "Log in using an admin account to access this page.", error);
        })
    }
    else {
        warn('warn', "Log in using an admin account to access this page.", error);
    }

    const confirmDeletion = () => {      
        deletion_dialog.value = true;
    }

    const confirmUnverification = () => {
        unverification_dialog.value = true;
    }

    const sendRequest = (code) => {
        deletion_dialog.value = false;
        unverification_dialog.value = false;
        let idArray = []

        for (let i = 0; i < selected.value.length; i++) {
            idArray.push(selected.value[i]['id'])
        }

        axios.post('/administrator/editEmployees/', { code: code, ids: idArray })
        .then( (response) => {
            warn('success', 'Successfully edited users!', '')
            
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })
        .catch( (error) => {
            warn('warn', 'Unsuccesful in editing users.', error)
        })
    }
</script>

<template>
    <Toast/>

    <div class="top-container mt-4" v-if="data.length >= 0">
        <div class="container">
            <div class="centered">
                <h1 class="text-3xl font-bold m-3">All Employees</h1>    
            </div>

            <div class="sub-container" style="margin-left:7rem;" v-if="data.length > 0">
                <div class="card">
                    <DataTable :value="data" v-model:selection="selected" datakey="id" removableSort paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem" resizableColumns columnResizeMode="fit">
                        <Column selectionMode="multiple" style="width: 3rem"></Column>
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 10%" sortable></Column>
                        <Column field="role" header="Role" style="width: 20%" sortable></Column>
                        <Column field="email" header="Email" style="width:40%" sortable></Column>
                        <Column field="is_verified" header="Verification Status" style="width: 10%" sortable></Column>
                    </DataTable>
                </div>
            </div>

            <div class="centered" v-if="data.length == 0">
                <h1 class="text-l font-bold m-2">There are no users in the system.</h1>
            </div>

            <div class="flex flex-row align-items-center justify-content-center mt-2">
                <div v-if="data.length > 0"> 
                    <Button label="Unverify Employees" icon="pi pi-trash" severity="danger" @click="confirmUnverification" :disabled="!selected || !selected.length"/>
                </div>

                <div v-if="data.length > 0"> 
                    <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeletion" class="ml-2" :disabled="!selected || !selected.length"/>
                </div>
            </div>
        </div>
    </div>

    <div v-else>
        <h1 class="text-3xl font-bold m-3">There are no employees in the system.</h1>
    </div>

    <Dialog v-model:visible="deletion_dialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to delete the selected users?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="deletion_dialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendRequest(0)"/>
        </template>
    </Dialog>

    <Dialog v-model:visible="unverification_dialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to unverify the selected users?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="unverification_dialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendRequest(1)"/>
        </template>
    </Dialog>

</template>