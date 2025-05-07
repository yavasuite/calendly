import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BookingForm from "./components/BookingForm";
import Login from "./components/Login";
import Register from "./components/Register";
import Home from "./components/Home";
import BookingConfirmation from "./components/BookingConfirmation";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/book" element={<BookingForm />} />
                <Route path="/confirm" element={<BookingConfirmation />} />
            </Routes>
        </Router>
    );
}

export default App;
