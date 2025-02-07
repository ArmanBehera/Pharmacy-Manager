<script setup>
    import axios from '../axios';
    import { onMounted } from 'vue';
    import { useStore } from 'vuex';
    import { ref } from 'vue';

    const message = ref('');

    const store = useStore()
    store.dispatch('initializeStore')
    
    if (store.state.is_registered === "true") {  
        const usertype = store.state.usertype

        axios.post('/logout/', 
        { 
            "refresh_token": localStorage.getItem('refresh_token')
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