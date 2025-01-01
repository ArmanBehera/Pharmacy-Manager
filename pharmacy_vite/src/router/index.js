import { createWebHistory, createRouter } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import Logout from '../views/Logout.vue'

import Doctor from '../views/DoctorViews/Index.vue'
import DoctorHomePage from '../views/DoctorViews/HomePage.vue'
import DoctorSignin from '../views/DoctorViews/Signin.vue'
import DoctorLogin from '../views/DoctorViews/Login.vue'

import Admin from '../views/AdminViews/Index.vue'
import AdminHomePage from '../views/AdminViews/HomePage.vue'
import AdminLogin from '../views/AdminViews/Login.vue'
import VerifyEmployees from '../views/AdminViews/VerifyEmployees.vue'
import ViewEmployees from '../views/AdminViews/ViewEmployees.vue'
import ViewMedicines from '../views/AdminViews/ViewMedicines.vue'
import AddMedicines from '../views/AdminViews/AddMedicines.vue'
import EditMedicines from '../views/AdminViews/EditMedicines.vue'

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
        path: 'signin',
        name: 'DoctorSignin',
        component: DoctorSignin
      },
      {
        path: 'login',
        name: 'DoctorLogin',
        component: DoctorLogin
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
        path: 'login',
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
        path: 'AddMedicines',
        name: 'AddMedicines',
        component: AddMedicines
      },
      {
        path: 'EditMedicines',
        name: 'EditMedicines',
        component: EditMedicines
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
        path: 'login',
        name: 'FrontDeskLogin',
        component: FrontDeskLogin
      },
      {
        path: 'signin',
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
        path: 'login',
        name: 'PharmacyLogin',
        component: PharmacyLogin
      },
      {
        path: 'signin',
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