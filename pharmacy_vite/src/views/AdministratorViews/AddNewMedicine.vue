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

    const ingredients_count = ref(1);
    const ingredients_data = ref([]);
    let selected_ingredients = ref([]);

    const allergens_count = ref(1);
    const allergens_data = ref([]);
    let selected_allergens = ref([]);

    const categories_count = ref(1);
    const categories_data = ref([]);
    let selected_categories = ref([]);

    const side_effects_count = ref(1);
    const side_effects_data = ref([]);
    let selected_side_effects = ref([]);

    const filtered_array = ref();

    const name = ref('');
    const stock = ref();
    const price = ref();
    const manufacturer = ref('');
    const expiration_date = ref();
    const description = ref('');

    const timings = ref('');
    const timings_choices = ref(['Before Food', 'After Food', 'Custom'])
    const custom_timing_description = ref('');

    const is_registered = ref(store.state.is_registered)
    const usertype = store.state.usertype
    
    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    if (is_registered.value === "true") {
        axios.get(`/${usertype}/addMedicines/`)
        .then((response) => {
            allergens_data.value = response.data.allergens
            ingredients_data.value = response.data.ingredients
            categories_data.value = response.data.categories
            side_effects_data.value = response.data.side_effects
        })
        .catch((error) => {
            warn('warn', 'Unsuccessful in getting data from the server.', error)
        })
    } else {
        warn('warn', 'Please log in with an appropriate account to access this page.', '');
    }

    const search = (event, fullArray) => {
        setTimeout(() => {
            if (!event.query.trim().length) {
                filtered_array.value = [...fullArray]
            } else {
                filtered_array.value = fullArray.filter((element) => {
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

        if (!timings.value) {
            warn('warn', 'Timings field should be filled with the timing at which the medicine should be taken.', '');
            return;
        }

        if (!checkDate(expiration_date)) {
            warn('Error with expiration date.', 'Make sure the date is filled and is today or after today.');
            return;
        }

        if (selected_allergens.value.length == 0) {
            warn('warn', 'Allergens should be filled.', '');
            return;
        }

        if (selected_side_effects.value.length == 0){
            warn('warn', 'Side Effects should be filled.', '');
            return;
        }

        const medicineToSend = {
            'name': name.value,
            'price': price.value,
            'description': description.value ? description.value : '',
            'manufacturer': manufacturer.value,
            'timings': timings.value,
            'side_effects' : selected_side_effects.value.map(sideEffect => ({ name: sideEffect.name ? sideEffect.name : sideEffect })),
            'allergens' : selected_allergens.value.map(allergy => ({ name: allergy.name ? allergy.name : allergy })),
            'timings': timings.value,
            'custom_timing_description': custom_timing_description.value
        }
        
        if (selected_ingredients.value.length != 0) {
            medicineToSend.ingredients = selected_ingredients.value.map(ingredient => ({ name: ingredient.name ? ingredient.name : ingredient }));
        } else {
            medicineToSend.ingredients = []
        }

        if (selected_categories.value.length != 0){
            const categoriesArray = [];

            for (let i = 0; i < categories_count.value; i++) {
                categoriesArray[i] = {
                    "name": selected_categories.value[i].name ? selected_categories.value[i].name : selected_categories.value[i],
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

        axios.post(`/${usertype}/addMedicines/`, requestToSend)
        .then( (response) => {
            warn('success', 'Successfully added medicine.', '')
            // Reload the page
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })  
        .catch( (error) => {
            warn('warn', 'Unsuccessful in adding medicine.', error)
        })
    }
</script>

<template>
    <Toast />

    <div class="centered" v-if="is_registered === 'true'">
        <h1 class="text-3xl font-bold m-3">Add Medicines</h1>
    </div>

    <div class="container mx-auto p-6 bg-grey shadow-md rounded-lg">
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div class="flex flex-col space-y-4">
                <InputText id="name" placeholder="Name *" v-model.trim="name" class="p-inputtext-sm w-full"/>
                <InputNumber id="stock" placeholder="Stock *" inputId="withoutgrouping" :useGrouping="false" v-model.number="stock" :min="0" class="p-inputnumber-sm w-full"/>
                <InputNumber id="price" placeholder="Price per unit*" inputId="currency-india" mode="currency" currency="INR" currencyDisplay="code" locale="en-IN" v-model.number="price" :min="0" class="p-inputnumber-sm w-full"/>
                <InputText id="manufacturer" placeholder="Manufacturer *" v-model.trim="manufacturer" class="p-inputtext-sm w-full"/>
                <DatePicker v-model="expiration_date" dateFormat="dd/mm/yy" placeholder="Expiration Date *" class="p-datepicker-sm w-full" showIcon fluid iconDisplay="input"/>
                <FloatLabel class="mt-4">
                    <Textarea v-model="description" autoResize rows="5" cols="54" class="w-full" />
                    <label>Description</label>
                </FloatLabel>
                <Select v-model="timings" :options="timings_choices" placeholder="Timing for taking the medicine *"/>
                <InputText id="customTiming" placeholder="Custom Timing Description *" v-model.trim="custom_timing_description" v-if="timings === 'Custom'" class="p-inputtext-sm w-full"/>
            </div>

            <div class="flex flex-col space-y-6">
                <div class="flex flex-col space-y-4">
                    <label class="font-semibold">Ingredients</label>
                    <div v-for="n in ingredients_count" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Ingredient ${n}`" v-model="selected_ingredients[n - 1]" optionLabel="name" dropdown :suggestions="filtered_array" @complete="(event) => search(event, ingredients_data)" class="w-full" />
                    </div>
                    <Button label="Add Ingredient" @click.prevent="ingredients_count += 1" class="p-button-sm" />
                </div>

                <div class="flex flex-col space-y-4">
                    <label class="font-semibold">Allergens</label>
                    <div v-for="n in allergens_count" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Allergy ${n}*`" v-model="selected_allergens[n - 1]" optionLabel="name" dropdown :suggestions="filtered_array" @complete="(event) => search(event, allergens_data)" class="w-full" />
                    </div>
                    <Button label="Add Allergy" @click.prevent="allergens_count += 1" class="p-button-sm" />
                </div>
            </div>

            <div>
                <div class="flex flex-col space-y-4">
                    <label class="font-semibold">Categories</label>
                    <div v-for="n in categories_count" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Use ${n}*`" v-model="selected_categories[n - 1]" optionLabel="name" dropdown :suggestions="filtered_array" @complete="(event) => search(event, categories_data)" class="w-full" />
                    </div>
                    <Button label="Add Use" @click.prevent="categories_count += 1" class="p-button-sm" />
                </div>

                <div class="flex flex-col space-y-4">
                    <label class="font-semibold mt-4">Side Effects</label>
                    <div v-for="n in side_effects_count" :key="n" class="flex items-center space-x-4">
                        <AutoComplete :placeholder="`Side Effect ${n}*`" v-model="selected_side_effects[n - 1]" optionLabel="name" dropdown :suggestions="filtered_array" @complete="(event) => search(event, side_effects_data)" class="w-full" />
                    </div>
                    <Button label="Add Side Effect" @click.prevent="side_effects_count += 1" class="p-button-sm" />
                </div>
            </div>
        </div>
        <div class="flex justify-center mt-4">
            <Button label="Submit" @click.prevent="submit" class="p-button-lg" v-if="is_registered === 'true'"/>
            <Button label="Submit" @click.prevent="submit" class="p-button-lg" v-if="is_registered === 'false'" disabled/>
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