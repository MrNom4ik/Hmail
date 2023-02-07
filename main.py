from fastapi import FastAPI
from api.router import router as router_api

app = FastAPI()

app.include_router(router_api, prefix='/api')
