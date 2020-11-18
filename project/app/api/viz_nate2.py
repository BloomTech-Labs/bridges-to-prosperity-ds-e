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
async def vizn2(project_code: str):
    '''
    Returns a plotly scatterplot of the overall impact score by the number of individuals served.  

    The graph should look something like viz2.PNG found in project/app/api/images

    Don't have a project code in mind? Try **1007561**    
    '''

    # connect to the database
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
    cursor = conn.cursor()

    # query the database and close the connection
    query = f"""SELECT * FROM "impact";"""
    query2 = f"""SELECT * FROM "impact" WHERE project_code = '{project_code}'"""

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.execute(query2)
    result2 = cursor.fetchall()

    conn.close()

    # create a dataframe of all of the data from the first result
    columns = ['project_code', 'ind_directly_served', 'days_flooded_per_year', 'market_blocked',
        'education_blocked', 'healthcare_blocked', 'river_deaths_3_yrs', 'river_inj_3yrs', 'impact_score', 
        'health_impact', 'education_impact', 'market_impact']
    df = pd.DataFrame(result, columns=columns)

    # create a dataframe of just the single bridge site from the give project code
    single_df = pd.DataFrame(result2, columns=columns)


    columns = ['ind_directly_served',
            'days_flooded_per_year', 
            'river_deaths_3_yrs',
            'river_inj_3yrs',
            'impact_score'] 

    values = []

    # get the values from the individual bridge site
    for feature in columns:
        value = single_df[feature][0]
        value = value[:5]
        value = float(value)
        values.append(value)

    # make a new df that will show the single bridge site on our scatterplot
    columns = ['Individuals Served', 'Days Per Year River is Flooded',
            'River crossing deaths in last 3 years', 
            'River crossing injuries in last 3 years', 
            'Overall Impact Score']
    new_c = {'Category':columns, 'Actual':values}
    new_df = pd.DataFrame(data=new_c)

    # this adds all of the blue dots to the scatterplot
    fig = go.Figure(go.Scatter(
                x=df["impact_score"], 
                y=df["ind_directly_served"],
                name='Other Sites',
                orientation='h',
                mode = 'markers',
                marker=dict(
                color='rgba(0, 158, 228, 1)',
                line=dict(
                    color='Black',
                    width=.5)),
                text=df['project_code'],
                hovertemplate = "<b>Project Code: %{text}</b><br><br>" +
                "Individuals Directly Served: %{y}<br><br>" +
                "Overall Impact Score: %{x}"
                ))

    # add the orange dot
    fig.add_trace(
        go.Scatter(
            
            mode='markers',
            x=[values[4]],
            y=[values[0]],
            name='Current Site',
            marker = dict(
                color='rgba(250, 140, 48, 1)',
                size = 15,
                line=dict(
                    color='Black',
                    width=2
                )
            
            ),
        text=df['project_code'],
        hovertemplate = "<b>Project Code: %{text}</b><br><br>" +
            "Individuals Directly Served: %{y}<br><br>" +
            "Overall Impact Score: %{x}"  
        )
    )

    fig.update_xaxes(
            title_text = "Overall Impact Score",
            title_font = {"size": 14},
            title_standoff = 25)

    fig.update_yaxes(
            title_text = "Individuals Directly Served",
            title_font = {"size": 14},
            title_standoff = 25)

    return fig.to_json()


