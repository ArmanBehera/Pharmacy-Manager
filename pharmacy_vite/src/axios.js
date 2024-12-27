import axios from 'axios';
import router from './router';

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000'
});

const getAccessToken = () => {
    return localStorage.getItem('accessToken');
};

const getRefreshToken = () => {
    return localStorage.getItem('refreshToken');
}

const refreshAccessToken = async () => {
    const refreshToken = getRefreshToken();

    if (!refreshToken) {
        return null;
    }

    try {
        const response = await instance.post('/api/v1/jwt/refresh', { refresh: refreshToken });
        const accessToken = response.data.access;
        localStorage.setItem('accessToken', accessToken);
        return accessToken;
    } catch (error) {
        return null; // The refresh token is invalid or expired.
    }
}

instance.interceptors.request.use(
    async(config) => {
        let accessToken = getAccessToken();

        if (accessToken) {
            config.headers['Authorization'] = `JWT ${accessToken}`
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
        const originalRequest = error.config

        if (error.response.status === 403) {
            const newAccessToken = await refreshAccessToken(); // Gets a new access token as the previous token is expired
            if (newAccessToken) {
                originalRequest.headers['Authorization'] = `JWT ${newAccessToken}`; // Changes the access token in the header of the original request's to reflect the changes
                return instance(originalRequest); // Sends the modified original request back to the backend in another try
            }
        }
        // Indicates that the refresh token is expired and user needs to be logged in again. 
        else if (error.response.status === 401) {
            const usertype = localStorage.getItem('usertype');

            // If there isn't a usertype and the user is in the login page then the user won't be redirected
            if (!usertype && !window.location.href.includes('login')) {
                router.push('/');
            }
            else if (usertype) {
                router.push(`/${usertype}/login/`);
            }  
        }
        
        // This statement is executed for all others errors, such as permission denied (403). They are to be handled individually by the respective pages.
        return Promise.reject(error);
    }
)

export default instance;