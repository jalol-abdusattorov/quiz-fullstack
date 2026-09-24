import jwt
import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv, find_dotenv
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from routes.users import router as users_router
from auth.routes.auth_router import auth_router
from routes.quizzes import router as quizzes_router
from routes.questions import router as questions_router
from routes.results import router as results_router

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
public_endpoints = ["/docs", "/openapi.json", "/api/auth/login", "/users", "/"]

openapi_tags = [
    {
        "name": "Users",
        "description": "User operaqtions"
    },
    {
        "name": "Auth",
        "description": "Authorization"
    },
    {
        "name": "Quizzes",
        "description": "Quizzes"
    },
    {
        "name": "Questions",
        "description": "Questions"
    },
    {
        "name": "Results",
        "description": "Results"
    }
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Open the public endpoints because they dont need auth
        if request.url.path in public_endpoints:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Not Authorized"})

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # Inject user, token payload and admin status into state for auth 
            request.state.user = payload
            request.state.token_string = token
            request.state.admin = payload['admin']

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=403, content={"detail": "Token has expired"})
        except jwt.PyJWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        return await call_next(request)

app = FastAPI(openapi_tags=openapi_tags, title="Quiz Backend")
app.add_middleware(AuthMiddleware)

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://192.168.100.103:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

@app.get("/")
def get():
    return {"message": "homepage"}

app.include_router(users_router, tags=["Users"])
app.include_router(auth_router, prefix="/api",)
app.include_router(quizzes_router, tags=["Quizzes"])
app.include_router(questions_router, tags=["Questions"])
app.include_router(results_router, tags=["Results"])