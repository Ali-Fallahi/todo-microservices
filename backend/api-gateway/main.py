# English Comments as requested

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import jwt
from decouple import config
import logging
from logstash_async.handler import AsynchronousLogstashHandler
import time
import uuid
from routing_config import ROUTES  # Import our clean routing map

# --- Logging Configuration ---
host = "logstash"
port = 5044
gateway_logger = logging.getLogger("api_gateway_logger")
gateway_logger.setLevel(logging.INFO)
gateway_logger.addHandler(AsynchronousLogstashHandler(host, port, database_path=None))

# --- FastAPI App Initialization ---
app = FastAPI()

# --- CORS Middleware ---
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Structured Logging Middleware ---
@app.middleware("http")
async def structured_logging_middleware(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())

    response = await call_next(request)

    duration = time.time() - start_time

    user_id = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                config("JWT_SIGNING_KEY"),
                algorithms=["HS256"],
                options={"verify_signature": False},
            )
            user_id = payload.get("user_id")
        except jwt.PyJWTError:
            user_id = "invalid_token"

    log_data = {
        "log_source": "api_gateway",
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "duration_ms": int(duration * 1000),
        "request_id": request_id,
        "user_id": user_id,
        "remote_addr": request.client.host,
    }
    gateway_logger.info("Gateway request handled", extra={"structured_log": log_data})
    return response


# --- Configuration Constants ---
JWT_SECRET_KEY = config("JWT_SIGNING_KEY")
client = httpx.AsyncClient()


# --- Main Smart Router ---
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_request(request: Request, path: str):

    # 1. Find the correct route from our configuration map
    matched_route = None
    for route in ROUTES:
        if path.startswith(route["path_prefix"]):
            matched_route = route
            break

    if not matched_route:
        return JSONResponse(status_code=404, content={"detail": "Endpoint not found"})

    # 2. Authenticate if the route is marked as protected
    user_id = None
    if matched_route["protected"]:
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
                    status_code=401, content={"detail": "Invalid token payload."}
                )
        except jwt.PyJWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token signature or format."},
            )

    # 3. Correctly rewrite the path to avoid double slashes
    rest_of_path = path[
        len(matched_route["path_prefix"]) :
    ]  # Safely get the rest of the path
    target_path = matched_route["rewrite_prefix"] + rest_of_path

    url = f"{matched_route['target_service']}{target_path}"

    headers = dict(request.headers)
    if user_id:
        headers["X-User-ID"] = str(user_id)
    headers.pop("host", None)

    data = await request.body()

    # 4. Forward the request to the correct downstream service
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
        gateway_logger.error(f"Service unavailable: {str(e)}")
        return JSONResponse(status_code=503, content={"detail": "Service unavailable."})
