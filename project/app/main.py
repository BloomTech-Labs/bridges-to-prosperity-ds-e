from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import sql, csv_api, viz, viz_noah, viz_nate3

app = FastAPI(
    title='Labs28-Team-Spencer',
    description="A REST API that delivers data assets to the front and backend of [our team's webapp](https://e.bridgestoprosperity.dev/) for Bridges to Prosperity",
    version='1.1',
    docs_url='/',
)

app.include_router(sql.router)
app.include_router(csv_api.router)
app.include_router(viz_noah.router)
app.include_router(viz_nate3.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
def healthcheck():
    return "OK"

if __name__ == '__main__':
    uvicorn.run(app)
