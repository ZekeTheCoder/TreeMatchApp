import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

// Set up the Axios mock adapter
const mock = new MockAdapter(axios);

// Example test case
test('should refresh token and retry original request', async () => {
    mock.onPost('/auth/refresh').reply(200, { access_token: 'new_access_token' });
    mock.onGet('/protected').reply(401);

    let refresh = false;
    axios.interceptors.response.use(resp => resp, async error => {
        if (error.response.status === 401 && !refresh) {
            refresh = true;

            const response = await axios.post('/auth/refresh', {}, { withCredentials: true });

            if (response.status === 200) {
                axios.defaults.headers.common['Authorization'] = `Bearer ${response.data['access_token']}`;
                return axios(error.config);
            }
        }
        refresh = false;
        return Promise.reject(error);
    });

    await axios.get('/protected').catch(err => {
        expect(err.response.status).toBe(401);
    });

    expect(mock.history.post.length).toBe(1);
    expect(mock.history.post[0].url).toBe('/auth/refresh');

    mock.onGet('/protected').reply(200, { data: 'success' });
    const response = await axios.get('/protected');
    expect(response.status).toBe(200);
    expect(response.data).toEqual({ data: 'success' });
});