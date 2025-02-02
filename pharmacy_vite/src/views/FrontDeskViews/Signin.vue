<script setup>
    // to add fields: specialization
    import { onBeforeMount, ref } from 'vue';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import router from '../../router' 
    import { useToast } from 'primevue/usetoast';
    import { onMounted, onBeforeUnmount } from 'vue';
    import { useStore } from 'vuex';

    const store = useStore();
    store.dispatch('logout')

    const toast = useToast();

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 5000 });
    }

    const visibility = ref(true);

    const updateVisibility = () => {
        if (window.innerWidth < 800) {
            visibility.value = false;
        }
        if (window.innerWidth >= 800) {
            visibility.value = true;
        }
    }

    onMounted(() => {
        window.addEventListener('resize', updateVisibility);
        updateVisibility();
    });

    onBeforeUnmount(() => {
        window.removeEventListener('resize', updateVisibility);
    });

    const first_name = ref('');
    const last_name = ref('');
    const primary_phone_number = ref('');
    const secondary_phone_number = ref('');
    const email = ref('');
    const password = ref('');
    const confirm_password = ref('');
    const age = ref();
    const gender = ref('');
    const gender_choices = ref([
        {gender: 'Male'},
        {gender: 'Female'}, 
        {gender: 'Other'}
    ]);

    const submit = () => {
        let data = {
            'first_name': first_name.value,
            'last_name': last_name.value,
            'primary_phone_number': primary_phone_number.value,
            'email': email.value,
            'password': password.value,
            'age': age.value,
            'gender': gender.value['gender'],
            'secondary_phone_number': secondary_phone_number.value? secondary_phone_number.value : '0',
        };

        if (data.password !== confirm_password.value) {
            warn("Passwords do not match!", "Password and confirmation password do not match. Ensure that they are the same.");
            return;
        }

        var filled = true;

        // Checks for any empty fields
        // Do not have to check for null fields since .trim() function already handles undefined values
        for (const key in data) {
            const value = data[key];
            if (key !== 'secondary_phone_number'){
                if (typeof value === 'string' && value.trim() === '') {
                    filled = false;
                    break; // Exit the loop early if an empty field is found
                } else if (typeof value === 'number' && value === 0) {
                    filled = false;
                    break; // Exit the loop early if a zero value is found
                }
            }
        }

        // If there's any field left out - All fields need to be filled
        if (!filled) {
            warn("Required fields are not filled", "Please fill in all the required fields with appropriate values.")
        }
        // No errors - Sending message to the backend to be processed
        else {
            // Debug this part - Showing internal server error
            axios.post('/frontdesk/signin/', {
                ...data,
                "username": `${data.first_name}${data.last_name}`,
                "role": "FrontDesk",
                "is_verified": false,
                "occupation": "Employee",
                "is_staff": true,
                "is_active": true,
                "is_superuser": false
            })
            .then( (response) => {
                router.push({ name: 'FrontDeskLogin' })
            })
            .catch( (error) => {
                warn("Failed to create a new front desk user.")
            })
        }
    }
</script>

<template>
    <div class="flex align-items-center justify-content-center">
        <Toast/>
        <h1 class="text-3xl font-bold m-3">Sign In</h1>
    </div>

    <div class="top-container">
        <div class="container">
            <div class="sub-container">
                <InputText class="elements" id="first-name" placeholder="First Name*" v-model.trim="first_name"/>
                <InputText class="elements" id="last-name" placeholder="Last Name*" v-model.trim="last_name"/>
            </div>

            <div class="sub-container">
                <InputText class="elements" id="primary-phone-number" placeholder="Primary Phone Number*" v-model.trim="primary_phone_number"/>
                <InputText class="elements" id="secondary-phone-number" placeholder="Secondary Phone Number" v-model.trim="secondary_phone_number"/>
            </div>

            <div class="sub-container">
                <InputText class="elements" id="email-id" placeholder="Email ID*" v-model.trim="email"/>
            </div>
            <div class="sub-container">
                <CustomPassword class="elements" placeholder="Password*" v-model.trim="password"/>
            </div>

            <div class="sub-container">
                <CustomPassword class="elements" placeholder="Confirm Password*" v-model.trim="confirm_password"/>
            </div>

            <div class="sub-container">
                <InputNumber class="elements" id="age" placeholder="Age*" inputId="withoutgrouping" :useGrouping="false" v-model.number="age" :min="0" :max="100" :allowEmpty="true"/>
                <Select class="elements" id="gender" v-model.trim="gender" :options="gender_choices" optionLabel="gender" placeholder="Gender*" showClear/>
            </div>
        </div>

        <div class="vertical-divide" v-show="visibility"></div>

        <div class="container" v-show="visibility">
            <img alt="injection-image" src="../../assets/Injection.png"/>
            <div class="sub-container">
                <span class="quote">"Medicine is not only a science; it is also an art. It does not consist of compounding pills and plasters; it deals with the very processes of life, which must be understood before they may be guided." - Paracelsus</span>
            </div>
        </div>
    </div>
    <Button id="submit" label="Submit" @click.prevent="submit"/>
</template>
