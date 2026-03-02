import { useCallback } from 'react';
import useAuthStore from '../store/authStore';
import client from '../api/client';

export default function useAuth() {
  const setAuth = useAuthStore((state) => state.setAuth);
  const clearAuth = useAuthStore((state) => state.clearAuth);

  const login = useCallback(async (credentials) => {
    const response = await client.post('/auth/login', credentials);
    const { access_token, user } = response.data;
    setAuth(access_token, user);
    return response;
  }, [setAuth]);

  const register = useCallback(async (values) => {
    const response = await client.post('/auth/register', values);
    return response;
  }, [setAuth]);

  const logout = useCallback(() => {
    clearAuth();
  }, [clearAuth]);

  return { login, register, logout };
}
