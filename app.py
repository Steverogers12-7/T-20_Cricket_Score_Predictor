import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import os
import plotly.express as px


st.set_page_config(page_title="T-20 Score Predictor", layout="centered")

st.markdown("""
    <style>
    /* Centered & Large Title */
    .main-title {
        font-size: 52px;
        font-weight: 900;
        color: #1E1E1E;
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.2;
    }

    /* Dark/Black Background for Expander Header */
    .stExpander {
        border: 1px solid #000000 !important;
        border-radius: 12px !important;
    }

    .streamlit-expanderHeader {
        background-color: #000000 !important;
        color: white !important;
        border-radius: 10px 10px 0 0 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }

    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Model Loading ---
file_id = "15N4KPQc7Job-26w3fKxVfqHCK5y_Pq0w"
if not os.path.exists("pipe.pkl"):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "pipe.pkl", quiet=False)

pipe = pickle.load(open("pipe.pkl", "rb"))

teams = ['Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
         'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka']

cities = ['Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town',
          'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban',
          'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion',
          'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton',
          'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi',
          'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts',
          'Cardiff', 'Christchurch', 'Trinidad']

# --- Main UI ---
st.markdown('<p class="main-title">T-20 Cricket Score Predictor</p>', unsafe_allow_html=True)

with st.expander("CONFIGURE MATCH SETUP", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        batting_team = st.selectbox('Select Batting Team', sorted(teams), index=1)
    with col_b:
        bowling_team = st.selectbox('Select Bowling Team', sorted(teams), index=0)

    city = st.selectbox('Select Venue (City)', sorted(cities),
                        index=cities.index('Mumbai') if 'Mumbai' in cities else 0)

st.markdown("---")

if batting_team == bowling_team:
    st.error("**Teams must be different!** Please select two different teams to proceed.")
else:
    st.subheader("Live Match Situation")

    c1, c2 = st.columns(2)
    with c1:
        current_score = st.number_input('Current Score', min_value=0, value=50, step=1)
        overs = st.number_input('Overs Done (Must be > 5)', min_value=5.0, max_value=19.5,
                                value=10.0, step=0.1,
                                help="The model requires at least 5 overs of data to predict.")
    with c2:
        wickets = st.number_input('Wickets Out', min_value=0, max_value=9, value=2, step=1)
        last_five = st.number_input('Last 5 Over Runs', min_value=0, value=35, step=1)

    # --- Derived values ---
    balls_left = 120 - (int(overs) * 6 + int((overs % 1) * 10))
    wickets_left = 10 - wickets
    crr = current_score / overs if overs > 0 else 0
    aggression = crr * wickets_left
    pressure = wickets_left / balls_left if balls_left > 0 else 0
    phase = "powerplay" if overs <= 6 else "middle" if overs <= 15 else "death"
    progress = overs / 20
    runs_possible = (balls_left / 6) * crr

    st.write(f"**Innings Progress:** {phase.upper()} Phase")
    st.progress(min(progress, 1.0))

    # --- Prediction ---
    input_df = pd.DataFrame({
        'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city],
        'current_score': [current_score], 'balls_left': [balls_left],
        'wickets_left': [wickets_left], 'crr': [crr], 'last_five': [last_five],
        'aggression': [aggression], 'pressure': [pressure], 'phase': [phase],
        'progress': [progress], 'runs_possible': [runs_possible]
    })

    result = pipe.predict(input_df)
    predicted_score = int(result[0])

    st.markdown("---")
    st.subheader("Prediction Results")

    res1, res2 = st.columns(2)
    res1.metric("Predicted Total Score", predicted_score)
    res2.metric("Expected Score Range", f"{predicted_score - 10} - {predicted_score + 10}")

    fig = px.bar(
        x=['Current Score', 'Predicted Total'],
        y=[current_score, predicted_score],
        color=['Current', 'Predicted'],
        color_discrete_map={'Current': '#D3D3D3', 'Predicted': '#1E1E1E'},
        text=[current_score, predicted_score]
    )
    fig.update_layout(
        showlegend=False, height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<br><hr><center><small>Developed by Ashutosh Kumar (2024UCM2304) | NSUT</small></center>",
    unsafe_allow_html=True
)
