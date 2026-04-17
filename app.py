import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import os
import plotly.express as px


file_id = "1pMc1hQeMUXbH1JIG2_NECSGNbVDV3L-4"

if not os.path.exists("pipe3.pkl"):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "pipe3.pkl", quiet=False)

pipe = pickle.load(open("pipe3.pkl", "rb"))

teams = ['Australia','India','Bangladesh','New Zealand','South Africa',
         'England','West Indies','Afghanistan','Pakistan','Sri Lanka']

cities = ['Colombo','Mirpur','Johannesburg','Dubai','Auckland','Cape Town',
          'London','Pallekele','Barbados','Sydney','Melbourne','Durban',
          'St Lucia','Wellington','Lauderhill','Hamilton','Centurion',
          'Manchester','Abu Dhabi','Mumbai','Nottingham','Southampton',
          'Mount Maunganui','Chittagong','Kolkata','Lahore','Delhi',
          'Nagpur','Chandigarh','Adelaide','Bangalore','St Kitts',
          'Cardiff','Christchurch','Trinidad']

# Sidebar
st.sidebar.title('Match Setup')
batting_team = st.sidebar.selectbox('Batting Team', sorted(teams), index=sorted(teams).index('Australia'))
bowling_team = st.sidebar.selectbox('Bowling Team', sorted(teams))
city = st.sidebar.selectbox('Match City', sorted(cities))

st.title('T-20 Cricket Score Predictor')

if batting_team == bowling_team:
    st.error("Batting and Bowling team must be different!")
else:
    st.subheader("Match Situation")
    col1, col2 = st.columns(2)

    with col1:
        current_score = st.number_input('Current Score', min_value=0, max_value=350, value=50, step=1)
        overs = st.number_input('Overs Done (works for over>5)', min_value=5, max_value=19, value=5, step=1)
    with col2:
        wickets = st.number_input('Wickets Out', min_value=0, max_value=10, value=0, step=1)
        last_five = st.number_input('Runs in Last 5 Overs', min_value=0, max_value=100, value=30, step=1)

    
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = current_score / overs if overs > 0 else 0
    aggression = crr * wickets_left

    
    if balls_left > 90:
        phase = "powerplay"
    elif balls_left < 30:
        phase = "death"
    else:
        phase = "middle"

    
    st.write(f"**Innings Progress** ({phase.capitalize()} Phase)")
    progress_percentage = min(int((overs / 20) * 100), 100)
    st.progress(progress_percentage)

    
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],
        'current_score': [current_score],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'crr': [crr],
        'last_five': [last_five],
        'aggression': [aggression],
        'phase': [phase]
    })

    
    result = pipe.predict(input_df)
    predicted_score = int(result[0])
    lower = predicted_score - 10
    upper = predicted_score + 10

    st.markdown("---")
    st.subheader("Prediction Results")

    col_res2, col_res3 = st.columns(2)
    with col_res2:
        st.metric(label="Predicted Score", value=predicted_score)
    with col_res3:
        st.metric(label="Expected Range", value=f"{lower} - {upper}")

    
    chart_data = pd.DataFrame({
        'Stage': ['Current Score', 'Projected Score'],
        'Runs': [current_score, predicted_score]
    })

    fig = px.bar(chart_data, x='Stage', y='Runs', text='Runs', color='Stage',
                 color_discrete_sequence=['#ff9999', '#66b3ff'], height=350)
    fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
