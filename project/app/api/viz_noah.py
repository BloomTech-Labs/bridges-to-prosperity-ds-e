from fastapi import APIRouter
import pandas as pd
import plotly.express as px
from collections import deque
import math 
from pathlib import Path 

router = APIRouter()

data_folder = Path('app/api/data/')
csv_file = data_folder / "viz_data.csv"
viz_df = pd.read_csv(csv_file)

@router.get('/viz/{statecode}')
async def viz(project_code: str):
    row = viz_df.loc[viz_df['Project_code'] ==project_code]
    prob_0 = row['Probabilities_0'] 
    prob_1 = row['Probabilities_1']
    neighbors = {'Unsuitable':deque(maxlen=3), 'Suitable':deque(maxlen=3), 'Bridge_classification': deque(maxlen=3),
    'Crossing':deque(maxlen=3), 'Days_per_year_river_is_flooded':deque(maxlen=3) ,
    'River_crossing_injuries_in_last_3_years': deque(maxlen=3), 'Cell_service_quality':deque(maxlen=3),
    '4WD_Accessibility':deque(maxlen=3), 'Bridge_Type':deque(maxlen=3),
    'Proposed_Bridge_Location(GPS)(Latitude)':deque(maxlen=3),
    'Proposed_Bridge_Location(GPS)(Longitude)':deque(maxlen=3),
    'Height_differential_between_banks':deque(maxlen=3), 'Estimated_span(m)':deque(maxlen=3)}
               
  
  
  
    for i in viz_df['Probabilities_0']: 
        if (math.isclose(i, prob_0,rel_tol=.01) == True):
            neighbors['Unsuitable'].append(i)
            neighbors['Bridge_classification'].append(row['Bridge_classification'])
            neighbors['Crossing'].append(row['Crossing'])
            neighbors['Days_per_year_river_is_flooded'].append(row['Days_per_year_river_is_flooded'])
            neighbors['River_crossing_injuries_in_last_3_years'].append(row['River_crossing_injuries_in_last_3_years'])
            neighbors['Cell_service_quality'].append(row['Cell_service_quality'])
            neighbors['4WD_Accessibility'].append(row['4WD_Accessibility'])
            neighbors['Bridge_Type'].append(row['Bridge_Type'])
            neighbors['Proposed_Bridge_Location(GPS)(Latitude)'].append(row['Proposed_Bridge_Location(GPS)(Latitude)'])
            neighbors['Proposed_Bridge_Location(GPS)(Longitude)'].append(row['Proposed_Bridge_Location(GPS)(Longitude)'])
            neighbors['Height_differential_between_banks'].append(row['Height_differential_between_banks'])
            neighbors['Estimated_span(m)'].append(row['Estimated_span(m)'])

  
    for i in viz_df['Probabilities_1']: 
        if (math.isclose(i, prob_1,rel_tol=.01) == True):
            neighbors['Suitable'].append(i)
            neighbors['Bridge_classification'].append(row['Bridge_classification'])
            neighbors['Crossing'].append(row['Crossing'])
            neighbors['Days_per_year_river_is_flooded'].append(row['Days_per_year_river_is_flooded'])
            neighbors['River_crossing_injuries_in_last_3_years'].append(row['River_crossing_injuries_in_last_3_years'])
            neighbors['Cell_service_quality'].append(row['Cell_service_quality'])
            neighbors['4WD_Accessibility'].append(row['4WD_Accessibility'])
            neighbors['Bridge_Type'].append(row['Bridge_Type'])
            neighbors['Proposed_Bridge_Location(GPS)(Latitude)'].append(row['Proposed_Bridge_Location(GPS)(Latitude)'])
            neighbors['Proposed_Bridge_Location(GPS)(Longitude)'].append(row['Proposed_Bridge_Location(GPS)(Longitude)'])
            neighbors['Height_differential_between_banks'].append(row['Height_differential_between_banks'])
            neighbors['Estimated_span(m)'].append(row['Estimated_span(m)'])
        
  
  
  
  
  
  
    fig = px.scatter(neighbors, x='Unsuitable', y='Suitable',
    hover_data=['Suitable','Unsuitable', 'Bridge_classification','Crossing', 'Days_per_year_river_is_flooded',
    'River_crossing_injuries_in_last_3_years', 'Cell_service_quality',
    '4WD_Accessibility', 'Bridge_Type',
    'Proposed_Bridge_Location(GPS)(Latitude)',
    'Proposed_Bridge_Location(GPS)(Longitude)',
    'Height_differential_between_banks', 
    'Estimated_span(m)'] )
    fig.update_traces(marker_size=12, marker_line_width=1.5)
    fig.update_layout(legend_orientation='h')
  
  
    print(f'Unsuitability of given project: {prob_0[0]}\n Suitability of given project: {prob_1[0]} ')


    # Return Plotly figure as JSON string
    return fig.to_json()
