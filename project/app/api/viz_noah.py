from fastapi import APIRouter
import pandas as pd
import plotly.express as px
from pathlib import Path 

router = APIRouter()

data_folder = Path('app/api/data/')
csv_file = data_folder / "viz_df.csv"
csv2_file = data_folder/"neighbors_data.csv"
viz_df = pd.read_csv(csv_file, index_col= [0])
neighbors_df = pd.read_csv(csv2_file, index_col=[0])

@router.get('/viz/{knn_visualization}')
async def viz(project_code: str):
    lst = []
    for i in range(0,62): #iterate through neighbors dictionary to grab the neighbors of the project code 
        if neighbors_df.loc[project_code][i] != None:
        #append neighbors to list 
            lst.append(neighbors_df.loc[project_code][i])
    #create a dataframe with only the rows that match the values in the lst created above   
    knn_df = viz_df.loc[viz_df['Project_code'].isin(lst)]
    fig = px.scatter(knn_df, x='Unsuitable', y='Suitable',
                    hover_data=['Project_code','Suitable','Unsuitable', 'Bridge_classification',
                                'Crossing', 'Days_per_year_river_is_flooded',
                                'River_crossing_injuries_in_last_3_years', 'Cell_service_quality',
                                '4WD_Accessibility', 'Bridge_Type',
                                'Proposed_Bridge_Location(GPS)(Latitude)',
                                'Proposed_Bridge_Location(GPS)(Longitude)',
                                'Height_differential_between_banks', 
                                'Estimated_span(m)'])
    
    fig.update_traces(marker_size=12, marker_line_width=1.5)
    fig.update_layout(legend_orientation='h')
    #create new fig for single input 
    fig2 = px.scatter(viz_df[viz_df['Project_code'] == project_code], x='Unsuitable', y='Suitable',
                    hover_data=['Project_code','Suitable','Unsuitable', 'Bridge_classification',
                                'Crossing', 'Days_per_year_river_is_flooded',
                                'River_crossing_injuries_in_last_3_years', 'Cell_service_quality',
                                '4WD_Accessibility', 'Bridge_Type',
                                'Proposed_Bridge_Location(GPS)(Latitude)',
                                'Proposed_Bridge_Location(GPS)(Longitude)',
                                'Height_differential_between_banks', 
                                'Estimated_span(m)'])
    #change color of input bridge
    fig2.update_traces(marker=dict(color='red'))
    #change color from default value 
    fig.update_traces(marker=dict(color='green'))
    #merge figs 
    fig.add_trace(fig2.data[0])
    # Return Plotly figure as JSON string
    return fig.to_json()
