import React, { createContext, useContext, useState, useEffect, useMemo } from 'react';
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
        try {
            const baseUrl = process.env.REACT_APP_API_BASE_URL;
            if (!baseUrl) throw new Error("REACT_APP_API_BASE_URL is not defined.");

            const res = await fetch(`${baseUrl}/api/auth/login`, {
                method: 'POST',
                credentials: 'omit',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Login failed');

            localStorage.setItem('token', data.access_token);
            localStorage.setItem('role', data.role);
            localStorage.setItem('userId', data.user_id);

            setUser({ token: data.access_token, role: data.role, userId: data.user_id });

            // � Redirect to Home or another valid route
            navigate('/');
        } catch (err) {
            console.error("Login error:", err);
            throw err;
        }
    };

    const register = async (email, password) => {
        try {
            const baseUrl = process.env.REACT_APP_API_BASE_URL;
            if (!baseUrl) throw new Error("REACT_APP_API_BASE_URL is not defined.");

            const res = await fetch(`${baseUrl}/api/auth/register`, {
                method: 'POST',
                credentials: 'omit',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, role: 'User' }),
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Registration failed');

            localStorage.setItem('token', data.token);
            localStorage.setItem('role', 'User');
            localStorage.setItem('userId', data.user_id || '');

            setUser({ token: data.token, role: 'User', userId: data.user_id || '' });

            // � Redirect to Home or Login page after register
            navigate('/');
        } catch (err) {
            console.error("Registration error:", err);
            throw err;
        }
    };

    const logout = () => {
        localStorage.clear();
        setUser(null);
        navigate('/login');
    };

    const value = useMemo(() => ({
        user,
        login,
        register,
        logout
    }), [user]);

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
