import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import os

# ---------------- DOWNLOAD MODEL ----------------
file_id = "1V5KvUPqU03ellevso7iYoVml-1bUbdBc"

if not os.path.exists("pipe.pkl"):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "pipe.pkl", quiet=False)

# ---------------- LOAD MODEL ----------------
pipe = pickle.load(open("pipe.pkl","rb"))

# ---------------- DATA ----------------
teams = ['Australia','India','Bangladesh','New Zealand','South Africa',
         'England','West Indies','Afghanistan','Pakistan','Sri Lanka']

cities = ['Colombo','Mirpur','Johannesburg','Dubai','Auckland','Cape Town',
          'London','Pallekele','Barbados','Sydney','Melbourne','Durban',
          'St Lucia','Wellington','Lauderhill','Hamilton','Centurion',
          'Manchester','Abu Dhabi','Mumbai','Nottingham','Southampton',
          'Mount Maunganui','Chittagong','Kolkata','Lahore','Delhi',
          'Nagpur','Chandigarh','Adelaide','Bangalore','St Kitts',
          'Cardiff','Christchurch','Trinidad']

# ---------------- UI ----------------
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
    overs_done = st.number_input('Overs Done (min 5)')

with col5:
    wickets = st.number_input('Wickets Out')

last_five = st.number_input('Runs in Last 5 Overs')

# ---------------- PREDICTION ----------------
if st.button('Predict Score'):

    if batting_team == bowling_team:
        st.error("Batting and Bowling team must be different")

    elif overs_done <= 0:
        st.error("Overs must be greater than 0")

    else:
        runs_left = 120 - current_score
        balls_left = 120 - (overs_done * 6)
        wickets_left = 10 - wickets

        crr = current_score / overs_done
        rrr = runs_left / (balls_left / 6)

        input_df = pd.DataFrame({
            'batting_team':[batting_team],
            'bowling_team':[bowling_team],
            'city':[city],
            'runs_left':[runs_left],
            'balls_left':[balls_left],
            'wickets_left':[wickets_left],
            'total_runs_x':[current_score],
            'crr':[crr],
            'rrr':[rrr]
        })

        result = pipe.predict(input_df)

        st.success(f"Predicted Score: {int(result[0])}")
