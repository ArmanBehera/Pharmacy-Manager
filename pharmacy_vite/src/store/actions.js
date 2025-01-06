export const initializeStore = ({ commit, getters }) => {

    if (localStorage.getItem('isRegistered')) {
        const isRegistered = localStorage.getItem('isRegistered');
        const usertype = localStorage.getItem('usertype');
        const firstName = localStorage.getItem('firstName');
        const lastName = localStorage.getItem('lastName');
        const refreshToken = localStorage.getItem('refreshToken');
        const accessToken = localStorage.getItem('accessToken');
        const userId = localStorage.getItem('userId')

        commit('setIsRegistered', isRegistered);
        commit('setFirstName', firstName);
        commit('setLastName', lastName);
        commit('setUserType', usertype);
        commit('setRefreshToken', refreshToken);
        commit('setAccessToken', accessToken);
        commit('setUserId', userId);
    }
}

export const logout = ({ commit }) => {
    localStorage.setItem('usertype', '');
    localStorage.setItem('isRegistered', false);
    localStorage.setItem('refreshToken', '');
    localStorage.setItem('accessToken', '');
    localStorage.setItem('firstName', '');
    localStorage.setItem('lastName', '');
    localStorage.setItem('userId', '');
    commit('logout');
}

export const setLoginDetails = ({ commit }, payload) => {
    localStorage.setItem('usertype', payload.usertype);
    localStorage.setItem('isRegistered', payload.isRegistered);
    localStorage.setItem('refreshToken', payload.refreshToken);
    localStorage.setItem('accessToken', payload.accessToken);
    localStorage.setItem('firstName', payload.firstName);
    localStorage.setItem('lastName', payload.lastName);
    localStorage.setItem('userId', payload.userId);

    commit('setUserType', payload.usertype);
    commit('setFirstName', payload.firstName);
    commit('setLastName', payload.lastName);
    commit('setIsRegistered', payload.isRegistered);
    commit('setRefreshToken', payload.refreshToken);
    commit('setAccessToken', payload.accessToken);
    commit('setUserId', payload.userId);
}
