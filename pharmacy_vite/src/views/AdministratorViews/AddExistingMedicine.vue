<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { checkDate, capitalize } from '../../helpers';
    import { format } from 'date-fns';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    const medicines_data = ref([]);
    const selected_medicine = ref();
    const medicine_name = ref();
    const is_loaded = ref([false]);
    
    const stock = ref();
    const expiration_date = ref();

    const is_registered = ref(store.state.is_registered)
    const usertype = store.state.usertype

    if (is_registered.value === 'true') {
        axios.get(`${usertype}/getMedicines/`)
        .then( (response) => {
            medicines_data.value = response.data
            is_loaded.value[0] = true
        })
        .catch( (error) => {
            warn('warn', 'Error getting medicines data.', 'Please check the status of the server or try reloading.')
        })
    } else {
        warn('warn', 'Please log in to access this page.', '');
    }

    const search = () => {

        if (!medicine_name.value) {
            warn('warn', 'Please fill in the name of the medicine to be searched for.', '');
            return;
        }

        axios.post(`/${usertype}/getMedicines/`, {
            'name': medicine_name.value
        })
        .then( (response) => {
            medicines_data.value = response.data
        })
        .catch( (error) =>{
            warn('warn', 'Error searching for the medicine with the given filter.', 'Please check the status of the server or try reloading.')
        })
    }

    const submit = () => {

        if (!selected_medicine.value.medicine.id || !stock.value || !expiration_date.value) {
            warn('warn', 'Please fill in all the fields.', '');
            return;
        }

        if (!checkDate(expiration_date))  {
            warn('warn', 'Error with expiration date.', 'Make sure the date is filled and is today or after today.');
            return;
        }

        axios.post(`${usertype}/addMedicineStock/`, {
            "id": selected_medicine.value.medicine.id,
            "stock": stock.value,
            "expiration_date": format(new Date(expiration_date.value), 'yyyy-MM-dd')  
        })
        .then( (response) => {
            warn('success', 'Successfully added stock for the medicine', '')
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in adding stock for the medicine', 'Please check the status of the server or try reloading.')
        })
    }
</script>

<template>
    <div class="flex flex-column align-items-center justify-content-center">
        <Toast/>
        <h1 class="text-3xl font-bold m-3">Add Existing Medicine</h1>
    </div>

    <div class="flex flex-row align-items-center justify-content-center">
        <InputText class="elements" id="medicine-name" placeholder="Medicine Name" v-model.trim="medicine_name"/>
        <Button id="search" label="Search" @click.prevent="search"/>
    </div>

    <div class="card m-10">
        <h1 class="text-l font-bold m-3">Select Medicine</h1>  
        <DataTable v-if="is_loaded[0] & medicines_data.length > 0" :value="medicines_data" datakey="id" removableSort :rows="3" paginator tableStyle="min-width: 22rem" v-model:selection="selected_medicine" >
            <Column selectionMode="single" headerStyle="width: 3rem"></Column>
            <Column field="medicine.name" header="Medicine Name" style="width: 40%" sortable></Column>
            <Column field="medicine.manufacturer" header="Manufacturer" style="width: 30%" sortable></Column>
            <Column field="medicine.price" header="Price" style="width: 20%;" sortable></Column>
        </DataTable>

        <div v-else-if="medicines_data.length == 0 && is_loaded[0]" class="centered placeholder-table" style="min-width: 20rem; padding:1rem">
            There are no medicines in this system.
        </div>

        <div class="centered" v-else>
            <ProgressSpinner/>
        </div>
    </div>

    <div class="top-container">
        <div class="container">
            <div class="sub-container">
                <InputNumber id="stock" placeholder="Stock *" inputId="withoutgrouping" :useGrouping="false" v-model.number="stock" :min="0" class="p-inputnumber-sm w-full"/>
                <DatePicker v-model="expiration_date" dateFormat="dd/mm/yy" placeholder="Expiration Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
            </div>

            <Button id="submit" label="Submit" @click.prevent="submit"/>
        </div>
    </div>
</template>