<script setup>
    import router from '../../router';
    import { watch } from 'vue';
    import { ref, computed } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import '../../styles/styles.css';
    
    const store = useStore();
    const drawerVisible = ref(false);
    const dropdownAppointments = ref();

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
                router.push({ name: 'FrontDeskHomePage' })
            }
        },
        {
            label: 'Signin',
            icon: 'pi pi-sign-in',
            loggedIn: false,
            loggedOut: true,
            command: () => {
                router.push({ name: 'FrontDeskSignin' })
            }
        },
        {
            label: 'Login',
            icon: 'pi pi-user',
            loggedIn: false,
            loggedOut: true,
            command: () => {
                router.push({ name: 'FrontDeskLogin' })
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

    const toggleDropdownAppointments = () => {
        dropdownAppointments.value = !dropdownAppointments.value
    }

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
                        <h1 class="font-bold text-2xl text-primary">Frontdesk</h1>
                    </div>
                    <Button type="button" @click="closeCallback" icon="pi pi-times" rounded outlined></Button>
                </div>

                <div class="overflow-y-auto">
                    <ul class="list-none p-4 m-0">
                        <li>
                            <a
                                @click="toggleDropdownAppointments"
                                class="flex items-center cursor-pointer p-4"
                            >
                                <i class="pi pi-chart-line mr-2"></i>
                                <span class="font-medium">Manage Appointments</span>
                                <i class="pi pi-chevron-down ml-auto transform transition-transform duration-600" :class="{ 'rotate-180': dropdownAppointments }"></i>
                            </a>
                            <ul v-show="dropdownAppointments" class="list-none py-0 pl-4 pr-0 m-0 overflow-y-hidden transition-all duration-[400ms] ease-in-out">
                                <li> 
                                    <a 
                                        class="flex items-center cursor-pointer p-4"
                                        @click="redirect('AddNewPatient')"
                                    >
                                        
                                        <i class="pi pi-eye mr-4"></i>
                                        <span class="font-medium">Add New Patient</span>
                                    </a>
                                </li>
                                <li> 
                                    <a
                                        class="flex items-center cursor-pointer p-4"
                                        @click="redirect('AddExistingPatient')"
                                    >
                                        <i class="pi pi-user-plus mr-4"></i>
                                        <span class="font-medium">Add Existing Patient</span>
                                    </a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </template>
    </Drawer>

    <Menubar :model="items" class="mt-2 mr-4 ml-4">
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