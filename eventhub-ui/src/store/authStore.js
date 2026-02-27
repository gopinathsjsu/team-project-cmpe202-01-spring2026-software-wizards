import create from 'zustand';

const useAuthStore = create((state) => ({
  token: null,
  user: null,
  setAuth: (token, user) => set({ token, user }),
  clearAuth: () => set({ token: null, user: null }),
}));

export const getAuthToken = () => {
  const state = useAuthStore.getState();
  return state.token;
};

export const clearAuth = () => {
  useAuthStore.getState().clearAuth();
};

export default useAuthStore;
