import streamlit as st
from pages import city_page,suburbs_page,about_page
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



page = st.sidebar.selectbox("Reviews Or Query Reviews or About", ("City", "Suburbs","About Application"))

sidebar_style = """
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
    color: black; /* Set text color to black */
"""

# Add a box around the sidebar content with black text
st.sidebar.markdown(f"""
    <div style="{sidebar_style}">
        <h3 style="color: black;">Welcome to PropertyPulse</h3>
        <p>This is a Streamlit based application.</p>
        <p>Developed an REST API on AWS LAMBDA for the web scrapping of the RealEstate data</p>
        <p>All data scrapped from Makaan.com</p>
        <br>
        <p style='text-align:right'> By:- Harsh Kandari</p>
        
 
""", unsafe_allow_html=True)
@st.cache_data
def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None
    


if page=='City':
    loc1 = st.text_input("Enter your city:- ")
    loc1=loc1.lower()
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

if page=='Suburbs':
    loc1
    loc1=loc1.lower()
    suburbs_page(loc1)
elif page=='About Application':
    about_page()
