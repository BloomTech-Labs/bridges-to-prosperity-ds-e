from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import os
from dotenv import load_dotenv
import json

router = APIRouter()

# load variables to connect to Postgresql database
load_dotenv()

HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")

@router.get('/viz_nate2/{ind_served_impact}')
async def vizn2():
    '''
    Returns a plotly scatterplot of the overall impact score by the number of individuals served.  

    The graph should look something like viz2.PNG found in project/app/api/images

    Don't have a project code in mind? Try **1007561**    
    '''

    # connect to the database
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
    cursor = conn.cursor()

    # query the database and close the connection
    query = f"""SELECT * FROM "impact" """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    # create a dataframe from the result
    columns = ['project_code', 'ind_directly_served', 'days_flooded_per_year', 'market_blocked',
        'education_blocked', 'healthcare_blocked', 'river_deaths_3_yrs', 'river_inj_3yrs', 'impact_score', 
        'health_impact', 'education_impact', 'market_impact']
    df = pd.DataFrame(result, columns=columns)

    # cast values to floats
    '''df['impact_score'] = float(df['impact_score'])
    df['ind_directly_served'] = float(df['ind_directly_served'])'''
    counter = 0
    for value in df['impact_score']:
        df['impact_score'][counter] = float(df['impact_score'][counter])
        df['ind_directly_served'][counter] = float(df['ind_directly_served'][counter])
        counter += 1

    # generate scatterplot
    fig = go.Figure(go.Scatter(
            x=df["impact_score"], 
            y=df['ind_directly_served'],
            name='Actual',
            orientation='h',
            mode = 'markers',
            marker=dict(
                color='rgba(0, 158, 228, 1)'),
                text=df['project_code']
            ))

    fig.update_xaxes(
            title_text = "Overall Impact Score",
            title_font = {"size": 14},
            title_standoff = 25)

    fig.update_yaxes(
            title_text = "Individuals Directly Served",
            title_font = {"size": 14},
            title_standoff = 25)

    return fig.to_json()


