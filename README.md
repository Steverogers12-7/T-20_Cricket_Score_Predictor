
This project is based on machine learning,used for prediction of score of first innings of the t-20 international men cricket matches.
Dataset used for the model= Cricksheet [kaggle].

## Live App
https://t20scorepredictor-ekiorjgngkmcdvpencdzfi.streamlit.app/

## Project Workflow
1. Data Collection
2. Data Cleaning & Preprocessing
3. Feature Engineering
4. Model Training
5. Pipeline Creation
6. Model Evaluation
7. Model Deployment using Streamlit

Conversion from the present form into required form from dataset and then applied feature engineering to make it well for algorithm.Added new features
useful for model generalization.  
Used Regressor class of XGBoost Algorithm for training the model.  

Input features are:-
- Batting Team
- Bowling Team
- City
- Current Score
- Overs Completed
- Wickets Fallen
- Runs in Last 5 Overs

Model calculates Runs Left,Balls Left,Wickets Left,Current Run Rate (CRR),Required Run Rate (RRR),phase,progress,aggression,runs_possible
from input taken from user.All matches data that are used in the training of algorithm is restricted to international t-20 matches 
and were played by men.All cities are not included ,those cities where atleast 5 matches were played are included.There are many teams 
but included only those who play frequently.  

There are some features that enhanced model's understanding as for wickets in match impact on model prediction "phase" as match starts
there are 6 overs for powerplay,7-15 middle and 16-20 overs are death overs.since this model is for first innings so there is only target setting
for team so phase becomes important as in death overs players are tend to score more than predicted and this dynamic as many factors combine to 
do so.others features added are-progress,aggression and runs_possible(from crr*).

I tried randomforest for training but it not generalizes the model better(underfitting) so, used boosting technique of ensemble learning.
eXtreme Gradient Boosting(xgboost) which sequentially corrects the errors of models.It genralise(learn patterns) from data and performed well and not 
overfitting as i verified with cross validation and intact the results in model training and testing notebook.
some latest match prediction screenshots are given below:-

##  Model Predictions & Results

### 🔹 Case Study 01
<p align="center">
  <img src="https://github.com/user-attachments/assets/4b6a7e21-dfee-41fc-9c43-624445177a9a" width="100%" alt="Full Model UI" />
</p>

<div align="center">
  <table>
    <tr>
      <th width="50%"></th>
      <th width="50%"></th>
    </tr>
    <tr>
      <td><img src="https://github.com/user-attachments/assets/b597ace4-99f1-4522-8ea7-052931edce63" width="100%"></td>
      <td><img src="https://github.com/user-attachments/assets/0af84fbd-2303-4c00-88b5-2d88e927aaa4" width="100%"></td>
    </tr>
  </table>
</div>

---

### 🔹 Case Study 02
<p align="center">
  <img src="https://github.com/user-attachments/assets/f8f595e6-6d01-4ca1-b0ff-948c9ab10db5" width="100%" alt="Full Model UI 2" />
</p>

<div align="center">
  <table>
    <tr>
      <th width="50%"></th>
      <th width="50%"></th>
    </tr>
    <tr>
      <td><img src="https://github.com/user-attachments/assets/a5f7dad5-151d-463c-84a5-a0a1978afdc7" width="100%"></td>
      <td><img src="https://github.com/user-attachments/assets/66544bb2-9e34-46b3-bcd4-bf92e31c5694" width="100%"></td>
    </tr>
  </table>
</div>

Match Result images are collected from Google.  
Model Prediction images are collected from live model deployed on streamlit.









All Data Extraction,preprocessing,feature extraction,model training & testing all performed in the jupyter notebook.

## Tech Stack
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


Ashutosh Kumar.
Machine Learning Project – T20 Cricket Score Prediction

