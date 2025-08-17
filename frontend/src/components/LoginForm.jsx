import React, { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import api from '../api';

const LoginForm = () =>
{
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [message, setMessage] = useState('');
    const [isError, setIsError] = useState(false);
    const { login } = useContext(AuthContext);

    const handleChange = (e) =>
    {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        setMessage('');
        setIsError(false);
        try
        {
            const response = await api.post('/auth/token/', formData);
            login(response.data.access, response.data.refresh);
        } catch (error)
        {
            console.error('Login failed:', error.response ? error.response.data : error.message);
            setIsError(true);
            setMessage('Login failed. Please check your username and password.');
        }
    };

    return (
        <div className="form-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" className="form-input" value={formData.username} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" className="form-input" value={formData.password} onChange={handleChange} required />
                </div>
                <button type="submit" className="form-button">Login</button>
            </form>
            {message && <p className={`message ${isError ? 'error' : 'success'}`}>{message}</p>}
        </div>
    );
};

export default LoginForm;