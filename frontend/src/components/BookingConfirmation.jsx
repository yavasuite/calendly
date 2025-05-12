import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const BookingConfirmation = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const meeting = location.state?.meeting;

    if (!meeting) {
        return (
            <div className="max-w-xl mx-auto mt-10 p-6 bg-white shadow-md rounded-lg">
                <h2 className="text-2xl font-semibold mb-4">No Booking Found</h2>
                <p className="text-gray-600 mb-6">
                    No meeting data was passed to this page.
                </p>
                <button
                    className="bg-blue-600 text-white px-4 py-2 rounded"
                    onClick={() => navigate('/')}
                >
                    Return Home
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white shadow-md rounded-lg">
            <h1 className="text-3xl font-bold text-green-600 mb-4">Booking Confirmed</h1>

            <div className="text-gray-800 space-y-2">
                <p><strong>Meeting ID:</strong> {meeting.id}</p>
                <p><strong>Title:</strong> {meeting.title}</p>
                {meeting.description && <p><strong>Description:</strong> {meeting.description}</p>}
                <p><strong>Status:</strong> {meeting.status}</p>
                <p><strong>Date:</strong> {new Date(meeting.start_time).toLocaleDateString()}</p>
                <p>
                    <strong>Time:</strong>{' '}
                    {new Date(meeting.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} -{' '}
                    {new Date(meeting.end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
                <p><strong>User ID:</strong> {meeting.user_id}</p>
            </div>

            <div className="mt-6">
                <button
                    className="bg-blue-600 text-white px-4 py-2 rounded"
                    onClick={() => navigate('/')}
                >
                    Book Another Meeting
                </button>
            </div>
        </div>
    );
};

export default BookingConfirmation;