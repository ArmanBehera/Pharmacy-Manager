<script setup>
    import router from '../../router';
    import { watch } from 'vue';
    import { ref, computed } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import '../../styles/styles.css';
    
    const store = useStore();
    store.dispatch('initializeStore');

    const items = ref([
        {
            label: 'Home',
            icon: 'pi pi-home',
            loggedIn: false,
            loggedOut: true,
            command: () => {
                router.push({ name: 'Home' })
            }
        },
        {
            label: 'Home',  
            icon: 'pi pi-home',
            loggedIn: true,
            loggedOut: false,
            command: () => {
                router.push({ name: 'DoctorHomePage' })
            }
        },
        {
            label: 'Signin',
            icon: 'pi pi-sign-in',
            loggedIn: false,
            loggedOut: true,
            command: () => {
                router.push({ name: 'DoctorSignin' })
            }
        },
        {
            label: 'Login',
            icon: 'pi pi-user',
            loggedIn: false,
            loggedOut: true,
            command: () => {
                router.push({ name: 'DoctorLogin' })
            }
        },
        {
            label: 'Logout',
            icon: 'pi pi-sign-out',
            loggedIn: true,
            loggedOut: false,
            command: () => {
                router.push({ name: 'Logout'})
            }
        }
    ]);

    const logged_in = computed(() => store.state.is_registered === 'true');

    const redirect = (urlName) => {
        router.push({ name: urlName})
        drawer_visible.value = false
    }
</script>

<template>
    <Menubar :model="items" class="mt-2">
        <template #item="{ item, props }">
            <a v-if="item.loggedIn == logged_in || item.loggedOut == !logged_in" :target="item.target" v-bind="props.action">
                <span :class="item.icon" />
                <span class="ml-2">{{ item.label }}</span>
            </a>
        </template>
        <template #end>
            <svg width="50" height="40">
                <image href="../../assets/Pharmacy.png" x="2" y="2" height="36" width="36"/>
            </svg>
        </template>
    </Menubar>
    <router-view/>
</template>