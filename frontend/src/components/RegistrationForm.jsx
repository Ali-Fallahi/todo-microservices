import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api'; // استفاده از سرویس api مرکزی

const RegistrationForm = () =>
{
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });
    const [message, setMessage] = useState('');
    const [isError, setIsError] = useState(false);
    const navigate = useNavigate();

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
            await api.post('/auth/register/', formData);
            setMessage('Registration successful! Redirecting to login...');
            setTimeout(() =>
            {
                navigate('/login'); // هدایت به صفحه لاگین
            }, 2000);
        } catch (error)
        {
            console.error('Registration failed:', error.response ? error.response.data : error.message);
            setIsError(true);
            setMessage('Registration failed. Please try a different username or email.');
        }
    };

    return (
        <div className="form-container">
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" className="form-input" value={formData.username} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label>Email:</label>
                    <input type="email" name="email" className="form-input" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" className="form-input" value={formData.password} onChange={handleChange} required />
                </div>
                <button type="submit" className="form-button">Register</button>
            </form>
            {message && <p className={`message ${isError ? 'error' : 'success'}`}>{message}</p>}
        </div>
    );
};

export default RegistrationForm;