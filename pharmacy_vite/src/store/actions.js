export const initializeStore = ({ commit, getters }) => {

    if (localStorage.getItem('is_registered')) {
        const is_registered = localStorage.getItem('is_registered');
        const usertype = localStorage.getItem('usertype');
        const first_name = localStorage.getItem('first_name');
        const last_name = localStorage.getItem('last_name');
        const refresh_token = localStorage.getItem('refresh_token');
        const access_token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id')

        commit('setIsRegistered', is_registered);
        commit('setFirstName', first_name);
        commit('setLastName', last_name);
        commit('setUserType', usertype);
        commit('setRefreshToken', refresh_token);
        commit('setAccessToken', access_token);
        commit('setUserId', user_id);
    }
}

export const logout = ({ commit }) => {
    localStorage.setItem('usertype', '');
    localStorage.setItem('is_registered', false);
    localStorage.setItem('refresh_token', '');
    localStorage.setItem('access_token', '');
    localStorage.setItem('first_name', '');
    localStorage.setItem('last_name', '');
    localStorage.setItem('user_id', '');
    commit('logout');
}

export const setLoginDetails = ({ commit }, payload) => {
    localStorage.setItem('usertype', payload.usertype);
    localStorage.setItem('is_registered', payload.is_registered);
    localStorage.setItem('refresh_token', payload.refresh_token);
    localStorage.setItem('access_token', payload.access_token);
    localStorage.setItem('first_name', payload.first_name);
    localStorage.setItem('last_name', payload.last_name);
    localStorage.setItem('user_id', payload.user_id);

    commit('setUserType', payload.usertype);
    commit('setFirstName', payload.first_name);
    commit('setLastName', payload.last_name);
    commit('setIsRegistered', payload.is_registered);
    commit('setRefreshToken', payload.refresh_token);
    commit('setAccessToken', payload.access_token);
    commit('setUserId', payload.user_id);
}
