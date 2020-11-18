from fastapi import APIRouter
import pandas as pd
import plotly.express as px
from pathlib import Path 
import numpy as np 

router = APIRouter()

data_folder = Path('app/api/data/')
csv_file = data_folder / "viz_df.csv"
csv2_file = data_folder/"neighbors_data_updated.csv"
viz_df = pd.read_csv(csv_file, index_col= [0])
neighbors_data = pd.read_csv(csv2_file, index_col=[0])

@router.get('/viz_noah/{knn_visualization}')
async def viz(project_code: str):
    '''
    Returns a nearest neighbors visualization of similar bridge sites  
    
    Use **1007561** as an example
    '''
    project_code_row = neighbors_data.loc[neighbors_data['main'] == f"{project_code}"]
    transformed_project_code = project_code_row.T.dropna()
    transformed_project_code.columns = ["PG"]
    transformed_project_code["PG"] = transformed_project_code["PG"].astype(int)
    transformed_project_code["PG"] = transformed_project_code["PG"].astype(str)
    lst =list(transformed_project_code["PG"])
    knn_df = viz_df.loc[viz_df['Project_code'].isin(lst)]
    knn_df["main"] = np.where(knn_df['Project_code']==f'{project_code}', 'selected', 'neighbors')
    
    fig = px.scatter(knn_df, x='Unsuitable', y='Suitable',
                        hover_data=['Project_code','Suitable','Unsuitable', 'Bridge_classification',
                                'Crossing', 'Days_per_year_river_is_flooded',
                                    'River_crossing_injuries_in_last_3_years', 'Cell_service_quality',
                                    '4WD_Accessibility', 'Bridge_Type',
                                    'Proposed_Bridge_Location(GPS)(Latitude)',
                                    'Proposed_Bridge_Location(GPS)(Longitude)',
                                    'Height_differential_between_banks', 
                                    'Estimated_span(m)'], color = knn_df["main"]
                                , color_discrete_map={"selected":"#F6D143",
                                                        "neighbors": "#79EC7D"}
                    )
    # Return Plotly figure as JSON string
    return fig.to_json()
