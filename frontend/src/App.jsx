import React, { useContext } from 'react';
import { Routes, Route, Navigate, Link } from 'react-router-dom';
import AuthContext from './context/AuthContext';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';
import './App.css';

// کامپوننت صفحه اصلی اپلیکیشن (محافظت شده)
const TodoPage = () =>
{
  const { logout } = useContext(AuthContext);
  return (
    <div className="App">
      <header className="App-header">
        <h1>Todo List</h1>
        <p>Your tasks will appear here soon!</p>
        <button onClick={logout} className="form-button" style={{ maxWidth: '200px' }}>
          Logout
        </button>
      </header>
    </div>
  );
};

// کامپوننت صفحه احراز هویت (عمومی)
const AuthPage = ({ isLogin = true }) =>
{
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to our TODO App</h1>
        {isLogin ? <LoginForm /> : <RegistrationForm />}
        <p style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <Link to={isLogin ? "/register" : "/login"} style={{ color: '#61dafb' }}>
            {isLogin ? "Register" : "Login"}
          </Link>
        </p>
      </header>
    </div>
  );
};

// روتر اصلی اپلیکیشن
function App()
{
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <Routes>
      <Route
        path="/login"
        element={!isAuthenticated ? <AuthPage isLogin={true} /> : <Navigate to="/" />}
      />
      <Route
        path="/register"
        element={!isAuthenticated ? <AuthPage isLogin={false} /> : <Navigate to="/" />}
      />
      <Route
        path="/"
        element={isAuthenticated ? <TodoPage /> : <Navigate to="/login" />}
      />
      {/* A catch-all route to redirect to login if no other route matches */}
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

export default App;