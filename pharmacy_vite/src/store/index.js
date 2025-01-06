import { createStore, createLogger } from 'vuex';
import * as getters from './getters';
import * as actions from './actions';
import mutations from './mutations';


const state = {
  isRegistered: false,
  usertype: '',
  firstName: '',
  lastName: '',
  accessToken: '',
  refreshToken: '',
  userId: '' // If the role is a doctor, then the user_id will be the id from DoctorUser model
}

export default createStore({

  state,
  getters,
  actions,
  mutations,
  plugins: process.env.NODE_ENV !== 'production'
    ? [createLogger()]
    : []
})
