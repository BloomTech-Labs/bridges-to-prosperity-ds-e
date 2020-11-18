import logging
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

log = logging.getLogger(__name__)
router = APIRouter()

# get the csv file
data_folder = Path('app/api/data/')
csv_file = data_folder / "cleaned4.csv"


@router.get('/csv')
async def get_csv():
    """
    Returns the cleaned csv (app/api/data/cleaned4.csv) of bridge data as a downloadable .txt file
    """


    return FileResponse(csv_file, media_type='.csv', filename='CleanedCSV.csv')
