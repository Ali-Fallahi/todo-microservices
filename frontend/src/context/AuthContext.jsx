import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) =>
{
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() =>
    {
        const token = localStorage.getItem('accessToken');
        if (token)
        {
            setIsAuthenticated(true);
        }
    }, []);

    const login = (access, refresh) =>
    {
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
        setIsAuthenticated(true);
    };

    const logout = () =>
    {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;