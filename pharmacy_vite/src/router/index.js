import { createWebHistory, createRouter } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import Logout from '../views/Logout.vue'

import Doctor from '../views/DoctorViews/Index.vue'
import DoctorHomePage from '../views/DoctorViews/HomePage.vue'
import DoctorSignin from '../views/DoctorViews/Signin.vue'
import DoctorLogin from '../views/DoctorViews/Login.vue'
import AddPrescription from '../views/DoctorViews/AddPrescription.vue'
import ViewPrescription from '../views/DoctorViews/ViewPrescription.vue'

import Administrator from '../views/AdministratorViews/Index.vue'
import AdministratorHomePage from '../views/AdministratorViews/HomePage.vue'
import AdministratorLogin from '../views/AdministratorViews/Login.vue'
import VerifyEmployees from '../views/AdministratorViews/VerifyEmployees.vue'
import ViewEmployees from '../views/AdministratorViews/ViewEmployees.vue'
import ViewMedicines from '../views/AdministratorViews/ViewMedicines.vue'
import AddNewMedicine from '../views/AdministratorViews/AddNewMedicine.vue'
import AddLabTests from '../views/AdministratorViews/AddLabTests.vue'
import ViewLabTests from '../views/AdministratorViews/ViewLabTests.vue'
import AddExistingMedicine from '../views/AdministratorViews/AddExistingMedicine.vue'
import ViewSpecializations from '../views/AdministratorViews/ViewSpecializations.vue'

import FrontDesk from '../views/FrontDeskViews/Index.vue'
import FrontDeskSignin from '../views/FrontDeskViews/Signin.vue'
import FrontDeskLogin from '../views/FrontDeskViews/Login.vue'
import FrontDeskHomePage from '../views/FrontDeskViews/HomePage.vue'
import AddNewPatient from '../views/FrontDeskViews/AddNewPatient.vue'
import AddExistingPatient from '../views/FrontDeskViews/AddExistingPatient.vue'

import Pharmacy from '../views/PharmacyViews/Index.vue'
import PharmacySignin from '../views/PharmacyViews/Signin.vue'
import PharmacyLogin from '../views/PharmacyViews/Login.vue'
import PharmacyHomePage from '../views/PharmacyViews/HomePage.vue'
import UpdateLabTest from '../views/PharmacyViews/UpdateLabTest.vue'
import DispenseMedicines from '../views/PharmacyViews/DispenseMedicines.vue'
import { compareAsc } from 'date-fns'

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
      },
      {
        path: 'ViewPrescription',
        name: 'ViewPrescription',
        component: ViewPrescription
      }
    ]
  },
  {
    path: '/administrator',
    component: Administrator,
    children: [
      {
        path: '',
        name: 'AdministratorHomePage',
        component: AdministratorHomePage
      },
      {
        path: 'Login',
        name: 'AdministratorLogin',
        component: AdministratorLogin
      },
      {
        path: 'VerifyEmployees',
        name: 'AdministratorVerifyEmployees',
        component: VerifyEmployees
      },
      {
        path: 'ViewEmployees',
        name: 'AdministratorViewEmployees',
        component: ViewEmployees
      },
      {
        path: 'ViewMedicines',
        name: 'AdministratorViewMedicines',
        component: ViewMedicines
      },
      {
        path: 'AddNewMedicine',
        name: 'AdministratorAddNewMedicine',
        component: AddNewMedicine
      },
      {
        path: 'AddLabTests',
        name: 'AdministratorAddLabTests',
        component: AddLabTests
      },
      {
        path: 'ViewLabTests',
        name: 'AdministratorViewLabTests',
        component: ViewLabTests
      },
      {
        path: 'AddExistingMedicine',
        name: 'AdministratorAddExistingMedicine',
        component: AddExistingMedicine
      },
      {
        path: 'ViewSpecializations',
        name: 'AdministratorViewSpecializations',
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
        path: 'AddNewPatient',
        name: 'AddNewPatient',
        component: AddNewPatient
      },
      {
        path: 'AddExistingPatient',
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
        path: '',
        name: 'PharmacyHomePage',
        component: PharmacyHomePage
      },
      {
        path: 'Login',
        name: 'PharmacyLogin',
        component: PharmacyLogin
      },
      {
        path: 'Signin',
        name: 'PharmacySignin',
        component: PharmacySignin
      },
      {
        path: 'ViewMedicines',
        name: 'PharmacyViewMedicines',
        component: ViewMedicines
      },
      {
        path: 'AddNewMedicine',
        name: 'PharmacyAddNewMedicine',
        component: AddNewMedicine
      },
      {
        path: 'AddLabTests',
        name: 'PharmacyAddLabTests',
        component: AddLabTests
      },
      {
        path: 'ViewLabTests',
        name: 'PharmacyViewLabTests',
        component: ViewLabTests
      },
      {
        path: 'AddExistingMedicine',
        name: 'PharmacyAddExistingMedicine',
        component: AddExistingMedicine
      },
      {
        path: 'UpdateLabTest',
        name: 'UpdateLabTest',
        component: UpdateLabTest
      },
      {
        path: 'DispenseMedicines',
        name: 'DispenseMedicines',
        component: DispenseMedicines
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router