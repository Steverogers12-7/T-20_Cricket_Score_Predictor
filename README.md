T20 Cricket Score Predictor
This project is based on machine learning,used for prediction of score of first innings of the t-20 international men cricket matches.
Dataset used for this model= Cricksheet [kaggle].

## 🚀 Live App
https://t20scorepredictor-ekiorjgngkmcdvpencdzfi.streamlit.app/

## 📊 Project Workflow
1. Data Collection
2. Data Cleaning & Preprocessing
3. Feature Engineering
4. Model Training
5. Pipeline Creation
6. Model Evaluation
7. Model Deployment using Streamlit

Conversion from the present form into required form from dataset and then applied feature engineering to make it well for algorithm.
Used Xgboost Algorithm for training this model.

Input features are:-
- Batting Team
- Bowling Team
- City
- Current Score
- Overs Completed
- Wickets Fallen
- Runs in Last 5 Overs

Model calculates Runs Left,Balls Left,Wickets Left,Current Run Rate (CRR),Required Run Rate (RRR).
All matches data that are used in the training of algorithm is restricted to international t-20 matches and were played by men.
All cities are not included ,those cities where atleast 5 matches were played are included.
There are many teams but included only those who play frequently.

All Data Extraction,preprocessing,feature extraction,model training & testing all performed in the jupyter notebook.

## 🛠️ Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Streamlit
- GitHub
- Google Drive (for model storage)

## 📈 Future Improvements
- Match winner prediction
- Win probability
- Player performance prediction
- Better UI design


Ashutosh Kumar
Machine Learning Project – T20 Cricket Score Prediction

