import streamlit as st
import pickle
import numpy as np

# Load the Random Forest Classifier model
filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))

# Define the function to convert team names to binary features
def get_binary_team_features(batting_team, bowling_team):
    team_names = ['Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
                  'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
                  'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
    team_features = []
    for team in team_names:
        if team == batting_team:
            team_features.append(1)
        else:
            team_features.append(0)
        if team == bowling_team:
            team_features.append(1)
        else:
            team_features.append(0)
    return team_features

# Define the Streamlit app
def main():
    st.title("Cricket Score Predictor")

    # Add input fields for user to enter the features
    batting_team = st.selectbox("Select Batting Team", ['Chennai Super Kings', 'Delhi Daredevils',
                                                        'Kings XI Punjab', 'Kolkata Knight Riders',
                                                        'Mumbai Indians', 'Rajasthan Royals',
                                                        'Royal Challengers Bangalore', 'Sunrisers Hyderabad'])
    bowling_team = st.selectbox("Select Bowling Team", ['Chennai Super Kings', 'Delhi Daredevils',
                                                        'Kings XI Punjab', 'Kolkata Knight Riders',
                                                        'Mumbai Indians', 'Rajasthan Royals',
                                                        'Royal Challengers Bangalore', 'Sunrisers Hyderabad'])
    overs = st.slider("Overs Played", 0.0, 20.0, 10.0, 0.1)
    runs = st.number_input("Runs Scored by Batting Team", min_value=0, max_value=400, value=150)
    wickets = st.number_input("Wickets Lost by Batting Team", min_value=0, max_value=10, value=2)
    runs_in_prev_5 = st.number_input("Runs Scored in Previous 5 Overs", min_value=0, max_value=100, value=30)
    wickets_in_prev_5 = st.number_input("Wickets Lost in Previous 5 Overs", min_value=0, max_value=5, value=1)

    # Add a button to submit the form and predict the score
    if st.button("Predict Score"):
        # Convert the features into the required format and predict the score
        team_features = get_binary_team_features(batting_team, bowling_team)
        input_features = np.array([team_features + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]])
        predicted_score = int(regressor.predict(input_features)[0])

        # Display the predicted score with some additional information
        st.write("### Predicted Score Range")
        st.write(f"Lower Limit: {predicted_score-10}")
        st.write(f"Upper Limit: {predicted_score+5}")

if __name__ == '__main__':
    main()
