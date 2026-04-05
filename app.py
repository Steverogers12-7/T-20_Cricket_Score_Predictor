import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import os

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

st.title('🏏 Cricket Score Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Bowling Team', sorted(teams))

city = st.selectbox('Match City', sorted(cities))

col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score')
with col4:
    overs = st.number_input('Overs Done (works for over>5)')
with col5:
    wickets = st.number_input('Wickets Out')

last_five = st.number_input('Runs in Last 5 Overs')

if st.button('Predict Score'):

    if batting_team == bowling_team:
        st.error("Batting and Bowling team must be different")
    else:
        
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
            phase = "Powerplay"
        elif overs <= 15:
            phase = "Middle"
        else:
            phase = "Death"

        # Progress
        progress = overs / 20

        # Runs Possible
        runs_possible = (balls_left/6) * crr

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

        result = pipe.predict(input_df)
        predicted_score = int(result[0])

        lower = predicted_score - 10
        upper = predicted_score + 10

        st.success(f"Predicted Score: {predicted_score}")
        st.info(f"Expected Score Range: {lower} - {upper}")
