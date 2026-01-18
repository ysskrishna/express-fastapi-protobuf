import axios from 'axios';

const API_BASE = typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE
  ? import.meta.env.VITE_API_BASE
  : 'http://localhost:3000/api';

export async function getTags(params = {}) {
  const response = await axios.get(`${API_BASE}/tags`, { params });
  return response.data || {};
}

export async function getQuotes(params = {}) {
  const response = await axios.get(`${API_BASE}/quotes`, { params });
  return response.data || {};
}

