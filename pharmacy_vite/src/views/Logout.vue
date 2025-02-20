<script setup>
    import axios from '../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';

    const message = ref('');

    const store = useStore()
    store.dispatch('initializeStore')
    
    if (store.state.is_registered === "true") {  
        axios.post('/logout/', 
        { 
            "refresh_token": localStorage.getItem('refresh_token')
        }).then( (response) => {
            store.dispatch('logout')
            message.value = "Logout successful!"
        }).catch( (error) => {
            message.value = "Logout unsuccessful!"
        })
    } else {
        message.value = "Logout unsuccesful! Log in first to log out."
    }
</script>

<template>
    <div class="flex flex-column align-items-center justify-content-center mt-4">
        <h1>{{ message }}</h1>
        <Button label="small" class="routerlink" @click="$router.push({ name: 'Home' })">Home Page</Button>
    </div>
</template>