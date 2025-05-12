const BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const login = async (email, password) => {
    const res = await fetch(`${BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });

    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.message || 'Login failed');
    }

    return data;
};
