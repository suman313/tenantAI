// frontend/src/components/RequestCard.jsx
// ==============================================
// 📇 Single Maintenance Request Card
// Shows details + a status dropdown
// ==============================================
export default function RequestCard({ request, onStatusChange }) {
    const statusColors = {
        received: 'bg-yellow-100',
        in_progress: 'bg-blue-100',
        completed: 'bg-green-100',
    };

    return (
        <div className={`p-4 rounded shadow ${statusColors[request.status] || 'bg-gray-100'}`}>
            <div className="flex justify-between items-center">
                <span className="font-semibold text-lg">
                    #{request.id} – {request.issue_type} in {request.unit_number || 'Unknown Unit'}
                </span>
                <select
                    value={request.status}
                    onChange={(e) => onStatusChange(request.id, e.target.value)}
                    className="border rounded px-2 py-1 text-sm"
                >
                    <option value="received">Received</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                </select>
            </div>
            <p className="text-gray-700 mt-2">{request.summary}</p>
            <p className="text-sm text-gray-500 mt-1">
                Contractor: <span className="font-medium">{request.contractor_name}</span> ({request.contractor_phone})
            </p>
            <p className="text-xs text-gray-400 mt-1">
                {new Date(request.created_at).toLocaleString()}
            </p>
            {request.email_id && (
                <a
                    href={`https://mail.google.com/mail/u/0/#inbox/${request.email_id}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-600 text-sm hover:underline mt-2 inline-block"
                >
                    📧 Open original email in Gmail
                </a>
            )}
        </div>
    );
}