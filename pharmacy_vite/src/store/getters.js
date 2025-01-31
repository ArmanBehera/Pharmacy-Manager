export const isRegistered = state => {
    return state.isRegistered
}

export const getUserDetails = state => {
    if (isRegistered === 'true')
        return {'usertype' : state.user_type, 'refresh_token': state.refresh_token, 'access_token': state.access_token,
         'first_name': state.first_name, 'last_name': state.last_name, 'user_id': state.user_id };
    
    return {'usertype': '', 'refresh_token': '', 'access_token': '', 'first_name': '', 'last_name': '', 'user_id': ''};
}