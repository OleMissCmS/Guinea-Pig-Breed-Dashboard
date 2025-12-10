import streamlit as st
import pandas as pd
import plotly.express as px
import base64 

st.set_page_config(layout="wide") 

# --- FUNCTION TO SET BACKGROUND IMAGE ---
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

st.title("Guinea Pig Dashboard 🐹")

# --- CREATE TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Breed Stats", "🍎 Diet Analysis", "🩺 Health Risks"])

# --- TAB 1: BREED ANALYSIS ---
with tab1:
    st.header("Guinea Pig Breed Data")
    try:
        df_breeds = pd.read_csv("guinea_pig_breeds.csv", sep=",") 
    except FileNotFoundError:
        st.error("Error: The breeds data file was not found.")
        st.stop() 

    # Sidebar Filter for Tab 1 (Sidebar state persists across tabs by default)
    st.sidebar.header("Filter Options")
    all_grooming = ['All'] + list(df_breeds['Grooming Needs'].unique())
    selected_grooming = st.sidebar.selectbox("Filter Breeds by Grooming Needs", all_grooming)

    if selected_grooming == 'All':
        filtered_df_breeds = df_breeds
    else:
        filtered_df_breeds = df_breeds[df_breeds['Grooming Needs'] == selected_grooming]

    st.subheader(f"Available Breeds with '{selected_grooming}' Grooming Needs")
    st.dataframe(filtered_df_breeds) 

    # Visualizations
    st.subheader("Average Weight Distribution by Breed (grams)")
    fig_weight = px.bar(filtered_df_breeds, x='Breed', y='Average Weight (g)', color='Coat Type')
    st.plotly_chart(fig_weight, use_container_width=True)

# --- TAB 2: DIET ANALYSIS ---
with tab2:
    st.header("Guinea Pig Diet & Nutrition Data")
    try:
        df_diet = pd.read_csv("guinea_pig_diet.csv", sep=",")
    except FileNotFoundError:
        st.error("Error: The diet data file was not found.")
        st.stop()

    st.subheader("Nutritional Breakdown of Common Foods")
    st.dataframe(df_diet)
    
    st.subheader("Calcium vs. Phosphorus in Diet (Ca:P Ratio)")
    fig_diet = px.scatter(df_diet, x="Calcium (mg)", y="Phosphorus (mg)", text="Food Item", 
                          color="Category", size="Serving Size (g)", title="Calcium vs Phosphorus Content")
    st.plotly_chart(fig_diet, use_container_width=True)

# --- TAB 3: HEALTH ANALYSIS ---
with tab3:
    st.header("Breed Health Disorder Risk Data")
    try:
        df_health = pd.read_csv("guinea_pig_health.csv", sep=",")
    except FileNotFoundError:
        st.error("Error: The health data file was not found.")
        st.stop()
    
    st.dataframe(df_health)

    st.subheader("Comparison of Health Risks by Breed (Index 1-5)")
    # Melt dataframe to use plotly express for multi-bar chart
    df_health_melted = df_health.melt(id_vars=['Breed', 'Avg_Lifespan_Years', 'Most_Common_Issue'], 
                                      var_name='Risk_Type', value_name='Risk_Index')
    
    # Exclude the lifespan from the risk comparison chart
    df_health_melted = df_health_melted[df_health_melted['Risk_Type'] != 'Avg_Lifespan_Years']

    fig_health = px.bar(df_health_melted, x="Breed", y="Risk_Index", color="Risk_Type", 
                        barmode="group", title="Comparative Health Risk Indices (Higher is worse)")
    st.plotly_chart(fig_health, use_container_width=True)

