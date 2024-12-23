export const isRegistered = state => {
    return JSON.parse(localStorage.getItem('isRegistered'))
}

export const getUserDetails = state => {

    if (isRegistered) {

        const usertype = localStorage.getItem('usertype');
        const refreshToken = localStorage.getItem('refreshToken')
        const accessToken = localStorage.getItem('accessToken')
        const firstName = localStorage.getItem('firstName')
        const lastName = localStorage.getItem('lastName')

        return {'usertype' : usertype, 'refreshToken': refreshToken, 'accessToken': accessToken, 'firstName': firstName, 'lastName': lastName }
    }

    return {'usertype' : '', 'refreshToken': '', 'accessToken': '', 'firstName': '', 'lastName': ''}
}