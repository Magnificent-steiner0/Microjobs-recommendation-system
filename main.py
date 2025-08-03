from fastapi import FastAPI
from routers import refresh, recommend 
from testing import jobs, user

app = FastAPI()

app.include_router(refresh.router)
app.include_router(recommend.router)
app.include_router(jobs.router)
app.include_router(user.router)