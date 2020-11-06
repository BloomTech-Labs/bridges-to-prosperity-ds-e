from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import database, csv_json, csv_api 

app = FastAPI(
    title='Labs28-Team-Spencer',
    description='Lets get it',
    version='0.1',
    docs_url='/',
)

app.include_router(database.router)
app.include_router(csv_json.router)
app.include_router(csv_api.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
