import { createStore, createLogger } from 'vuex';
import * as getters from './getters';
import * as actions from './actions';
import mutations from './mutations';


const state = {
  is_registered: false,
  usertype: '',
  first_name: '',
  last_name: '',
  access_token: '',
  refresh_token: '',
  user_id: '' // If the role is a doctor, then the user_id will be the id from DoctorUser model
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
