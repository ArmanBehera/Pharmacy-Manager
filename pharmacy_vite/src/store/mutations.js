export default {
    setUserType(state, usertype) {
        state.usertype = usertype;
    },

    setIsRegistered(state, isRegistered) {
        state.isRegistered = isRegistered;
    },

    setUsername(state, firstName, lastName) {
        state.firstName = firstName;
        state.lastName = lastName;
    },
    
    setRefreshToken(state, refresh) {
        state.refreshToken = refresh
    },

    setAccessToken(state, access) {
        state.accessToken = access
    },

    logout (state) {

        state.usertype = '';
        state.isRegistered = false;
        state.accessToken = '';
        state.refreshToken = '';
        state.firstName = '';
        state.lastName = '';
    }
}