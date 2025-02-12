<script setup>
    import { useStore } from 'vuex';
    import { useToast } from 'primevue/usetoast';
    import { ref } from 'vue';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { filled } from '../../helpers';

    const store = useStore();
    const toast = useToast();

    const name = ref('');
    const price = ref();
    const provider = ref('');
    const description = ref('');
    const sample_required = ref(''); // Get from backend
    const pre_test_requirements = ref(''); // Get from backend

    const is_registered = ref(store.state.is_registered)
    const usertype = store.state.usertype

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    if (is_registered.value === 'false') {
        warn('warn', 'Please log in to access this page.', '')
    }

    const submit = () => {
        
        let data = {}
        
        try {
            data = {
                'name': name.value,
                'test_cost': price.value,
                'provider': provider.value,
                'description': description.value ? description.value : '',
                'sample_required': sample_required.value,
                'pre_test_requirements': pre_test_requirements.value ? pre_test_requirements.value : ''
            }
        } catch (error) {
            warn("warn", "Required fields are not filled", "Please fill in all the required fields with appropriate values.")
            return;
        }

        const completed = filled(data, [])

        if (completed !== 'success') {
            warn('warn', completed + " required field is not filled", "Please fill in all the required fields with appropriate values.")
            return;
        }

        axios.post(`${usertype}/addLabTests/`, {
            ...data
        })
        .then( (response) => {
            warn('success', 'Successfully added new labtest.', '')
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in adding the labtest.', error)
        })
    }
</script>    

<template>
    <Toast />

    <div class="centered">
        <h1 class="text-3xl font-bold m-3">Add Lab Tests</h1>
    </div>

    <div class="flex flex-row align-items-center justify-content-center">
        <div class="flex flex-column mr-4">
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

        <div class="flex flex-column">
            <div class="flex flex-col space-y-4">
                <InputText id="sample-required" placeholder="Sample Required *" v-model.trim="sample_required" class="p-inputtext-sm w-full"/>
                
                <FloatLabel class="mt-4">
                    <Textarea v-model="pre_test_requirements" autoResize rows="5" cols="54" class="w-full" />
                    <label>Pre-Test Requirements</label>
                </FloatLabel>
            </div>
        </div>
    </div>

    <div class="flex justify-center mt-4">
        <Button label="Submit" @click.prevent="submit" class="p-button-lg" v-if="is_registered === 'true'"/>
        <Button label="Submit" @click.prevent="submit" class="p-button-lg" v-if="is_registered === 'false'" disabled/>
    </div>
</template>