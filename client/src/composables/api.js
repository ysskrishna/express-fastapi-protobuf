import axios from 'axios';
import { API_BASE } from '../config.js';

export async function getTags(params = {}) {
  const response = await axios.get(`${API_BASE}/tags`, { params });
  return response.data || {};
}

export async function getQuotes(params = {}) {
  const response = await axios.get(`${API_BASE}/quotes`, { params });
  return response.data || {};
}

