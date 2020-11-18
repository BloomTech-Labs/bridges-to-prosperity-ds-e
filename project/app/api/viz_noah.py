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
    Returns a plotly scatterplot visualization of sites that have a similar probability of either being “Suitable” or “Unsuitable” to build a bridge. 
    The goal of this visualization is to allow the stakeholders involved in bridge location planning and selecting process to find patterns in the features that each location has that will ultimately allow their processing time to decrease over time. 
    The yellow dot is the site project number being input, while the green dots are the nearest neighbors to this location according to their probabilities. 
    The probability for each site is measured according to features input into the semi-supervised model such as: 
    -Bridge Classification
    -Crossing (current method of crossing the water)
    -Days per year river is flooded
    -River crossing deaths in last 3 years
    -River crossing injuries in last 3 years
    -Cell service quality
    -4WD Accessibility
    -Bridge Type
    -Proposed Bridge Location (GPS) (Latitude)
    -Proposed Bridge Location (GPS) (Longitude)
    -Height differential between banks (meters)
    -Estimated span (meters)
    The semi-supervised model used to gather the probabilities of each site was 
    Label propagation from the skit-learn library. Label propagation is a machine learning algorithm that assigns labels to previously unlabeled data points 
    and since we were working with a dataset that contained a majority of unlabeled instances it allowed us to extract more information from the data given.
    
    Use **1007561** as an example
    '''
    project_code_row = neighbors_data.loc[neighbors_data['main'] == f"{project_code}"]
    #transform row into single column to make it easier to manipulate as a list
    transformed_project_code = project_code_row.T.dropna()
    #name column PG 
    transformed_project_code.columns = ["PG"]
    #convert floats and int to single data type 
    transformed_project_code["PG"] = transformed_project_code["PG"].astype(int)
    #convert back str 
    transformed_project_code["PG"] = transformed_project_code["PG"].astype(str)
    #convert pandas series to list for manipulation purposes
    lst =list(transformed_project_code["PG"])
    #grab only the rows that have the project code (nearest neighbors) for plotly graph 
    knn_df = viz_df.loc[viz_df['Project_code'].isin(lst)]
    #create a column that will contain the input project code that will be colored differently in the graph. See documentation for np.where() 
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
