from fastapi import FastAPI
from routers import refresh, recommend 
app = FastAPI()

app.include_router(refresh.router)
app.include_router(recommend.router)