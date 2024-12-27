export const initializeStore = ({ commit, getters }) => {

    if (localStorage.getItem('isRegistered')) {
        const isRegistered = localStorage.getItem('isRegistered');
        const usertype = localStorage.getItem('usertype');
        const firstName = localStorage.getItem('firstName');
        const lastName = localStorage.getItem('lastName');
        const refreshToken = localStorage.getItem('refreshToken');
        const accessToken = localStorage.getItem('accessToken');

        commit('setIsRegistered', isRegistered);
        commit('setUsername', firstName, lastName);
        commit('setUserType', usertype);
        commit('setRefreshToken', refreshToken);
        commit('setAccessToken', accessToken);
    }
}

export const logout = ({ commit }) => {
    localStorage.setItem('usertype', '');
    localStorage.setItem('isRegistered', false);
    localStorage.setItem('refreshToken', '');
    localStorage.setItem('accessToken', '');
    localStorage.setItem('firstName', '');
    localStorage.setItem('lastName', '');
    commit('logout');
}

export const setLoginDetails = ({ commit }, payload) => {
    localStorage.setItem('usertype', payload.usertype);
    localStorage.setItem('isRegistered', payload.isRegistered);
    localStorage.setItem('refreshToken', payload.refreshToken);
    localStorage.setItem('accessToken', payload.accessToken);
    localStorage.setItem('firstName', payload.firstName);
    localStorage.setItem('lastName', payload.lastName);

    commit('setUserType', payload.usertype);
    commit('setUsername', payload.firstName, payload.lastName); // Sets both the first name and last name
    commit('setIsRegistered', payload.isRegistered);
    commit('setRefreshToken', payload.refreshToken);
    commit('setAccessToken', payload.accessToken);
}
