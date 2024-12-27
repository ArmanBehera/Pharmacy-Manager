<script setup>
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import '../../styles/styles.css';

    const data = ref(['1'])
    const length = ref(-1) // Length of the data 

    const message = ref();
    const selected = ref();

    const verificationDialog = ref();
    const deletionDialog = ref();

    const store = useStore();
    store.dispatch('initializeStore');
    const toast = useToast();

    if (store.getters.isRegistered){
        axios.get('/administrator/verifyEmployees/')
        .then( (response) => {
            data.value = response.data
            length.value = data.value.length
        })
        .catch( (error) => {
            message.value = "Log in using an admin account to access this page."
        })
    }
    else {
        message.value = "Log in using an admin account to access this page."
    }

    const confirmVerification = () => {
        verificationDialog.value = true;
    }

    const confirmDeletion = () => {
        deletionDialog.value = true;
    }

    const sendRequest = (code) => {

        verificationDialog.value = false;
        deletionDialog.value = false;
        let idArray = []

        for (let i = 0; i < selected.value.length; i++) {
            idArray.push(selected.value[i]['id'])
        }

        axios.post("/administrator/verifyEmployees/", { code: code, ids: idArray })
        .then( (response) => {
            data.value = data.value.filter(val => !selected.value.includes(val));
            selected.value = null;

            if (code == 0){
                toast.add({severity:'success', summary: 'Successfully verified users!', life: 3000});
            } else {
                toast.add({severity:'success', summary: 'Successfully deleted users!', life: 3000});
            }
        })
        .catch( (error) => {
            if (code == 0){
                toast.add({severity:'warn', summary: 'Unsuccesful in verifying users.', message: 'Please try again.', life:3000});
            } else {
                toast.add({severity:'warn', summary: 'Unsuccesful in deleting users.', message: 'Please try again.', life:3000});
            }
        })
    }
</script>

<template>
    <Toast/>

    <div class="centered">
        <h1 class="text-3xl font-bold m-3"> {{ message }}</h1>
    </div>
    
    <div class="top-container">
        
        <div class="container">
            <div class="centered" v-if="length > 0">
                <h1 class="text-xl font-bold m-2">Verify Employees</h1>
            </div>
            <div class="sub-container" style="margin-left:7rem;" v-if="length != 0">
                <div class="card">
                    <DataTable :value="data" v-model:selection="selected" datakey="id" removableSort paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem" resizableColumns columnResizeMode="fit" >
                        
                        <Column selectionMode="multiple" style="width: 3rem"></Column>
                        <Column field="first_name" header="First Name" style="width: 20%" sortable></Column>
                        <Column field="last_name" header="Last Name" style="width: 20%" sortable></Column>
                        <Column field="role" header="Role" style="width: 20%" sortable></Column>
                        <Column field="email" header="Email" style="width:50%" sortable></Column>
                    </DataTable>
                </div>
            </div>
            <div class="centered" v-if="length == 0">
                <h1 class="text-l font-bold m-2">All users are verified!</h1>
            </div>
            
            <div class="sub-container" v-if="length > 0"> 
                <Button label="Verify" icon="pi pi-check-circle" severity="success" @click="confirmVerification" style="margin-left: 25rem; margin-top: 3rem;" :disabled="!selected || !selected.length"/>
                <Button label="Delete" icon="pi pi-trash" severity="danger" @click="confirmDeletion" style="margin-left: 2rem; margin-top: 3rem;" :disabled="!selected || !selected.length"/>
            </div>    
        </div>
    </div>

    <Dialog v-model:visible="verificationDialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to verify the selected users?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="verificationDialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendRequest(0)"/>
        </template>
    </Dialog>

    <Dialog v-model:visible="deletionDialog" :style="{ width: '450px' }" header="Confirm">
        <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span>Are you sure you want to delete the selected users?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="deletionDialog = false"/>
            <Button label="Yes" icon="pi pi-check" text @click="sendRequest(1)"/>
        </template>
    </Dialog>
</template>