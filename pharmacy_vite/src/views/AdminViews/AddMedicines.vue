<script setup>
    import { useStore } from 'vuex';
    import { useToast } from 'primevue/usetoast';
    import { ref } from 'vue';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { addSeconds, format } from 'date-fns';

    const store = useStore();
    const toast = useToast();

    const message = ref('');

    const ingredientsCount = ref(1);
    const ingredientsData = ref([]);
    let selectedIngredients = ref([]);

    const allergensCount = ref(1);
    const allergensData = ref([]);
    let selectedAllergens = ref([]);

    const categoriesCount = ref(1);
    const categoriesData = ref([]);
    let selectedCategories = ref([]);

    const sideEffectsCount = ref(1);
    const sideEffectsData = ref([]);
    let selectedSideEffects = ref([]);

    const filteredArray = ref();

    const name = ref('');
    const stock = ref();
    const price = ref();
    const manufacturer = ref('');
    const expiration_date = ref('');
    const description = ref('');
    
    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    if (store.getters.isRegistered) { 
        const usertype = store.getters.getUserDetails['usertype']
        if (usertype === 'administrator' || usertype === 'pharmacy') {
            axios.get('/administrator/addMedicines/')
            .then((response) => {
                allergensData.value = response.data.allergens
                ingredientsData.value = response.data.ingredients
                categoriesData.value = response.data.categories
                sideEffectsData.value = response.data.sideEffects
            })
            .catch((error) => {
                warn('warn', 'Unsuccessful in getting data from the server.', 'Please try again.')
            })
        } else {
            message.value = "Log in using an admin or pharmacist account to access this page."
        }
    }

    const search = (event, fullArray) => {
        setTimeout(() => {
            if (!event.query.trim().length) {
                filteredArray.value = [...fullArray]
            } else {
                filteredArray.value = fullArray.filter((element) => {
                    return element.name.toLowerCase().startsWith(event.query.toLowerCase());
                });
            }
        }, 50);
    }

    const submit = () => {

        if (!name.value){
            warn('warn', 'Name field should be filled with the name of the medicine.', '');
            return;
        }

        if (!stock.value){
            warn('warn', 'Stock field should be filled with an appropriate value.', '');
            return;
        }

        if (!price.value){
            warn('warn', 'Price field should be filled with an appropriate value.', '');
            return;
        }

        if (!manufacturer.value){
            warn('warn', 'Manufacturer field should be filled with the name of the manufacturer.', '');
            return;
        }

        if (!expiration_date.value) {
            warn('warn', 'Date of expiry should be filled.', '');
            return;
        } else {
            const expirationDate = new Date(expiration_date.value);

            const currentDate = new Date();
            currentDate.setHours(0, 0, 0, 0);

            if (expirationDate < currentDate) {
                warn('warn', 'Expiration date is already past.', 'Please set the expiration date on a date after today.')
                return;
            }
        }

        if (selectedAllergens.value.length == 0) {
            warn('warn', 'Allergens should be filled.', '');
            return;
        }

        if (selectedSideEffects.value.length == 0){
            warn('warn', 'Side Effects should be filled.', '');
            return;
        }

        const medicineToSend = {
            "name": name.value,
            "price": price.value,
            "description": description.value ? description.value : '',
            "manufacturer": manufacturer.value,
            "sideEffects" : selectedSideEffects.value.map(sideEffect => ({ name: sideEffect.name ? sideEffect.name : sideEffect })),
            "allergens" : selectedAllergens.value.map(allergy => ({ name: allergy.name ? allergy.name : allergy })),
        }
        
        if (selectedIngredients.value.length != 0) {
            medicineToSend.ingredients = selectedIngredients.value.map(ingredient => ({ name: ingredient.name ? ingredient.name : ingredient }));
        }

        if (selectedCategories.value.length != 0){
            const categoriesArray = [];

            for (let i = 0; i < categoriesCount.value; i++) {
                categoriesArray[i] = {
                    "name": selectedCategories.value[i].name ? selectedCategories.value[i].name : selectedCategories.value[i],
                    "usage_priority": (i + 1)
                };
            }

            medicineToSend.categories = categoriesArray
        } else {
            warn('warn', 'Categories should be filled.', '');
            return;
        }

        const requestToSend = {
            "medicine" : medicineToSend,
            "stock": stock.value,
            "expiration_date" : format(new Date(expiration_date.value), 'yyyy-MM-dd')
        }

        axios.post('/administrator/addMedicines/', requestToSend)
        .then( (response) => {
            warn('success', 'Successfully added medicine.', '')
            
            // Reload the page
            setTimeout(() => {
                window.location.reload();
            }, 3000);
        })  
        .catch( (error) => {
            warn('warn', 'Unsuccessful in adding medicine.', 'Please try again in some time.')
        })
    }
</script>

<template>
    <Toast />

    <div class="centered">
        <h1 class="text-3xl font-bold m-3">{{ message }}</h1>
    </div>

    <div class="centered" v-if="!message">
        <h1 class="text-3xl font-bld m-3">Add Medicines</h1>
    </div>

    <div class="container mx-auto p-6 bg-grey shadow-md rounded-lg">
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div class="flex flex-col space-y-4">
                <InputText id="Name" placeholder="Name *" v-model.trim="name" class="p-inputtext-sm w-full"/>
                <InputNumber id="stock" placeholder="Stock *" inputId="withoutgrouping" :useGrouping="false" v-model.number="stock" :min="0" class="p-inputnumber-sm w-full"/>
                <InputNumber id="price" placeholder="Price *" inputId="currency-india" mode="currency" currency="INR" currencyDisplay="code" locale="en-IN" v-model.number="price" :min="0" class="p-inputnumber-sm w-full"/>
                <InputText id="Manufacturer" placeholder="Manufacturer *" v-model.trim="manufacturer" class="p-inputtext-sm w-full"/>
                <DatePicker v-model="expiration_date" dateFormat="dd/mm/yy" placeholder="Expiration Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
                <FloatLabel class="mt-4">
                    <Textarea v-model="description" autoResize rows="5" cols="54" class="w-full" />
                    <label>Description</label>
                </FloatLabel>
            </div>

            <div class="flex flex-col space-y-6">
                <div class="flex flex-col space-y-4">
                    <label class="font-semibold">Ingredients</label>
                    <div v-for="n in ingredientsCount" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Ingredient ${n}`" v-model="selectedIngredients[n - 1]" optionLabel="name" dropdown :suggestions="filteredArray" @complete="(event) => search(event, ingredientsData)" class="w-full" />
                    </div>
                    <Button label="Add Ingredient" @click.prevent="ingredientsCount += 1" class="p-button-sm" />
                </div>

                <div class="flex flex-col space-y-4">
                    <label class="font-semibold">Allergens</label>
                    <div v-for="n in allergensCount" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Allergy ${n}*`" v-model="selectedAllergens[n - 1]" optionLabel="name" dropdown :suggestions="filteredArray" @complete="(event) => search(event, allergensData)" class="w-full" />
                    </div>
                    <Button label="Add Allergy" @click.prevent="allergensCount += 1" class="p-button-sm" />
                </div>
            </div>

            <div>
                <div class="flex flex-col space-y-4">
                    <label class="font-semibold">Categories</label>
                    <div v-for="n in categoriesCount" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Use ${n}*`" v-model="selectedCategories[n - 1]" optionLabel="name" dropdown :suggestions="filteredArray" @complete="(event) => search(event, categoriesData)" class="w-full" />
                    </div>
                    <Button label="Add Use" @click.prevent="categoriesCount += 1" class="p-button-sm" />
                </div>

                <div class="flex flex-col space-y-4">
                    <label class="font-semibold mt-4">Side Effects</label>
                    <div v-for="n in sideEffectsCount" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Side Effect ${n}*`" v-model="selectedSideEffects[n - 1]" optionLabel="name" dropdown :suggestions="filteredArray" @complete="(event) => search(event, sideEffectsData)" class="w-full" />
                    </div>
                    <Button label="Add Side Effect" @click.prevent="sideEffectsCount += 1" class="p-button-sm" />
                </div>    
            </div>
        </div>
        <div class="flex justify-center mt-4">
            <Button label="Submit" @click.prevent="submit" class="p-button-lg" />
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 1200px;
}

.sub-container {
    margin-bottom: 1rem;
}

.vertical-divide {
    margin: 0 1rem;
}

.flex-col > .sub-container {
    margin-bottom: 0;
}

.p-button-sm {
    width: auto;
    margin-top: 0.5rem;
}

.p-button-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1.1rem;
}
</style>