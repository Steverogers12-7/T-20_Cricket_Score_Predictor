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

        crr = current_score / overs
        

        input_df = pd.DataFrame({
            'batting_team':[batting_team],
            'bowling_team':[bowling_team],
            'city':[city],
            'current_score':[current_score],
            'balls_left':[balls_left],
            'wickets_left':[wickets],
            'crr':[crr],
            'last_five':[last_five]
        })

        result = pipe.predict(input_df)

        st.success(f"Predicted Score: {int(result[0])}")

