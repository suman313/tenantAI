// frontend/src/api.js
// ==============================================
// 📞 API Service – speaks to our FastAPI backend
// ==============================================
import axios from 'axios';

const API_BASE = 'https://didactic-potato-ppwpjx99x6x297xv-8000.app.github.dev/api';
const PASSWORD = 'admin123';   // same as in backend/auth.py

const headers = { 'x-password': PASSWORD };

export const fetchRequests = () =>
    axios.get(`${API_BASE}/requests`, { headers });

export const updateRequestStatus = (id, status) =>
    axios.patch(`${API_BASE}/requests/${id}/status`, { status }, { headers });