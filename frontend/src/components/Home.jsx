
import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white shadow-md rounded-lg text-center">
            <h1 className="text-3xl font-bold mb-6">Welcome to YavaSuite Scheduler</h1>

            <div className="space-y-4">
                <Link to="/book" className="block bg-blue-600 text-white px-6 py-3 rounded">
                    Book a Meeting
                </Link>
                <Link to="/login" className="block bg-gray-700 text-white px-6 py-3 rounded">
                    Login
                </Link>
                <Link to="/register" className="block bg-gray-500 text-white px-6 py-3 rounded">
                    Register
                </Link>
            </div>
        </div>
    );
};

export default Home;
