<script setup>
    import router from '../../router';
    import { watch } from 'vue';
    import { ref, computed } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import '../../styles/styles.css';
    
    const store = useStore();
    const drawerVisible = ref(false);

    store.dispatch('initializeStore');

    const items = ref([
        {
            label: '',
            icon: 'pi pi-bars',
            loggedIn: true,
            loggedOut: false,
            command: () => {
                drawerVisible.value = true;
            }
        },
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

    const loggedIn = computed(() => store.state.isRegistered === 'true');

    const redirect = (urlName) => {
        router.push({ name: urlName})
        drawerVisible.value = false
    }
</script>

<template>
    <Drawer v-model:visible="drawerVisible">
        <template #container="{ closeCallback }">
            <div class="flex flex-col h-full">
                <div class="flex items-center justify-between px-3 py-4 shadow-md">
                    <div class="inline-flex items-center gap-4">
                        <img src="../../assets/Pharmacy.png" alt="Pharmacy Logo" class="h-10 w-10" />
                        <h1 class="font-bold text-2xl text-primary">Doctor</h1>
                    </div>
                    <Button type="button" @click="closeCallback" icon="pi pi-times" rounded outlined></Button>
                </div>
            </div>
        </template>
    </Drawer>

    <Menubar :model="items">
        <template #item="{ item, props }">
            <a v-if="item.loggedIn == loggedIn || item.loggedOut == !loggedIn" :target="item.target" v-bind="props.action">
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