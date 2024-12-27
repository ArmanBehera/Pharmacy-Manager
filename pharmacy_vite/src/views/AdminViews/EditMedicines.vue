
<script setup>
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    import axios from '../../axios'
    import { useStore } from 'vuex';
    import { useToast } from 'primevue/usetoast';

    const route = useRoute();
    const store = useStore();
    const toast = useToast();

    store.dispatch('initializeStore');

    const message = ref();
    const data = ref();
    const length = ref();

    const name = ref();
    const stock = ref();
    const price = ref();
    const manufacturer = ref('');
    const expiration_date = ref('');
    const description = ref('');

    const id = route.query.id;

    if (store.state.isRegistered === "true") {
        axios.get(`/administrator/editMedicines/?id=${id}`)
        .then( (response) => {
            data.value = response.data
            length.value = data.value.length
            
            name.value = response.data.name
            stock.value = response.data.stock
        })
        .catch( (error) => {
            message.value = "Log in using an admin or pharmacist account to access this page."
        })
    }
    else {
        message.value = "Log in using an admin or pharmacist account to access this page."
    }

    const submit = () => {

    }
</script>

<template>
    <Toast />

    <div class="centered">
        <h1 class="text-3xl font-bold m-3">{{ message }}</h1>
    </div>

    <div class="centered" v-if="!message">
        <h1 class="text-3xl font-bld m-3">Edit Medicines</h1>
    </div>

    <div class="container mx-auto p-6 bg-grey shadow-md rounded-lg">
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div class="flex flex-col space-y-4">
               <InputText id="Name" placeholder="Name *" v-model.trim="name" class="p-inputtext-sm w-full" />
                <InputNumber id="stock" placeholder="Stock *" inputId="withoutgrouping" :useGrouping="false" v-model.number="stock" :min="0" :allowEmpty="true" class="p-inputnumber-sm w-full" />
                <InputNumber id="price" placeholder="Price *" inputId="currency-india" mode="currency" currency="INR" currencyDisplay="code" locale="en-IN" v-model.number="price" :min="0" :allowEmpty="true" class="p-inputnumber-sm w-full" />
                <InputText id="Manufacturer" placeholder="Manufacturer" v-model.trim="manufacturer" class="p-inputtext-sm w-full" />
                <DatePicker v-model="expiration_date" dateFormat="dd/mm/yy" placeholder="Expiration Date" class="p-datepicker-sm w-full" />
                <FloatLabel class="mt-4">
                    <Textarea v-model="description" autoResize rows="5" cols="54" class="w-full" />
                    <label>Description</label>
                </FloatLabel>
            </div>
            {{ name }}
            <div class="flex flex-col space-y-6">
                <div class="flex flex-col space-y-4">
                    
                </div>

                <div class="flex flex-col space-y-4">
                    
                </div>
            </div>

            <div>
                <div class="flex flex-col space-y-4">
                    
                </div>

                <div class="flex flex-col space-y-4">
                    
                </div>    
            </div>
        </div>
        <div class="flex justify-center mt-4">
            <Button label="Submit" @click.prevent="submit" class="p-button-lg" />
        </div>
    </div>
</template>