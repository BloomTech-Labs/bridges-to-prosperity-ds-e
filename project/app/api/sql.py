import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import json
import logging
import random
from fastapi import APIRouter

log = logging.getLogger(__name__)
router = APIRouter()

#this is to grab the .env file with the credentials 
load_dotenv()

HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")

@router.get('/all_data')
async def get_all_data():
    """
    Returns all records from the database as text  

    These records can be found in the bridges_1.csv file

    # Response
    - ID
    - country
    - province
    - district
    - district_id
    - sector
    - sector_id
    - cell
    - cell_id
    - village
    - name
    - project_code
    - type
    - stage
    - sub_stage
    - individuals_directly_served
    - span
    - lat
    - long
    - community_served_1
    - community_served_1_id
    - community_served_2
    - community_served_2_id
    - community_served_3
    - community_served_3_id
    - community_served_4
    - community_served_4_id
    - community_served_5
    - community_served_5_id
    - form
    - case_safe_id
    - opportunity_id
    - inc_income
    - inc_income_rwf
    - inc_income_usd
    """
    # connect to the database
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

    # fetch all the records from the database
    def fetch_all():
        
        cursor = conn.cursor()
        query = f"""SELECT * FROM "Bridges";"""
        cursor.execute(query)
        result = cursor.fetchall()
        columns = ['ID', 'country', 'province', 'district', 'district_id', 'sector', 'sector_id', 'cell', 'cell_id', 'village', 'village_id', 'name', 'project_code', 'type', 'stage', 'sub_stage', 'individuals_directly_served', 'span', 'lat', 'long', 'community_served_1', 'community_served_1_id',
                    'community_served_2', 'community_served_2_id', 'community_served_3', 'community_served_3_id', 'community_served_4', 'community_served_4_id', 'community_served_5', 'community_served_5_id', 'form', 'case_safe_id', 'opportunity_id', 'inc_income', 'inc_income_rwf', 'inc_income_usd']
        df = pd.DataFrame(result, columns=columns)
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed

    #this if statement is used to call back to the fetch_all above 
    #     
    if conn is not None:
        print('We have lift off')
        data = fetch_all()
        conn.close()
        return data
    else:
        print('ERROR')

@router.get('/get_all_project_codes')
async def get_all_project_codes():
    """
    Returns all project codes in the database  

    These project codes can be found in the bridges_1.csv file
    """
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

    # create a function to return all the project codes
    def fetch_project_codes():
        cursor = conn.cursor()
        query = f"""SELECT project_code FROM "Bridges";"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result


    if conn is not None:
        print('We have lift off')
        data = fetch_project_codes()
        conn.close()
        return data
    else:
        print('ERROR')


@router.post('/get_one_project')
async def get_record(project_code):
    """
    Returns the information of a single project_code from the database  

    These records can be found in the bridges_1.csv file      

    If you don't have a project_code in mind, try **1007561**  

    That should return the following information for ID 323

    # Response
    - ID
    - country
    - province
    - district
    - district_id
    - sector
    - sector_id
    - cell
    - cell_id
    - village
    - name
    - project_code
    - type
    - stage
    - sub_stage
    - individuals_directly_served
    - span
    - lat
    - long
    - community_served_1
    - community_served_1_id
    - community_served_2
    - community_served_2_id
    - community_served_3
    - community_served_3_id
    - community_served_4
    - community_served_4_id
    - community_served_5
    - community_served_5_id
    - form
    - case_safe_id
    - opportunity_id
    - inc_income
    - inc_income_rwf
    - inc_income_usd
    """
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)    


    # create a function to access data from db and store it as a dataframe
    def fetch_query_given_project_and_columns(project_code):
        cursor = conn.cursor()
        query = f"""SELECT * FROM "Bridges" WHERE project_code = '{project_code}';"""
        cursor.execute(query)
        result = cursor.fetchall()
        columns = ['ID', 'country', 'province', 'district', 'district_id', 'sector', 'sector_id', 'cell', 'cell_id', 'village', 'village_id', 'name', 'project_code', 'type', 'stage', 'sub_stage', 'individuals_directly_served', 'span', 'lat', 'long', 'community_served_1', 'community_served_1_id',
                    'community_served_2', 'community_served_2_id', 'community_served_3', 'community_served_3_id', 'community_served_4', 'community_served_4_id', 'community_served_5', 'community_served_5_id', 'form', 'case_safe_id', 'opportunity_id', 'inc_income', 'inc_income_rwf', 'inc_income_usd']
        df = pd.DataFrame(result, columns=columns)
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed



    if conn is not None:
        print('We have lift off')
        data = fetch_query_given_project_and_columns(project_code)
        conn.close()
        return data
    else:
        print('ERROR')
@router.post('/prediction')
async def get_record(project_code):
    '''
    Returns the the model's prediction of whether or not the site is suitable or unsuitable  

    These predictions can be found in our bridges_2.csv file  

    **1007561 should return "Unsuitable"**
    '''
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

    cursor = conn.cursor()
    query = f"""SELECT * FROM "dataz" WHERE project_code = '{project_code}';"""
    cursor.execute(query)
    result = cursor.fetchall()
    result = result[0][-1]
    return result


@router.post('/probability')
async def get_record(project_code):
    '''
    Returns the the probability that a site is suitable or unsuitable for building according to the model  

    These probabilities can be found in our bridges_3.csv file  
    
    **1007561 should return 0.25086823**
    '''
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

    cursor = conn.cursor()
    query = f"""SELECT * FROM "likelihood_predictions" WHERE project_code = '{project_code}';"""
    cursor.execute(query)
    result = cursor.fetchall()
    result = result[0][-1]
    return result