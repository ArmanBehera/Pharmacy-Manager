<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { convertDateFormat, checkToday } from '../../helpers'
    import router from '../../router';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();

    const warn = (summary, detailed) => {
        toast.add({ severity: 'warn', summary: summary, detail: detailed, life: 3000 });
    }
</script>

<template>
    <Toast/>
</template>