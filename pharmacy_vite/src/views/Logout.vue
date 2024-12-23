<script setup>
    import axios from '../axios';
    import { onMounted } from 'vue';
    import { useStore } from 'vuex';
    import { ref } from 'vue';

    const message = ref('');

    onMounted (() => {
        const store = useStore()
        if (store.getters.isRegistered === true){ 
            const usertype = store.getters.getUserDetails['usertype']
            const url = '/' + usertype + '/logout/'

            axios.post(url, 
            { 
                "logout" : true,
            }, 
            {
                withCredentials: true
            })
            .then( (response) => {
                store.dispatch('logout')
                message.value = "Logout successful!"
            })
            .catch( (error) => {
                message.value = "Logout unsuccessful!"
                console.log(error);
            })
        }
    })
</script>

<template>
    <div class="centered">
        <h1>{{ message }}</h1>
    </div>

    <div class="centered">
        <Button label="small" class="routerlink" @click="$router.push({ name: 'Home' })">Home Page</Button>
    </div>
</template>