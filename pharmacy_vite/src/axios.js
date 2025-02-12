import axios from 'axios';
import router from './router';

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000'
});

const getAccessToken = () => {
    return localStorage.getItem('access_token');
};

const getRefreshToken = () => {
    return localStorage.getItem('refresh_token');
}

const refreshAccessToken = async () => {
    const refresh_token = getRefreshToken();

    if (!refresh_token) {
        return null;
    }

    try {
        const response = await instance.post('/api/v1/jwt/refresh', { refresh: refresh_token });
        const access_token = response.data.access;
        localStorage.setItem('access_token', access_token);
        return access_token;
    } catch (error) {
        return null; // The refresh token is invalid or expired.
    }
}

instance.interceptors.request.use(
    async(config) => {
        let access_token = getAccessToken();

        if (access_token) {
            config.headers['Authorization'] = `JWT ${access_token}`
        }

        return config
    },
    (error) => {
        console.log(`Request Error: ${error}`)
        return Promise.reject(error)
    }
)

instance.interceptors.response.use(
    (response) => {
        return response
    },
    async (error) => {
        console.log(error.response)
        const original_request = error.config

        // If the access token is expired and needs to be refreshed
        if (error.response.status === 403 && error.response.data.detail === 'Authentication credentials were not provided.') {
            const new_access_token = await refreshAccessToken(); // Gets a new access token as the previous token is expired

            if (new_access_token) {
                original_request.headers['Authorization'] = `JWT ${new_access_token}`; // Changes the access token in the header of the original request's to reflect the changes
                return instance(original_request); // Sends the modified original request back to the backend in another try
            }
        }
        // Indicates that the refresh token is expired and user needs to be logged in again. 
        else if (error.response.status === 401 && error.response.data.detail === 'Token is invalid or expired') {
            const usertype = localStorage.getItem('usertype');
            localStorage.setItem('usertype', '');
            localStorage.setItem('is_registered', false);
            localStorage.setItem('refresh_token', '');
            localStorage.setItem('access_token', '');
            localStorage.setItem('first_name', '');
            localStorage.setItem('last_name', '');
            localStorage.setItem('user_id', '');
            // If there isn't a usertype and the user is in the login page then the user will be directed to the home page
            if (!usertype && !window.location.href.includes('login')) {
                router.push('/');
            }
            else if (usertype  && !window.location.href.includes('login')) {
                router.push(`/${usertype}/login/`);
            }
        }
        // This statement is executed for all others errors, such as permission denied (403). They are to be handled individually by the respective pages.
        return Promise.reject(error);
    }
)

export default instance;