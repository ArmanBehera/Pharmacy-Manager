import axios from 'axios';

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