import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import time

pd.options.mode.chained_assignment = None

def fetch_raw_data_MLB(year, type):
    url = f"https://www.baseball-reference.com/leagues/majors/{year}-schedule.shtml" # change year here
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if type == 'reg':
        soup = soup.find_all(class_="section_content")[0]
    else:
        
        soup = soup.find_all(class_="section_content")[1]

    ret = []

    for calendar_date in soup.find_all('div'): # can switch with post season here
        date = calendar_date.find('h3').text
        for boxscore in calendar_date.find_all(class_="game"):
            
            game_stats = [x.strip() for x in boxscore.text.split('\n') if x.strip() != '']
            
            team1 = game_stats[0].strip()
            team1score = int(game_stats[1].strip()[1:-1])
            team2 = game_stats[3].strip()
            team2score = int(game_stats[4].strip()[1:-1])
            
            if team1score > team2score:
                wTeamName = team1
                wTeamScore = team1score
                lTeamName = team2
                lTeamScore = team2score
            else:
                wTeamName = team2
                wTeamScore = team2score
                lTeamName = team1
                lTeamScore = team1score

            ret.append([wTeamName, wTeamScore, lTeamName, lTeamScore, date])  

    df = pd.DataFrame(ret, columns=['Winning Team', 'W Runs', 'Losing Team', 'L Runs', 'Date'])   
    
    df.Date = df.Date.astype('datetime64[ns]')
    
    return df
'''
df = fetch_raw_data_MLB(1970, 'reg')
df = pd.concat([df, fetch_raw_data_MLB(1970, 'post')], axis=0)

for year in [x+1971 for x in range(52)]:
    time.sleep(3.5)
    try:
        df = pd.concat([df, fetch_raw_data_MLB(year, 'reg')], axis=0)
        df = pd.concat([df, fetch_raw_data_MLB(year, 'post')], axis=0)
        print(year)
    except:
        print(f"{year} did not compute")
        continue

#df.to_csv('./historical_game_outcomes_MLB_pre_1990.csv') # 1970 - 1990, excludes 1979, 1989
#df.to_csv('./historical_game_outcomes_MLB.csv') # 1990 - 2022, change line 'for year in [x+1971 for x in range(19)]:' to different range to change years
'''


####### TRANSFORM / CLEAN DATA #######

def transform(team, year, dataframe):
    
    df = dataframe[(dataframe['Winning Team'] == team) | (dataframe['Losing Team'] == team)]
    df['Year'] = df.Date.str.split('-').str[0]
    df = df[df['Year'] == str(year)]

    df['W_Count'] = (df['Winning Team'] == team)
    df['L_Count'] = (df['Losing Team'] == team)
    df['W_Count_Cum'] = df['W_Count'].cumsum()
    df['L_Count_Cum'] = df['L_Count'].cumsum()
    df['plus_minus'] = df['W_Count_Cum'] - df['L_Count_Cum']
    df.Date = df.Date.astype('datetime64[ns]')
    df = df[['Date', 'plus_minus']].drop_duplicates(subset='Date')
    df['Team'] = team
    return df

teams = ['Boston Red Sox', 'Seattle Mariners', 'Chicago White Sox',
       'Cincinnati Reds', 'Baltimore Orioles', 'Los Angeles Dodgers',
       'Pittsburgh Pirates', 'Oakland Athletics', 'St. Louis Cardinals',
       'Texas Rangers', 'California Angels', 'Chicago Cubs',
       'Toronto Blue Jays', 'San Francisco Giants', 'Atlanta Braves',
       'Kansas City Royals', 'New York Mets', 'Minnesota Twins',
       'San Diego Padres', 'Montreal Expos', 'Philadelphia Phillies',
       'Detroit Tigers', 'New York Yankees', 'Milwaukee Brewers',
       'Cleveland Indians', 'Houston Astros', 'Florida Marlins',
       'Colorado Rockies', 'Anaheim Angels', 'Tampa Bay Devil Rays',
       "Arizona D'Backs", 'LA Angels of Anaheim', 'Washington Nationals',
       'Tampa Bay Rays', 'Miami Marlins', 'Los Angeles Angels',
       'Cleveland Guardians', 'Washington Senators']

# both reg and post
ret = pd.DataFrame()
for year in [x+1970 for x in range(53)]:
    for team in teams:
        print(team, year)
        if year != 1979 and year != 1989:
            if year < 1990:
                temp = transform(team, year, pd.read_csv('./historical_game_outcomes_MLB_pre_1990.csv'))

                ret = pd.concat([ret, temp], axis=0)
            else:
                temp = transform(team, year, pd.read_csv('./historical_game_outcomes_MLB.csv'))
                ret = pd.concat([ret, temp], axis=0)
                
ret['Year'] = ret['Date'].astype('str').str.split('-').str[0]
                
ret.to_csv('./historical_plus_minus.csv', index=False)


# playoffs only
ret = pd.DataFrame()
for year in [x+1970 for x in range(53)]:
    for team in teams:
        print(team, year)
        if year != 1979 and year != 1989:

            temp = transform(team, year, pd.read_csv('./temp.csv'))
            ret = pd.concat([ret, temp], axis=0)

                
ret['Year'] = ret['Date'].astype('str').str.split('-').str[0]
                
ret.to_csv('./historical_plus_minus_playoff_only.csv', index=False)



