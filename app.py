import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import os
import base64
import plotly.express as px



# Download model from Google Drive
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

# 1. Sidebar for Match Setup
st.sidebar.title(' Match Setup')
batting_team = st.sidebar.selectbox('Batting Team', sorted(teams))
bowling_team = st.sidebar.selectbox('Bowling Team', sorted(teams))
city = st.sidebar.selectbox('Match City', sorted(cities))

st.title('T-20 Cricket Score Predictor')

if batting_team == bowling_team:
    st.error("Batting and Bowling team must be different!")
else:
    st.subheader(" Match Situation")
    col1, col2 = st.columns(2)

    # Sliders hata kar wapas number_input laga diya, integers set karne ke liye step=1 rakha hai
    with col1:
        current_score = st.number_input('Current Score', min_value=0, max_value=350, value=50, step=1)
        overs = st.number_input('Overs Done (works for over>5)', min_value=5, max_value=19, value=5, step=1)
    with col2:
        wickets = st.number_input('Wickets Out', min_value=0, max_value=10, value=0, step=1)
        last_five = st.number_input('Runs in Last 5 Overs', min_value=0, max_value=100, value=30, step=1)

    # Core Logic
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets

    if overs == 0:
        crr = 0
    else:
        crr = current_score / overs

    # Aggression
    aggression = crr * wickets_left

    # Pressure
    if balls_left == 0:
        pressure = 0
    else:
        pressure = wickets_left / balls_left

    # Phase
    if overs <= 6:
        phase = "powerplay"
    elif overs <= 15:
        phase = "middle"
    else:
        phase = "death"

    # Progress
    progress = overs / 20

    # Runs Possible
    runs_possible = (balls_left/6) * crr

    # Progress Bar
    st.write(f"**Innings Progress** ({phase.capitalize()} Phase)")
    progress_percentage = min(int((overs/20)*100), 100)
    st.progress(progress_percentage)

    # Prepare DataFrame for Model
    input_df = pd.DataFrame({
        'batting_team':[batting_team],
        'bowling_team':[bowling_team],
        'city':[city],
        'current_score':[current_score],
        'balls_left':[balls_left],
        'wickets_left':[wickets_left],
        'crr':[crr],
        'last_five':[last_five],
        'aggression':[aggression],
        'pressure':[pressure],
        'phase':[phase],
        'progress':[progress],
        'runs_possible':[runs_possible]
    })

    # Prediction
    result = pipe.predict(input_df)
    predicted_score = int(result[0])

    lower = predicted_score - 10
    upper = predicted_score + 10

    # Output via Metrics
    st.markdown("---")
    st.subheader("Prediction Results")
    
    col_res2, col_res3 = st.columns(2)
    with col_res2:
        st.metric(label="Predicted Score", value=predicted_score)
    with col_res3:
        st.metric(label="Expected Range", value=f"{lower} - {upper}")

    # Bar Chart Visualization
    chart_data = pd.DataFrame({
        'Stage': ['Current Score', 'Projected Score'],
        'Runs': [current_score, predicted_score]
    })
    
    fig = px.bar(chart_data, x='Stage', y='Runs', text='Runs', color='Stage', 
                 color_discrete_sequence=['#ff9999','#66b3ff'], height=350)
    fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<br><hr><center><small>Developed by Ashutosh Kumar (2024UCM2304) | NSUT</small></center>",
    unsafe_allow_html=True
)
