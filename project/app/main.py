from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

<<<<<<< HEAD
from app.api import sql, csv_api, viz_noah 
=======
from app.api import sql, csv_api, viz 

>>>>>>> 89615138b7a091262834a29ab2fcc04ef4964101

app = FastAPI(
    title='Labs28-Team-Spencer',
    description="A REST API that delivers data assets to the front and backend of [our team's webapp](https://e.bridgestoprosperity.dev/) for Bridges to Prosperity",
    version='1.1',
    docs_url='/',
)

app.include_router(sql.router)
app.include_router(csv_api.router)
<<<<<<< HEAD
app.include_router(viz_noah.router)
=======
app.include_router(viz.router)
>>>>>>> 89615138b7a091262834a29ab2fcc04ef4964101

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
