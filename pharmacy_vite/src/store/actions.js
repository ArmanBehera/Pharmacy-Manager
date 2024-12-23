export const initializeStore = ({ commit, getters }) => {
    const isRegistered = getters.isRegistered;

    if (isRegistered) {
        const userDetails= getters.getUserDetails;
        commit('setIsRegistered', true);
        commit('setUsername', userDetails.firstName, userDetails.lastName);
        commit('setUserType', userDetails.usertype);
        commit('setRefreshToken', userDetails.refreshToken);
        commit('setAccessToken', userDetails.accessToken);
    }
}

export const logout = ({ commit }) => {
    localStorage.setItem('usertype', '');
    localStorage.setItem('isRegistered', JSON.stringify(false));
    localStorage.setItem('refreshToken', '');
    localStorage.setItem('accessToken', '');
    localStorage.setItem('firstName', '');
    localStorage.setItem('lastName', '');
    commit('logout');
}

export const setLoginDetails = ({ commit }, payload) => {
    localStorage.setItem('usertype', payload.usertype);
    localStorage.setItem('isRegistered', JSON.stringify(payload.isRegistered));
    localStorage.setItem('refreshToken', payload.refreshToken);
    localStorage.setItem('accessToken', payload.accessToken);
    localStorage.setItem('firstName', payload.firstName);
    localStorage.setItem('lastName', payload.lastName);

    commit('setUserType', payload.usertype);
    commit('setUsername', payload.firstName, payload.lastName);
    commit('setIsRegistered', payload.isRegistered);
    commit('setRefreshToken', payload.refreshToken);
    commit('setAccessToken', payload.accessToken);
}