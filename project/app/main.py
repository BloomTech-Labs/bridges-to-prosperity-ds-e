from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import database

app = FastAPI(
    title='Labs28-Bridges-Team-Spencer',
    description='Making the world a better place one bridge at a time',
    version='0.1',
    docs_url='/',
)

app.include_router(database.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
