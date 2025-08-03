from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import refresh, recommend 
from testing import jobs, user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://your-backend-domain.com"], restrict to backend's domain only
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.include_router(jobs.router)
# app.include_router(user.router)

app.include_router(refresh.router)
app.include_router(recommend.router)