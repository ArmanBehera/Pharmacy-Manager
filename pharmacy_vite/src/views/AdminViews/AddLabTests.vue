<script setup>
    import { useStore } from 'vuex';
    import { useToast } from 'primevue/usetoast';
    import { ref } from 'vue';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { format } from 'date-fns';
    import { checkDate } from '../../helpers';

    const store = useStore();
    const toast = useToast();

    const name = ref('');
    const price = ref();
    const provider = ref('');
    const description = ref('');
    const sample_required = ref(''); // Get from backend
    const pre_test_requirements = ref(''); // Get from backend

    const isRegistered = ref(store.state.isRegistered)

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    if (isRegistered.value === 'true') {
        warn('warn', 'Please log in to access this page.', '')
    }

    const submit = () => {
        const data = {
            'name': name.value,
            'price': price.value,
            'provider': provider.value,
            'description': description.value
        }


    }
</script>    

<template>
    <Toast />

    <div class="centered" v-if="isRegistered === 'true'">
        <h1 class="text-3xl font-bld m-3">Add Lab Tests</h1>
    </div>

    <div class="flex flex-column align-items-center justify-content-center">
        <div class="flex flex-column">
            <div class="flex flex-col space-y-4">
                <InputText id="name" placeholder="Test Name *" v-model.trim="name" class="p-inputtext-sm w-full"/>
                <InputNumber id="price" placeholder="Price *" inputId="currency-india" mode="currency" currency="INR" currencyDisplay="code" locale="en-IN" v-model.number="price" :min="0" class="p-inputnumber-sm w-full"/>
                <InputText id="provider" placeholder="Provider *" v-model.trim="provider" class="p-inputtext-sm w-full"/>
                
                <FloatLabel class="mt-4">
                    <Textarea v-model="description" autoResize rows="5" cols="54" class="w-full" />
                    <label>Description</label>
                </FloatLabel>
            </div>
        </div>

        <div class="flex justify-center mt-4">
            <Button label="Submit" @click.prevent="submit" class="p-button-lg" v-if="isRegistered === 'true'"/>
            <Button label="Submit" @click.prevent="submit" class="p-button-lg" v-if="isRegistered === 'false'" disabled/>
        </div>
    </div>
</template>