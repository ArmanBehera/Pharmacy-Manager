<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, computed, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { useRoute } from 'vue-router';

    const store = useStore();
    store.dispatch('initializeStore');
    const is_registered = ref(store.state.is_registered)

    const toast = useToast();
    const route = useRoute();

    const prescription_id = route.query.id

    if (is_registered.value === 'true') {

    }
</script>

<template>
    <Toast/>
</template>