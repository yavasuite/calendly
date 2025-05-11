import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const BookingForm = () => {
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        start_time: "",
        end_time: "",
    });

    const [status, setStatus] = useState(null);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const token = localStorage.getItem("token");

            const res = await axios.post(
                `${API_BASE_URL}/api/meetings/schedule`,
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                }
            );

            // Navigate to confirmation page with meeting data
            navigate("/confirm", { state: { meeting: res.data } });
        } catch (err) {
            setStatus("❌ Error: " + (err.response?.data?.error || "Unknown"));
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 border rounded-xl shadow">
            <h2 className="text-xl font-bold mb-4">Book a Meeting</h2>
            <form onSubmit={handleSubmit} className="space-y-3">
                <input
                    type="text"
                    name="title"
                    placeholder="Title"
                    className="w-full p-2 border rounded"
                    value={formData.title}
                    onChange={handleChange}
                    required
                />
                <textarea
                    name="description"
                    placeholder="Description"
                    className="w-full p-2 border rounded"
                    value={formData.description}
                    onChange={handleChange}
                />
                <input
                    type="datetime-local"
                    name="start_time"
                    className="w-full p-2 border rounded"
                    value={formData.start_time}
                    onChange={handleChange}
                    required
                />
                <input
                    type="datetime-local"
                    name="end_time"
                    className="w-full p-2 border rounded"
                    value={formData.end_time}
                    onChange={handleChange}
                    required
                />
                <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">
                    Book
                </button>
            </form>
            {status && <p className="mt-4">{status}</p>}
        </div>
    );
};

export default BookingForm;
