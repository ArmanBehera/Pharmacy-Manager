export const isRegistered = state => {
    return state.isRegistered
}

export const getUserDetails = state => {
    if (isRegistered)
        return {'usertype' : state.usertype, 'refreshToken': state.refreshToken, 'accessToken': state.accessToken,
         'firstName': state.firstName, 'lastName': state.lastName, 'username': state.username };
    
    return {'usertype' : '', 'usertype': '', 'refreshToken': '', 'accessToken': '', 'firstName': '', 'lastName': ''};
}