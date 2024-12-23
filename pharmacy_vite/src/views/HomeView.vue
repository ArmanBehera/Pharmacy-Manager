<script setup>
    import '../styles/styles.css';
    import { ref } from 'vue';
    import { useStore } from 'vuex';

    const store = useStore(); 
    store.dispatch('initializeStore');

    const options = ref([
        {
            'name': 'Admin',
            'description': 'Manage users, appointments, and system settings',
            'loginroute': 'AdminLogin'
        },
        {
            'name': 'Doctor',
            'description': 'View and manage patient appointments',
            'loginroute': 'DoctorLogin',
            'siginroute': 'DoctorSignin'
        },
        {
            'name': 'Front Desk',
            'description': 'Handle front desk tasks like scheduling and patient check-ins',
            'loginroute': 'FrontDeskLogin',
            'siginroute': 'FrontDeskSignin'
        },
        {
            'name': 'Pharmacy',
            'description': 'Manage prescriptions, medicine inventory, and dispense medications to patients',
            'loginroute': 'PharmacyLogin',
            'siginroute': 'PharmacySignin'
        }
    ])
</script>

<template>
    <!-- Landing Page Introduction -->
    <div class="text-center my-8">
        <h1 class="text-4xl font-bold text-gray-800">Welcome to Our Healthcare Management System</h1>
        <p class="text-lg text-gray-500">Easily manage appointments, prescriptions, and more based on your role.</p>
    </div>  

    <div class="card">
        <Carousel :value="options" :numVisible="1" :numScroll="1" :responsiveOptions="responsiveOptions" circular :autoplayInterval="10000">
            <template #item="slotProps">
                <div class="relative border border-surface-200 dark:border-surface-700 rounded m-2 p-4 bg-cover bg-center" :style="{ backgroundImage: `url(${asd})` }">
                    <div class="flex flex-column items-center justify-center h-full">
                        <div class="text-white text-2xl p-4 rounded">{{ slotProps.data.name }}</div>
                        <div class="mt-10 text-l">{{ slotProps.data.description }}</div>
                        <span class="mt-5">
                            <Button icon="pi pi-sign-in" severity="secondary" label="Sign In" @click="$router.push({ name: slotProps.data.siginroute })" v-if="slotProps.data.siginroute"/>
                            <Button icon="pi pi-user" label="Log In" class="ml-4" @click="$router.push({ name: slotProps.data.loginroute })"/>
                        </span>
                    </div>
                </div>
            </template>
        </Carousel>

    </div>

    <!-- Footer Section with Useful Links -->
    <footer class="mt-16 bg-gray-100 p-4 text-center">
        <p class="text-gray-600">© 2024 Healthcare Management System</p>
        <div class="flex justify-center space-x-4">
            <a href="/privacy-policy" class="text-indigo-400 underline">Privacy Policy</a>
            <a href="/terms-of-service" class="text-indigo-400 underline">Terms of Service</a>
            <a href="/help" class="text-indigo-400 underline">Help</a>
        </div>
    </footer>
</template>

<style scoped>
  .routerlink {
    color: white;
    border-radius: 8px;
    transition: background-color 0.3s ease;
  }

  .btn-large {
    width: 80%; /* Make the button fill the container */
    padding: 8px; /* Add more padding for larger buttons */
    font-size: 1.25rem; /* Increase the font size */
    background-color: #4f46e5; /* Adjust background color if necessary */
  }

  .btn-large:hover {
    background-color: #3730a3; /* Darken on hover */
  }

  .routerlink p {
    word-break: keep-all; /* Prevents breaking words */
  }
</style>
