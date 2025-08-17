import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import api from '../api'; // سرویس api مرکزی ما

const TodoPage = () =>
{
    const { logout } = useContext(AuthContext);
    const [todos, setTodos] = useState([]);
    const [newTodoTitle, setNewTodoTitle] = useState('');
    const [error, setError] = useState(null);

    // دریافت لیست وظایف هنگام بارگذاری کامپوننت
    useEffect(() =>
    {
        const fetchTodos = async () =>
        {
            try
            {
                const response = await api.get('/tasks/');
                setTodos(response.data);
            } catch (err)
            {
                setError('Could not fetch todos.');
                console.error(err);
            }
        };
        fetchTodos();
    }, []); // [] یعنی این افکت فقط یک بار بعد از رندر اولیه اجرا می‌شود

    // تابع افزودن یک وظیفه جدید
    const addTodo = async (e) =>
    {
        e.preventDefault();
        if (!newTodoTitle.trim()) return;
        try
        {
            const response = await api.post('/tasks/', { title: newTodoTitle });
            setTodos([...todos, response.data]); // افزودن تسک جدید به لیست
            setNewTodoTitle(''); // خالی کردن اینپوت
        } catch (err)
        {
            setError('Could not add todo.');
            console.error(err);
        }
    };

    // تابع حذف یک وظیفه
    const deleteTodo = async (id) =>
    {
        try
        {
            await api.delete(`/tasks/${id}/`);
            setTodos(todos.filter((todo) => todo.id !== id)); // حذف تسک از لیست
        } catch (err)
        {
            setError('Could not delete todo.');
            console.error(err);
        }
    };

    // تابع تغییر وضعیت تکمیل یک وظیفه
    const toggleTodo = async (id) =>
    {
        const todo = todos.find((t) => t.id === id);
        try
        {
            const response = await api.patch(`/tasks/${id}/`, { completed: !todo.completed });

            setTodos(todos.map((t) => (t.id === id ? response.data : t)));
        } catch (err)
        {
            setError('Could not update todo.');
            console.error(err);
        }
    };

    return (
        <div className="App">
            <div className="main-container">
                <div className="header">
                    <h1>My Tasks</h1>
                    <button onClick={logout} className="logout-button">Logout</button>
                </div>

                {error && <p className="message error">{error}</p>}

                <form onSubmit={addTodo} className="add-todo-form">
                    <input
                        type="text"
                        className="form-input"
                        value={newTodoTitle}
                        onChange={(e) => setNewTodoTitle(e.target.value)}
                        placeholder="Add a new task..."
                    />
                    <button type="submit" className="form-button">Add</button>
                </form>

                <div className="todo-list">
                    {todos.map((todo) => (
                        <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                            <div className="todo-item-title" onClick={() => toggleTodo(todo.id)}>
                                <input type="checkbox" checked={todo.completed} readOnly />
                                <span>{todo.title}</span>
                            </div>
                            <button onClick={() => deleteTodo(todo.id)} className="delete-button">×</button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default TodoPage;