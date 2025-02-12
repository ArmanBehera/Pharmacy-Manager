<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { useToast } from 'primevue/usetoast';
    import router from '../../router' 
    import '../../styles/styles.css';
    import { filled } from '../../helpers';
    
    const first_name = ref('');
    const last_name = ref('');
    const password = ref('');
    const confirm_password = ref('');

    const store = useStore();
    store.dispatch('logout')

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
                password: password.value
            }
        }
        catch (err) {
            warn('Required fields are not filled!', 'Please fill in all the required fields with appropriate values.');
            return;
        }

        if (data.password !== confirm_password.value){
            warn('Passwords do not match!', 'Password and confirmation password do not match. Ensure that they are the same.')
            return;
        }

        let completed = filled(data, [])

        if (completed !== 'success') {
            warn(completed + " required field is not filled", "Please fill in all the required fields with appropriate values.")
            return;
        }

        axios.post('/api/v1/jwt/create/', {
            
            'username': `${data.first_name}${data.last_name}`,
            'password': data.password,
            'role': 'Administrator'
        })
        .then( (response) => {

            store.dispatch('setLoginDetails', {
                'usertype': 'administrator',
                'is_registered': true,
                'refresh_token': response.data.refresh,
                'access_token': response.data.access,
                'user_id': response.data.user_id,
                'first_name': data.first_name,
                'last_name': data.last_name,
            });
            router.push({ name: 'AdministratorHomePage' });
        })
        .catch( (error) => {
            warn('Unauthorized credentials!', error);
        })
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
        </div>

        <div class="vertical-divide" v-show="visibility"></div>

        <div class="container" v-show="visibility">
            <div class="sub-container">
                <span class="quote">"Medicine is not only a science; it is also an art. It does not consist of compounding pills and plasters; it deals with the very processes of life, which must be understood before they may be guided." - Paracelsus</span>
            </div>
        </div>
    </div>
</template>