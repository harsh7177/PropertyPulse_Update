import streamlit as st
from streamlit import session_state
from pages import city_page,suburbs_page,about_page
from predict import predict_page
from sql_href import href_tables
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import folium
import base64
import plotly.express as px
from streamlit_folium import folium_static


st.markdown("<h1 style='text-align: center; color: #B64831;'>PropertyPulse</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align:center'> Easy way to get information about RealEstate in your city</p>",unsafe_allow_html=True)
st.divider()

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("anime/background_image.jpg")

page_bg_img = f"""
<style>


[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""


st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("<br><br><br>", unsafe_allow_html=True)



page = st.sidebar.selectbox("Reviews Or Query Reviews or About", ("City", "Suburbs","Predict","About Application"))

sidebar_style = """
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
    color: black; /* Set text color to black */
"""
sidebar_style = "background-color: #f0f2f6; padding: 20px; border-radius: 10px;"

instructions_html = """
<h4 style='color: black; font-family: Arial, sans-serif;'>Step 1: Explore City</h4>
<ol>
    <li style='color: blue; font-weight: bold;'>Select a city from the dropdown menu or enter any city from INDIA.</li>
    <li style='color: blue; font-weight: bold;'>Click the "Explore" button to proceed.</li>
</ol>

<h4 style='color: black; font-family: Arial, sans-serif;'>Step 2: Explore Suburb</h4>
<ol>
    <li style='color: blue; font-weight: bold;'>Choose a suburb from the list or use the search bar to find a specific suburb.</li>
    <li style='color: blue; font-weight: bold;'>Click the "Explore" button to view details about the selected suburb.</li>
</ol>

<h4 style='color: black; font-family: Arial, sans-serif;'>Step 3: Predict</h4>
<ol>
    <li style='color: black; font-weight: bold;'>Fill in the details below to predict the price of a house:</li>
    <ul>
        <li style='color: blue; font-weight: bold;'>Enter the number of bedrooms.</li>
        <li style='color: blue; font-weight: bold;'>Provide the size of the property (in square feet).</li>
        <li style='color: blue; font-weight: bold;'>Specify the number of bathrooms.</li>
        <li style='color: blue; font-weight: bold;'>Select whether the property is ready to move in or under construction.</li>
    </ul>
    <li style='color: blue; font-weight: bold;'>Click the "Predict" button to see the predicted price.</li>
</ol>

<p style='text-align:right; color: red; font-family: Arial, sans-serif;'>By:- Harsh Kandari</p>
"""
st.sidebar.markdown(instructions_html, unsafe_allow_html=True)


@st.cache_data
def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None
    


if page=='City':
    city_set = set([word.split('_')[0].capitalize() for word in href_tables()])
    city = list(city_set) 
    loc1_option = st.radio("Select your city or enter manually:", ["Select from list", "Enter manually"])
    if loc1_option == "Select from list":
        loc1 = st.selectbox("Select your city:", ["None"] + city)
    else:
        loc1 = st.text_input("Enter your city:")
        session_state.loc1 = loc1
    if loc1=="None":
        pass
    else:
        loc1=loc1.lower()
        try:
            if loc1:
                coordinates = get_city_coordinates(loc1)
                if coordinates:
                    latitude, longitude = coordinates
                    print(f"The coordinates of {loc1} are: Latitude {latitude}, Longitude {longitude}")
                else:
                    print(f"Coordinates for {loc1} not found")
                city_coordinates = (latitude,longitude)  # Example: London coordinates
                m = folium.Map(location=city_coordinates, zoom_start=12)
                marker_coordinates = (latitude, longitude)  # Example: London coordinates
                folium.Marker(marker_coordinates, popup='City Center').add_to(m)
                folium_static(m)
                city_page(loc1)
        except:
            st.info("Not able to find coordinates of city")
            city_page(loc1)

if page=='Suburbs':
    loc1 = session_state.loc1
    loc1=loc1.lower()
    suburbs_page(loc1)
if page=="Predict":
    suburb=session_state.suburb
    predict_page(suburb)
elif page=='About Application':
    about_page()
