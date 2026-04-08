## This project is based on machine learning,used for prediction of score of first innings of the t-20 international men cricket matches.  
## Dataset used for the model= Cricksheet [kaggle].


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

## Methodology

### Feature Engineering
To enhance the model's accuracy, several custom features were engineered to capture the dynamic nature of a T-20 innings:
* **Calculated Metrics:** The model dynamically computes `Runs Left`, `Balls Left`, `Wickets Left`, `Current Run Rate (CRR)`, and `Required Run Rate (RRR)`.
* **Match Phases:** I divided the match into three distinct phases to better predict scoring patterns:
    * **Powerplay:** 0–6 Overs
    * **Middle Overs:** 7–15 Overs
    * **Death Overs:** 16–20 Overs (Crucial for capturing the scoring acceleration typical in the final stages).
* **Advanced Indicators:** Additional features like `Phase`, `Progress`, `Aggression`, and `Runs Possible` (extrapolated from CRR) were added to help the model understand the intent and momentum of the batting team.

### Data Constraints & Quality
To ensure high-quality predictions, the dataset was filtered based on the following criteria:
* **Format:** Restricted to **International Men's T-20** matches.
* **Venues:** Only cities that have hosted at least **5 matches** were included to ensure statistical significance.
* **Teams:** Included only frequently playing nations to maintain a consistent baseline for team performance.

### Model Selection & Generalization
The modeling process involved iterative testing of different algorithms:
* **Random Forest:** Initially tested, but it resulted in **Underfitting**, failing to generalize well across different match situations.
* **XGBoost (Final Model):** I switched to **eXtreme Gradient Boosting**, a powerful ensemble learning technique. XGBoost sequentially corrects errors from previous iterations, allowing it to learn complex patterns more effectively.
* **Validation:** The model was verified using **Cross-Validation** to ensure it generalizes well to unseen data without **Overfitting**. The consistent results between training and testing phases are documented in the project notebooks.

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

