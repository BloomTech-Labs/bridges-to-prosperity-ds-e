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

@router.get('/viz_nate1/{impact_score}')
async def vizn1(project_code: str):
    '''
    Returns a plotly visualization of the      
    - Overall    
    - Market   
    - Education   
    - and Health   
    impact scores.  

    Market, education, and health impact scores are calculated using the following formula:  

    days per year the river is flooded / 365 * binary * 100 /3  

    For example, let's say that the river was flooded 60 days per year and that the river blocked access to  
    education and healthcare but not markets. The formulas would look like this:

    Education impact = 60 / 365 * 1 * 100 / 3  = 5.48
    Health impact = 60 / 365 * 1 * 100 / 3 = 5.48  
    Market impact = 60 / 365 * 0 * 100 / 3 = 0  

    We find the overall impact score by adding these three impact scores together:  

    Overall impact score = 5.48 + 5.48 + 0 = 10.96  

    The graph should look something like viz1.PNG found in project/app/api/images

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

    # make a sub dataframe of the values we want to graph
    columns = ['health_impact', 'education_impact', 'market_impact', 'impact_score'] 
    values = []

    for feature in columns:
        value = df[feature][0]
        value = value[:5]
        value = float(value)
        values.append(value)


    columns = ['Health', 'Education', 'Market', 'Overall']
    possible = [33.33, 33.33, 33.33, 100]
    new_c = {'Category':columns, 'Score':values, 'Possible': possible}
    new_df = pd.DataFrame(data=new_c)

    # create the visualization
    fig = go.Figure(go.Bar(
            x=new_df['Score'], 
            y=columns,
            name='Actual Impact Score',
            text=values,
            textposition='auto',
            orientation='h',
            marker=dict(
              color='rgba(0, 158, 228, 1)',
              line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )))

    fig.add_trace(go.Bar(
        y=columns,
        x=new_df['Possible']-new_df['Score'],
        name='Potential',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.1)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))

    fig.update_xaxes(
            title_text = "Impact Scores",
            title_font = {"size": 20},
            title_standoff = 25)

    fig.update_layout(barmode='stack')

    return fig.to_json()




