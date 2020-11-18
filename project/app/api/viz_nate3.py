from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import os
from dotenv import load_dotenv
import json
from pathlib import Path

router = APIRouter()

# load variables to connect to Postgresql database
load_dotenv()

HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")

# get the png file
data_folder = Path('app/api/images/')
image = data_folder / "viz3.png"

@router.get('/viz_nate3/{key_metrics}')
async def vizn3(project_code: str):
    '''
    Returns a plotly visualization of key impact metrics such as  
    - Overall Impact Score  
    - River crossing injuries in last 3 years  
    - River crossing deaths in last 3 years  
    - Days per year river is flooded  
    - Individuals served  

    These metrics are measured by percentile  



    **THE OVERALL IMPACT SCORE**  
    
    The overall impact score is an aggregate of the market, education, and health impact scores.  
    Market, education, and health impact scores are calculated using the following formula:  

    days per year the river is flooded / 365 * binary * 100 / 3  

    For example, let's say that the river was flooded 60 days per year and that the river blocked access to  
    education and healthcare but not markets. The formulas would look like this:

    Education impact = 60 / 365 * 1 * 100 / 3  = 5.48
    Health impact = 60 / 365 * 1 * 100 / 3 = 5.48  
    Market impact = 60 / 365 * 0 * 100 / 3 = 0  

    We find the overall impact score by adding these three impact scores together:  

    Overall impact score = 5.48 + 5.48 + 0 = 10.96  



    The graph should look something like viz3.PNG found in project/app/api/images

    Don't have a project code in mind? Try **1007561**        
    '''

    # connect to the database
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
    cursor = conn.cursor()

    # query the database and close the connection
    query = f"""SELECT * FROM "impact" WHERE project_code = '{project_code}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    # create a dataframe from the result
    columns = ['project_code', 'ind_directly_served', 'days_flooded_per_year', 'market_blocked',
        'education_blocked', 'healthcare_blocked', 'river_deaths_3_yrs', 'river_inj_3yrs', 'impact_score', 
        'health_impact', 'education_impact', 'market_impact']
    df = pd.DataFrame(result, columns=columns)

    columns = ['ind_directly_served',
            'days_flooded_per_year', 
            'river_deaths_3_yrs',
            'river_inj_3yrs',
            'impact_score'] 
    values = []

    for feature in columns:
        value = df[feature][0]
        value = value[:5]
        value = float(value)
        values.append(value)

    # adjust values
    # find the max value of each column
    maxes = [65160.0, 365.0, 50.0, 300.0, 100.0]
    
    adj_values = []
    counter = 0
    for value in values:
        new_val = value/maxes[counter]*100
        adj_values.append(new_val)
        counter +=1

    # make a df
    columns = ['Individuals Served', 'Days Per Year River is Flooded',
            'River crossing deaths in last 3 years', 
            'River crossing injuries in last 3 years', 
            'Overall Impact Score']
    possible = [100, 100, 100, 100,100]
    new_c = {'Category':columns, 'Actual':values, 'Score':adj_values, 'Possible': possible}
    new_df = pd.DataFrame(data=new_c)

    # create the visualization
    fig = go.Figure(go.Bar(
            x=new_df['Score'], 
            y=columns,
            orientation='h',
            text = new_df['Actual'],
            marker=dict(
              color='rgba(0, 158, 228, 1)',
              line=dict(color='rgba(58, 71, 80, 1.0)', width=2)),
            hovertemplate = 
            "<b>%{text} %{y}</b><br><br>" + 
            "Percentile: %{x}"
            ))

    fig.update_xaxes(
            title_text = "Key Impact Metrics (Percentile)",
            title_font = {"size": 20},
            title_standoff = 25,
            range=[0,100]
            )

    fig.update_layout(barmode='stack')

    return fig.to_json()




