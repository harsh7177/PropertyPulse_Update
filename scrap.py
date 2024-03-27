import requests
import json
import pandas as pd
import streamlit as st

def scrap_city(loc1):
    endpoint_url = "https://stgpxl9ok3.execute-api.us-east-1.amazonaws.com/dev"
    post = {"loc": str(loc1),"href":"None"}
    response = requests.post(endpoint_url, json=post)
    z=response.text
    response_body_dict = json.loads(z)
    dic=json.loads(response_body_dict['body'])

    df=pd.DataFrame.from_dict(dic)
    df=df.dropna()
    return df

def sub_scrap(href,pages):
    endpoint_url = "https://stgpxl9ok3.execute-api.us-east-1.amazonaws.com/dev"
    post = {"loc": "None","href":href,"page":pages}
    response = requests.post(endpoint_url, json=post).text
    response_body_dict = json.loads(response)
    try:
        dic=json.loads(response_body_dict['body'])
        df=pd.DataFrame.from_dict(dic)
        return df
    except Exception as e:
        return e
    

def get_href_pages(href):
    endpoint_url = "https://stgpxl9ok3.execute-api.us-east-1.amazonaws.com/dev"
    post = {"loc": "None","href":href,"page":"True"}
    response = requests.post(endpoint_url, json=post).text
    response_body_dict = json.loads(response)
    try:
        return response_body_dict['pages']
    except Exception as e:
        return response_body_dict
    
    
        
    
