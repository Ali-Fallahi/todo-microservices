ROUTES = [
    {
        # Any path starting with 'auth'
        "path_prefix": "auth",
        "target_service": "http://user-service:8000",
        # Will be rewritten to start with this
        "rewrite_prefix": "/api/accounts",
        "protected": False,  # Auth routes are public
    },
    {
        # Any path starting with 'tasks'
        "path_prefix": "tasks",
        "target_service": "http://todo-service:8000",
        # Will be rewritten to start with this
        "rewrite_prefix": "/api/tasks",
        "protected": True,  # Task routes require a valid token
    },
]
