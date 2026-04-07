import axios from 'axios';
import { 
  User, 
  TokenResponse, 
  Specification, 
  SharedLink, 
  TrelloExport,
  ProjectType,
  ComplexityLevel 
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  register: async (email: string, name: string, password: string): Promise<User> => {
    const response = await api.post<User>('/auth/register', { email, name, password });
    return response.data;
  },
  
  login: async (email: string, password: string): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/auth/login', { email, password });
    localStorage.setItem('token', response.data.access_token);
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('token');
  },
  
  getToken: () => localStorage.getItem('token'),
};

export const specApi = {
  generate: async (type: ProjectType, complexity: ComplexityLevel): Promise<Specification> => {
    const response = await api.post<Specification>('/specifications/generate', { type, complexity });
    return response.data;
  },
  
  list: async (): Promise<Specification[]> => {
    const response = await api.get<Specification[]>('/specifications');
    return response.data;
  },
  
  get: async (id: string): Promise<Specification> => {
    const response = await api.get<Specification>(`/specifications/${id}`);
    return response.data;
  },
  
  update: async (id: string, title?: string, content?: object): Promise<Specification> => {
    const response = await api.put<Specification>(`/specifications/${id}`, { title, content });
    return response.data;
  },
  
  delete: async (id: string): Promise<void> => {
    await api.delete(`/specifications/${id}`);
  },
  
  share: async (id: string): Promise<SharedLink> => {
    const response = await api.post<SharedLink>(`/specifications/${id}/share`);
    return response.data;
  },
  
  getShared: async (token: string): Promise<Specification> => {
    const response = await api.get<Specification>(`/shared/${token}`);
    return response.data;
  },
};

export const exportApi = {
  downloadDocx: async (id: string): Promise<Blob> => {
    const response = await api.get(`/export/${id}/docx`, { responseType: 'blob' });
    return response.data;
  },
  
  downloadPdf: async (id: string): Promise<Blob> => {
    const response = await api.get(`/export/${id}/pdf`, { responseType: 'blob' });
    return response.data;
  },
  
  getTrello: async (id: string): Promise<TrelloExport> => {
    const response = await api.get<TrelloExport>(`/export/${id}/trello`);
    return response.data;
  },
};

export default api;