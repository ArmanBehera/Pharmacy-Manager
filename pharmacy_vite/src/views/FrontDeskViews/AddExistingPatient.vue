<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { FilterMatchMode } from '@primevue/core/api';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 3000 });
    }

    const patientsData = ref([]);
    const isLoaded = ref([false]);
    const selectedPatient = ref();

    const filters = ref({
        name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
    })

    if (store.state.isRegistered) {
        axios.get('/frontdesk/getPatients')
        .then( (response) => {
            patientsData.value = response.data.map(patient => ({
                ...patient,
                name: `${patient.first_name} ${patient.last_name}`
            }));
            isLoaded.value[0] = true;
        })
        .catch( (error) => {
            warn("Error getting patients data.", "Please check the status of the server or try reloading.")
        })
    }
</script>

<template>
    <div class="flex flex-column align-items-center justify-content-center">
        <Toast/>
        <h1 class="text-3xl font-bold m-3">Add Existing Patient</h1>

        <div class="card centered" style="width: 80%; max-width: 600px;">
            
            <DataTable v-if="isLoaded[0] && patientsData.length > 0" :value="patientsData"
                datakey="id" v-model:selection="selectedPatient" removableSort :rows="7" paginator
                v-model:filters="filteredArray" filterDisplay="row" :globalFilterFields="['name']">
                <template #header>
                    <div class="flex justify-end">
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText v-model="filters['name'].value" placeholder="Keyword Search"/>
                        </IconField>
                    </div>
                </template>
                <template #empty>
                     No patients found.
                     <Button label="Add New Patient" icon="pi pi-external-link"  iconPos="right" @click="$router.push({ name: 'AddNewPatient' })" style="margin: 0.5rem"/> 
                </template>
                <template #loading> Loading patients data. Please wait. </template>
                
                <Column field="name" header="Name" sortable>
                    <template #body="{ data }">
                        {{ data.name }}
                    </template>
                    <template #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" @input="filterCallback()" placeholder="Search by name" />
                    </template>
                </Column>
                <Column field="age" header="Age" sortable>
                    <template #body="{ data } ">
                        {{  data.age }}
                    </template>
                </Column>
                <Column field="last_appointment_date" header="Last Appointment Date" sortable>
                    <template #body="{ data } ">
                        {{  data.last_appointment_date }}
                    </template>
                </Column>
            </DataTable>

            <div v-else-if="patientsData.length === 0 && isLoaded[0]" class="text-center" style="padding: 1rem;">
                <p>There are no scheduled patients in this system.</p>
            </div>

            <div v-else class="flex justify-content-center" style="padding: 2rem;">
                <ProgressSpinner/>
            </div>
        </div>
    </div>
</template>