import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import os
import plotly.express as px

# --- 1. Page Config & Custom CSS ---
st.set_page_config(page_title="T-20 Score Predictor", layout="centered")

# Professional CSS for Styling
st.markdown("""
    <style>
    /* Main Background and Font */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 36px;
        font-weight: 800;
        color: #1E1E1E;
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 2px solid #ff4b4b;
        padding-bottom: 10px;
    }
    
    /* Card-like look for sections */
    div.stExpander {
        border: none !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        border-radius: 12px !important;
        background-color: white !important;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.03);
        text-align: center;
    }
    
    /* Button / Selectbox improvements */
    .stSelectbox label, .stNumberInput label {
        font-weight: 600 !important;
        color: #4F4F4F !important;
    }
    
    /* Progress Bar Color */
    .stProgress > div > div > div > div {
        background-color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data & Model Loading ---
file_id = "15N4KPQc7Job-26w3fKxVfqHCK5y_Pq0w"
if not os.path.exists("pipe.pkl"):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "pipe.pkl", quiet=False)

pipe = pickle.load(open("pipe.pkl","rb"))

teams = ['Australia','India','Bangladesh','New Zealand','South Africa',
         'England','West Indies','Afghanistan','Pakistan','Sri Lanka']

cities = ['Colombo','Mirpur','Johannesburg','Dubai','Auckland','Cape Town',
          'London','Pallekele','Barbados','Sydney','Melbourne','Durban',
          'St Lucia','Wellington','Lauderhill','Hamilton','Centurion',
          'Manchester','Abu Dhabi','Mumbai','Nottingham','Southampton',
          'Mount Maunganui','Chittagong','Kolkata','Lahore','Delhi',
          'Nagpur','Chandigarh','Adelaide','Bangalore','St Kitts',
          'Cardiff','Christchurch','Trinidad']

# --- 3. UI Layout ---
st.markdown('<p class="main-title">T-20 Match Score Predictor</p>', unsafe_allow_html=True)

# Match Setup Section
with st.expander(" STEP 1: CONFIGURE MATCH SETUP", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        batting_team = st.selectbox('Select Batting Team', sorted(teams), index=1) # India default
    with col_b:
        bowling_team = st.selectbox('Select Bowling Team', sorted(teams), index=0) # Australia default
    
    city = st.selectbox('Select Venue (City)', sorted(cities), index=cities.index('Mumbai') if 'Mumbai' in cities else 0)

if batting_team == bowling_team:
    st.warning(" **Wait!** Batting and Bowling teams cannot be the same. Please select different teams.")
else:
    # Match Situation Section
    st.markdown("### STEP 2: LIVE MATCH SITUATION")
    
    # Custom Container for Inputs
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            current_score = st.number_input('Score', min_value=0, value=50)
        with c2:
            overs = st.number_input('Overs', min_value=5.0, max_value=19.5, value=10.0, step=0.1)
        with c3:
            wickets = st.number_input('Wickets', min_value=0, max_value=9, value=2)
        with c4:
            last_five = st.number_input('Last 5v', min_value=0, value=35)

    # Calculation Logic
    balls_left = 120 - (int(overs) * 6 + int((overs % 1) * 10))
    wickets_left = 10 - wickets
    crr = current_score / overs if overs > 0 else 0
    aggression = crr * wickets_left
    pressure = wickets_left / balls_left if balls_left > 0 else 0
    phase = "powerplay" if overs <= 6 else "middle" if overs <= 15 else "death"
    progress = overs / 20
    runs_possible = (balls_left/6) * crr

    # Progress Indicator
    st.write(f"**Innings Progress:** {phase.upper()} PHASE")
    st.progress(min(progress, 1.0))

    # Prediction Logic
    input_df = pd.DataFrame({
        'batting_team':[batting_team], 'bowling_team':[bowling_team], 'city':[city],
        'current_score':[current_score], 'balls_left':[balls_left], 'wickets_left':[wickets_left],
        'crr':[crr], 'last_five':[last_five], 'aggression':[aggression],
        'pressure':[pressure], 'phase':[phase], 'progress':[progress], 'runs_possible':[runs_possible]
    })

    result = pipe.predict(input_df)
    predicted_score = int(result[0])
    
    # Prediction Display
    st.markdown("---")
    st.markdown("### STEP 3: PREDICTION OUTPUT")
    
    out1, out2 = st.columns(2)
    with out1:
        st.metric(label="PROJECTED TOTAL", value=predicted_score)
    with out2:
        st.metric(label="EXPECTED RANGE", value=f"{predicted_score-10} - {predicted_score+10}")

    # Visualization
    fig = px.bar(
        x=['Current Score', 'Predicted Total'], 
        y=[current_score, predicted_score],
        color=['Current', 'Predicted'],
        color_discrete_map={'Current': '#E1E1E1', 'Predicted': '#ff4b4b'},
        text=[current_score, predicted_score]
    )
    fig.update_layout(
        showlegend=False, 
        height=300, 
        margin=dict(t=10, b=0, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
    <div style='text-align: center; color: #888; font-size: 12px; margin-top: 50px;'>
        Developed by Ashutosh Kumar(2024UCM2304) | NSUT
    </div>
    """, unsafe_allow_html=True)
