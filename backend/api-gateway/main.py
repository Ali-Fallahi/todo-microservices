import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import jwt
from decouple import config

app = FastAPI()

# Configuration
USER_SERVICE_URL = "http://user-service:8000"
TODO_SERVICE_URL = "http://todo-service:8000"
JWT_SECRET_KEY = config("JWT_SIGNING_KEY")

# A client that can make requests to other services
client = httpx.AsyncClient()


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_request(request: Request, path: str):
    destination_service = None

    # 1. Determine the destination service based on the path
    if path.startswith("auth/"):
        destination_service = USER_SERVICE_URL
        path = path.replace("auth/", "api/accounts/", 1)
    elif path.startswith("tasks/"):
        destination_service = TODO_SERVICE_URL
        path = path.replace("tasks/", "api/tasks/", 1)
    else:
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    # 2. Extract user ID from JWT for protected routes
    user_id = None
    if destination_service == TODO_SERVICE_URL:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication credentials were not provided."},
            )

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return JSONResponse(
                    status_code=401, content={"detail": "Invalid token."}
                )
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401, content={"detail": "Token has expired."}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token."})

    # 3. Forward the request to the destination service
    url = f"{destination_service}/{path}"
    headers = dict(request.headers)

    # Add the user ID header for the downstream service
    if user_id:
        headers["X-User-ID"] = str(user_id)

    # Remove host header to avoid conflicts
    headers.pop("host", None)

    data = await request.body()

    try:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=data,
            params=request.query_params,
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.RequestError as e:
        return JSONResponse(
            status_code=503, content={"detail": "Service unavailable.", "error": str(e)}
        )
