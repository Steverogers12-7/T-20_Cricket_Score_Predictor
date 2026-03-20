import streamlit as st
import pickle
import pandas as pd
import numpy as np

pipe=pickle.load(open('pipe.pkl','rb'))

teams=['Australia',
'India',
'Bangladesh',
'New Zealand',
'South Africa',
'England',
'West Indies',
'Afghanistan',
'Pakistan',
'Sri Lanka']

cities=['Colombo',
 'Mirpur',
 'Johannesburg',
 'Dubai',
 'Auckland',
 'Cape Town',
 'London',
 'Pallekele',
 'Barbados',
 'Sydney',
 'Melbourne',
 'Durban',
 'St Lucia',
 'Wellington',
 'Lauderhill',
 'Hamilton',
 'Centurion',
 'Manchester',
 'Abu Dhabi',
 'Mumbai',
 'Nottingham',
 'Southampton',
 'Mount Maunganui',
 'Chittagong',
 'Kolkata',
 'Lahore',
 'Delhi',
 'Nagpur',
 'Chandigarh',
 'Adelaide',
 'Bangalore',
 'St Kitts',
 'Cardiff',
 'Christchurch',
 'Trinidad']

st.title('Cricket Score Predictor')
col1,col2=st.beta_columns(2)
with col1:
    Batting_team=st.selectbox('Select Batting Team',sorted(teams))
with col2:
    Bowling_team=st.selectbox('Select Bowling Team',sorted(teams))

city=st.selectbox('Select City',sorted(cities))

col3,col4,col5=st.beta_columns(3)

with col3:
    current_score=st.number_input('Current Score')

with col4:
    overs_done=st.number_input('overs Done(works for over>5)')
with col5:
    wickets=st.number_input('Wickets Out')

last_five=st.number_input('Runs Scored in last 5 overs')

if st.button('Predict Score'):
    pass



