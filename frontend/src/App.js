import React from "react";
import { AuthProvider } from './context/AuthContext';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BookingForm from "./components/BookingForm";
import Login from "./components/Login";
import Register from "./components/Register";
import Home from "./components/Home";
import BookingConfirmation from "./components/BookingConfirmation";

function App() {
    return (
        <Router>
            <AuthProvider>
                <Routes>
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/confirm" element={<BookingConfirmation />} />
                    </Routes>
                </Routes>
            </AuthProvider>
        </Router>
    );
}

export default App;
