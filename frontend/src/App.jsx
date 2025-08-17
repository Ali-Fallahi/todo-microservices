import React, { useContext } from 'react';
import { Routes, Route, Navigate, Link } from 'react-router-dom';
import AuthContext from './context/AuthContext';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';
import TodoPage from './pages/TodoPage'; // <-- فقط ایمپورت می‌کنیم
import './App.css';

// کامپوننت صفحه احراز هویت که فرم لاگین یا ثبت‌نام را نمایش می‌دهد
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
      {/* اگر هیچ مسیری پیدا نشد، کاربر را به مسیر اصلی هدایت کن */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default App;