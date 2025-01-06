export default {
    setUserType(state, usertype) {
        state.usertype = usertype;
    },

    setIsRegistered(state, isRegistered) {
        state.isRegistered = isRegistered;
    },

    setFirstName(state, firstName) {
        state.firstName = firstName;
    },

    setLastName(state, lastName) {
        state.lastName = lastName
    },
    
    setRefreshToken(state, refresh) {
        state.refreshToken = refresh
    },

    setAccessToken(state, access) {
        state.accessToken = access
    },

    setUserId(state, userId) {
        state.userId = userId
    },

    logout (state) {    
        state.usertype = '';
        state.isRegistered = false;
        state.accessToken = '';
        state.refreshToken = '';
        state.firstName = '';
        state.lastName = '';
        state.userId = '';
    }
}