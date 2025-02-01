<script setup>
    import router from '../../router';
    import { watch } from 'vue';
    import { ref, computed } from 'vue';
    import { useStore } from 'vuex';
    import axios from '../../axios';
    import '../../styles/styles.css';
    
    const store = useStore();
    const drawer_visible = ref(false);
    const dropdown_open_medicines = ref(false);
    const dropdown_open_lab_tests = ref(false); 

    store.dispatch('initializeStore');

    const items = ref([
        {
            label: '',
            icon: 'pi pi-bars',
            loggedIn: true,
            loggedOut: false,
            command: () => {
                drawer_visible.value = true;
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
                router.push({ name: 'PharmacyHomePage' })
            }
        },
        {
            label: 'Login',
            icon: 'pi pi-user',
            loggedIn: false,
            loggedOut: true,
            command: () => {
                router.push({ name: 'PharmacyLogin' })
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

    const toggleDropdownMedicines = () => {
        dropdown_open_medicines.value = !dropdown_open_medicines.value;
    }

    const toggleDropdownLabTests = () => {
        dropdown_open_lab_tests.value = !dropdown_open_lab_tests.value
    }

    const redirect = (url_name) => {
        router.push({ name: url_name})
        drawer_visible.value = false
    }
</script>

<template>
    <Drawer v-model:visible="drawer_visible">
        <template #container="{ closeCallback }">
            <div class="flex flex-col h-full">
                <div class="flex items-center justify-between px-3 py-4 shadow-md">
                    <div class="inline-flex items-center gap-4">
                        <img src="../../assets/Pharmacy.png" alt="Pharmacy Logo" class="h-10 w-10" />
                        <h1 class="font-bold text-2xl text-primary">Pharmacy</h1>
                    </div>
                    <Button type="button" @click="closeCallback" icon="pi pi-times" rounded outlined></Button>
                </div>

                <div class="overflow-y-auto">
                    <ul class="list-none p-4 m-0">
                        <li>
                            <a
                                @click="toggleDropdownMedicines"
                                class="flex items-center cursor-pointer p-4 rounded text-surface-700 hover:bg-surface-100 dark:text-surface-0 dark:hover:bg-surface-800 duration-150 transition-colors p-ripple"
                            >
                                <i class="pi pi-chart-line mr-4"></i>
                                <span class="font-medium">Manage Medicines</span>
                                <i class="pi pi-chevron-down ml-auto transform transition-transform duration-600" :class="{ 'rotate-180': dropdown_open_medicines }"></i>
                            </a>
                            <ul v-show="dropdown_open_medicines" class="list-none py-0 pl-4 pr-0 m-0 overflow-y-hidden transition-all duration-[400ms] ease-in-out">
                                <li> 
                                    <a 
                                        class="flex items-center cursor-pointer p-4"
                                         @click="redirect('PharmacyViewMedicines')"
                                    >
                                        
                                        <i class="pi pi-eye mr-4"></i>
                                        <span class="font-medium">View Medicines Inventory</span>
                                    </a>
                                </li>
                                <li> 
                                    <a 
                                        class="flex items-center cursor-pointer p-4"
                                        @click="redirect('PharmacyAddNewMedicine')"
                                    >
                                        <i class="pi pi-plus mr-4"></i>
                                        <span class="font-medium">Add New Medcines</span>
                                    </a>
                                </li>
                                <li> 
                                    <a 
                                        class="flex items-center cursor-pointer p-4"
                                        @click="redirect('PharmacyAddExistingMedicine')"
                                    >
                                        <i class="pi pi-plus mr-4"></i>
                                        <span class="font-medium">Add Stock for Existing Medcines</span>
                                    </a>
                                </li>
                            </ul>
                        </li>

                        <li>
                            <a
                                @click="toggleDropdownLabTests"
                                class="flex items-center cursor-pointer p-4 rounded text-surface-700 hover:bg-surface-100 dark:text-surface-0 dark:hover:bg-surface-800 duration-150 transition-colors p-ripple"
                            >
                                <i class="pi pi-chart-line mr-4"></i>
                                <span class="font-medium">Manage Lab Tests</span>
                                <i class="pi pi-chevron-down ml-auto transform transition-transform duration-600" :class="{ 'rotate-180': dropdown_open_lab_tests }"></i>
                            </a>
                            <ul v-show="dropdown_open_lab_tests" class="list-none py-0 pl-4 pr-0 m-0 overflow-y-hidden transition-all duration-[400ms] ease-in-out">
                                <li> 
                                    <a 
                                        class="flex items-center cursor-pointer p-4"
                                         @click="redirect('PharmacyViewLabTests')"
                                    >
                                        
                                        <i class="pi pi-eye mr-4"></i>
                                        <span class="font-medium">View Lab Tests</span>
                                    </a>
                                </li>
                                <li> 
                                    <a 
                                        class="flex items-center cursor-pointer p-4"
                                        @click="redirect('PharmacyAddLabTests')"
                                    >
                                        <i class="pi pi-plus mr-4"></i>
                                        <span class="font-medium">Add Lab Test</span>
                                    </a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </template>
    </Drawer>

    <Menubar :model="items">
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