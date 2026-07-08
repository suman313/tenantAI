// frontend/src/components/Dashboard.jsx
// ==============================================
// 🏠 Main Dashboard – fetches & lists all requests
// ==============================================
import { useEffect, useState } from 'react';
import { fetchRequests, updateRequestStatus } from '../api';
import RequestCard from './RequestCard';

export default function Dashboard() {
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const loadRequests = async () => {
        try {
            const res = await fetchRequests();
            setRequests(res.data);
            setError(null);
        } catch (err) {
            setError('Failed to load requests. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadRequests();
    }, []);

    const handleStatusChange = async (id, newStatus) => {
        try {
            await updateRequestStatus(id, newStatus);
            // Optimistic update
            setRequests(prev =>
                prev.map(r => (r.id === id ? { ...r, status: newStatus } : r))
            );
        } catch (err) {
            alert('Failed to update status. Check backend connection.');
        }
    };

    if (loading) return <div className="p-6 text-center">Loading...</div>;
    if (error) return <div className="p-6 text-red-600 text-center">{error}</div>;

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">🏠 Maintenance Dashboard</h1>
                <button
                    onClick={loadRequests}
                    className="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded text-sm"
                >
                    🔄 Refresh
                </button>
            </div>
            {requests.length === 0 ? (
                <p className="text-gray-500 text-center">No maintenance requests yet. They'll appear here once the agent processes emails.</p>
            ) : (
                <div className="grid gap-4">
                    {requests.map(req => (
                        <RequestCard key={req.id} request={req} onStatusChange={handleStatusChange} />
                    ))}
                </div>
            )}
        </div>
    );
}