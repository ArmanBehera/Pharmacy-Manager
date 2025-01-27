import { createWebHistory, createRouter } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import Logout from '../views/Logout.vue'

import Doctor from '../views/DoctorViews/Index.vue'
import DoctorHomePage from '../views/DoctorViews/HomePage.vue'
import DoctorSignin from '../views/DoctorViews/Signin.vue'
import DoctorLogin from '../views/DoctorViews/Login.vue'
import AddPrescription from '../views/DoctorViews/AddPrescription.vue'

import Admin from '../views/AdminViews/Index.vue'
import AdminHomePage from '../views/AdminViews/HomePage.vue'
import AdminLogin from '../views/AdminViews/Login.vue'
import VerifyEmployees from '../views/AdminViews/VerifyEmployees.vue'
import ViewEmployees from '../views/AdminViews/ViewEmployees.vue'
import ViewMedicines from '../views/AdminViews/ViewMedicines.vue'
import AddNewMedicine from '../views/AdminViews/AddNewMedicine.vue'
import AddLabTests from '../views/AdminViews/AddLabTests.vue'
import ViewLabTests from '../views/AdminViews/ViewLabTests.vue'
import AddExistingMedicine from '../views/AdminViews/AddExistingMedicine.vue'
import ViewSpecializations from '../views/AdminViews/ViewSpecializations.vue'

import FrontDesk from '../views/FrontDeskViews/Index.vue'
import FrontDeskSignin from '../views/FrontDeskViews/Signin.vue'
import FrontDeskLogin from '../views/FrontDeskViews/Login.vue'
import FrontDeskHomePage from '../views/FrontDeskViews/HomePage.vue'
import AddNewPatient from '../views/FrontDeskViews/AddNewPatient.vue'
import AddExistingPatient from '../views/FrontDeskViews/AddExistingPatient.vue'

import Pharmacy from '../views/PharmacyViews/Index.vue'
import PharmacySignin from '../views/PharmacyViews/Signin.vue'
import PharmacyLogin from '../views/PharmacyViews/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
  {
    path: '/doctor',
    component: Doctor,
    children: [
      {
        path: '',
        name: 'DoctorHomePage',
        component: DoctorHomePage
      },
      {
        path: 'Signin',
        name: 'DoctorSignin',
        component: DoctorSignin
      },
      {
        path: 'Login',
        name: 'DoctorLogin',
        component: DoctorLogin
      },
      {
        path: 'AddPrescription',
        name: 'AddPrescription',
        component: AddPrescription
      }
    ]
  },
  {
    path: '/administrator',
    component: Admin,
    children: [
      {
        path: '',
        name: 'AdminHomePage',
        component: AdminHomePage
      },
      {
        path: 'Login',
        name: 'AdminLogin',
        component: AdminLogin
      },
      {
        path: 'VerifyEmployees',
        name: 'VerifyEmployees',
        component: VerifyEmployees
      },
      {
        path: 'ViewEmployees',
        name: 'ViewEmployees',
        component: ViewEmployees
      },
      {
        path: 'ViewMedicines',
        name: 'ViewMedicines',
        component: ViewMedicines
      },
      {
        path: 'AddNewMedicine',
        name: 'AddNewMedicine',
        component: AddNewMedicine
      },
      {
        path: 'AddLabTests',
        name: 'AddLabTests',
        component: AddLabTests
      },
      {
        path: 'ViewLabTests',
        name: 'ViewLabTests',
        component: ViewLabTests
      },
      {
        path: 'AddExistingMedicine',
        name: 'AddExistingMedicine',
        component: AddExistingMedicine
      },
      {
        path: 'ViewSpecializations',
        name: 'ViewSpecializations',
        component: ViewSpecializations
      }
    ]
  },
  {
    path: '/frontdesk',
    component: FrontDesk,
    children: [
      {
        path: '',
        name: 'FrontDeskHomePage',
        component: FrontDeskHomePage
      },
      {
        path: 'Login',
        name: 'FrontDeskLogin',
        component: FrontDeskLogin
      },
      {
        path: 'Signin',
        name: 'FrontDeskSignin',
        component: FrontDeskSignin
      },
      {
        path: 'addNewPatient',
        name: 'AddNewPatient',
        component: AddNewPatient
      },
      {
        path: 'addExistingPatient',
        name: 'AddExistingPatient',
        component: AddExistingPatient
      }
    ]
  },
  {
    path: '/pharmacy',
    component: Pharmacy,
    children: [
      {
        path: 'Login',
        name: 'PharmacyLogin',
        component: PharmacyLogin
      },
      {
        path: 'Signin',
        name: 'PharmacySignin',
        component: PharmacySignin
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router