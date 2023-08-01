import streamlit as st
import pandas as pd
import random
from streamlit_functions import chart_plus_minus, fetch_team_playoff_outcome, leauge_teams, fetch_penent_race_data, chart_penent_races, chart_playoff_races

historical_plus_minus = pd.read_csv('./HISTORICAL_CSV_FILES/historical_plus_minus.csv')
historical_plus_minus_playoff_only = pd.read_csv('./HISTORICAL_CSV_FILES/historical_plus_minus_playoff_only.csv')
historical_playoff_outcomes = pd.read_csv('./HISTORICAL_CSV_FILES/historical_playoff_outcomes.csv')

st.title("MLB Plus Minus Historical Data")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Random", "Single Year", "Pennent Races", "Playoff Races", "About"])

with tab1:
    def generate_random_number():
        return random.randint(0, historical_plus_minus.shape[0] - 1)

    row_index = generate_random_number()

    random_team = historical_plus_minus.iloc[row_index][['Team']].values[0]
    random_year = historical_plus_minus.iloc[row_index][['Year']].values[0]

    try:
        st.pyplot(chart_plus_minus(random_team, random_year, historical_plus_minus))
    except:
        st.write('No information available. Please Reset')   
                
    st.write(random_team, '\n', random_year)
    
    if st.button('Reset'):
        row_index =  generate_random_number()


with tab2:
    user_team = st.selectbox('Team', list(historical_plus_minus['Team'].unique()), index=19)
    user_year = st.slider('Year', 1970, 2022, 2000, key='single_year_slider')

    outcome = fetch_team_playoff_outcome(user_team, user_year, historical_playoff_outcomes)
        
    st.title(f"Games above .500: {user_team} - {user_year}")

    try:
        st.pyplot(chart_plus_minus(user_team, user_year, historical_plus_minus))
    except:
        st.write('No information available.')
        
    st.write(fetch_team_playoff_outcome(user_team, user_year, historical_playoff_outcomes))


with tab3:
    user_div = st.selectbox('Division', ['AL East', 'AL Central', 'AL West', 'NL East', 'NL Central', 'NL West'], index=2)
    user_year = st.slider('Year', 1970, 2022, 2001, key='b')
    
    team1, team2, team3, team4, team5, team6, team7, team8, team9, color_dictionary = leauge_teams(user_div)
      
    df = fetch_penent_race_data(historical_plus_minus, team1, team2, team3, team4, team5, team6, team7, team8, team9, user_year)

    st.title(f"{user_div} - {user_year}")

    try:
        st.pyplot(chart_penent_races(df['Team'].unique(), df, color_dictionary))
    except:
        st.write("No data avaliable.")
        
        
with tab4:
    user_year = st.slider('Year', 1970, 2022, 2009)
    
    df = historical_plus_minus_playoff_only
    
    st.title(f"{user_year} Playoffs")
    
    try:
        st.pyplot(chart_playoff_races(df, user_year))    
    except:
        st.write("No data avaliable.")
    
with tab5:
    st.write('Have any questions? Connect with me.')
    st.write('Twitter: @AllStar_Stats')
    st.write('Email: brennanhurd@gmail.com')