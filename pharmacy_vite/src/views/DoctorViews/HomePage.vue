<script setup>
    
    import axios from '../../axios';
    import { useStore } from 'vuex';

    const store = useStore();

    store.dispatch('initializeStore');
    
</script>

<template>
    
</template>