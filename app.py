import streamlit as st
import pandas as pd
import plotly.express as px
import base64 # Import the base64 library

st.set_page_config(layout="wide") 

# --- FUNCTION TO SET BACKGROUND IMAGE ---
# We use the specific file name "guinea pig pic.webp" here
def set_background(image_file="guinea pig pic.webp"):
    try:
        with open(image_file, "rb") as f:
            img_bytes = base64.b64encode(f.read()).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/webp;base64,{img_bytes}"); 
                background-size: cover; 
                background-attachment: fixed; 
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image file not found. Running without background image.")

# --- CALL THE FUNCTION TO SET THE BACKGROUND ---
set_background() 

st.title("Guinea Pig Breed Dashboard 🐹")

# Load the data from your new CSV file
try:
    df = pd.read_csv("guinea_pig_breeds.csv") 
except FileNotFoundError:
    st.error("Error: The data file 'guinea_pig_breeds.csv' was not found.")
    st.stop() 

# --- SIDEBAR FOR INTERACTION ---
st.sidebar.header("Filter Breeds")

# Get unique grooming needs and add an 'All' option
all_grooming = ['All'] + list(df['Grooming Needs'].unique())
selected_grooming = st.sidebar.selectbox("Select Grooming Needs Level", all_grooming)

# Filter the data based on selection
if selected_grooming == 'All':
    filtered_df = df
else:
    filtered_df = df[df['Grooming Needs'] == selected_grooming]

# --- MAIN CONTENT ---
st.subheader(f"Available Breeds with '{selected_grooming}' Grooming Needs")
st.write(f"Total breeds selected: **{len(filtered_df)}**")
st.dataframe(filtered_df) 

st.header("Data Analysis and Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Weight Distribution by Breed (grams)")
    fig_weight = px.bar(filtered_df, x='Breed', y='Average Weight (g)', color='Coat Type')
    st.plotly_chart(fig_weight, use_container_width=True)

with col2:
    st.subheader("Breeds by Origin Country")
    origin_counts = df['Origin'].value_counts()
    fig_origin = px.pie(origin_counts, values='count', names=origin_counts.index, title='Origin Country Distribution')
    st.plotly_chart(fig_origin, use_container_width=True)

