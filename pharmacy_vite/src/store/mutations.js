export default {
    setUserType(state, usertype) {
        state.usertype = usertype;
    },

    setIsRegistered(state, is_registered) {
        state.is_registered = is_registered;
    },

    setFirstName(state, first_name) {
        state.first_name = first_name;
    },

    setLastName(state, last_name) {
        state.last_name = last_name
    },
    
    setRefreshToken(state, refresh_token) {
        state.refresh_token = refresh_token
    },

    setAccessToken(state, access_token) {
        state.access_token = access_token
    },

    setUserId(state, user_id) {
        state.user_id = user_id
    },

    logout (state) {    
        state.usertype = '';
        state.is_registered = false;
        state.access_token = '';
        state.refresh_token = '';
        state.first_name = '';
        state.last_name = '';
        state.user_id = '';
    }
}