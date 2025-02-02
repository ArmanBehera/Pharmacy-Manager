<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { useToast } from 'primevue/usetoast';
    import router from '../../router' 
    
    const first_name = ref('');
    const last_name = ref('');
    const password = ref('');
    const confirm_password = ref('');

    const store = useStore();
    store.dispatch('logout');

    const toast = useToast();

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

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 5000 });
    }

    const submit = () => {

        let data = {}
        try {
            data = {
                first_name: first_name.value,
                last_name: last_name.value,
                password: password.value,
            }
        }
        catch (err) {
            warn("Required fields are not filled!", "Please fill in all the required fields with appropriate values.");
            return;
        }
        

        let filled = true;

        if (data.password !== confirm_password.value){
            warn("Passwords do not match!", "Password and confirmation password do not match. Ensure that they are the same.")
            return;
        }

        for (const key in data) {
            
            const value = data[key];
            if (typeof value === 'string' && value.trim() === '') {
                filled = false;
                break; // Exit the loop early if an empty field is found
            } else if (typeof value === 'number' && value === 0) {
                filled = false;
                break; // Exit the loop early if a zero value is found
            }
        }

        if (!filled){
            warn("Required fields are not filled!", "Please fill in all the required fields with appropriate values.");
        }
        else {
            axios.post("/api/v1/jwt/create/", {
                
                "username": `${data.first_name}${data.last_name}`,
                "password": data.password,
                'role': 'Pharmacy'
            })
            .then( (response) => {
                store.dispatch('setLoginDetails', {
                    'usertype': 'pharmacy',
                    'is_registered': true,
                    'refresh_token': response.data.refresh,
                    'access_token': response.data.access,
                    'first_name': data.first_name,
                    'last_name': data.last_name,
                    'user_id': response.data.user_id
                });
                router.push({ name: 'PharmacyHomePage' })
            })
            .catch( (error) => {
                warn("Unauthorized credentials!", "Invalid username/password or unauthorized by the admin. Contact admin for further details.");
            })
        }
    };
</script>

<template>
    
    <div class="flex align-items-center justify-content-center">
        <Toast/>
        <h1 class="text-3xl font-bold m-3">Login</h1>
    </div>

    <div class="top-container">
        <div class="container">
            <div class="sub-container">
                <InputText class="elements" id="first-name" placeholder="First Name" v-model.trim="first_name"/>
                <InputText class="elements" id="last-name" placeholder="Last Name" v-model.trim="last_name"/>
            </div>

            <div class="sub-container">
                <CustomPassword class="elements" placeholder="Password" v-model.trim="password"/>
            </div>
            
            <div class="sub-container">
                <CustomPassword class="elements" placeholder="Confirm Password" v-model.trim="confirm_password"/>
            </div>

            <Button label="Submit" @click.prevent="submit"/>
            <br>
            Need to make a new account?<router-link class="underline" :to="{ name: 'DoctorSignin'}">Sign In</router-link>
        </div>

        <div class="vertical-divide" v-show="visibility"></div>

        <div class="container" v-show="visibility">
            <div class="sub-container">
                <span class="quote">"Medicine is not only a science; it is also an art. It does not consist of compounding pills and plasters; it deals with the very processes of life, which must be understood before they may be guided." - Paracelsus</span>
            </div>
        </div>
    </div>
</template>