import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        const role = localStorage.getItem('role');
        const userId = localStorage.getItem('userId');
        if (token && role && userId) {
            setUser({ token, role, userId });
        }
    }, []);

    const login = async (email, password) => {
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || 'Login failed');
        }

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('userId', data.user_id);
        setUser({ token: data.access_token, role: data.role, userId: data.user_id });
        navigate('/dashboard');
    };

    const register = async (email, password) => {
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, role: 'User' }),
        });

        let data;
        try {
            data = await res.json();
        } catch {
            throw new Error("Invalid response from server. Could not parse JSON.");
        }

        if (!res.ok) {
            throw new Error(data?.error || 'Registration failed');
        }

        localStorage.setItem('token', data.token);
        localStorage.setItem('role', 'User');
        localStorage.setItem('userId', data.user_id || null);
        setUser({ token: data.token, role: 'User', userId: data.user_id || null });
        navigate('/dashboard');
    };

    const logout = () => {
        localStorage.clear();
        setUser(null);
        navigate('/login');
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
