import * as api from '$lib/api';

export const actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    
    const body = await api.post(`/auth/token`, { 
        mail: data.get('mail'),
        password: data.get('password')
      });

    const value = await body.access_token
    cookies.set('access_token', value, {path: '/'})
  }
};