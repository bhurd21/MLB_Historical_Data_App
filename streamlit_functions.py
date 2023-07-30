import pandas as pd
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

def chart_plus_minus(team, year, dataframe):
    
    # take in dataframe, filter on team and year
    df = dataframe[(dataframe['Team'] == team) & (dataframe['Year'] == year)]
    
    # change date type to datetime for easier use
    df.Date = df.Date.astype('datetime64[ns]')
    
    # cut out unnecessary columns, duplicates that will mess up viz
    df = df[['Date', 'plus_minus', 'Year']].drop_duplicates(subset='Date')
    
    # smooth the values slightly, get less pointed lines, more rounded
    df['smoothed_value'] = df['plus_minus'].rolling(window=3, center=True).mean()

    # create figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))  
    
    # set whole background to match streamlit
    fig.patch.set_facecolor('#0f1116') 
    ax.set_facecolor('#0f1116')

    # plot the line graph with small white line, will be covered
    ax.plot(df['Date'], df['smoothed_value'], color='white', linewidth=0.01)

    # the 'fill' part -- gives us the green and red areas... red is the same as slider, green is from excel logo, alphaed a little
    ax.fill_between(df['Date'], df['smoothed_value'], 0, where=df['smoothed_value'] >= 0, interpolate=True, color='#33c482', alpha=0.7)
    ax.fill_between(df['Date'], df['smoothed_value'], 0, where=df['smoothed_value'] < 0, interpolate=True, color='#ff4c4b', alpha=0.7)

    # creates baseline, blends into background for regular season, gold for post-season
    ax.hlines(0, pd.to_datetime(min(dataframe[dataframe['Year'] == year]['Date'])), pd.to_datetime(min(dataframe[(dataframe['Year'] == year)].pivot_table(index='Team', values='Date', aggfunc='max')['Date'])), colors='#0f1116')
    ax.hlines(0, pd.to_datetime(min(dataframe[(dataframe['Year'] == year)].pivot_table(index='Team', values='Date', aggfunc='max')['Date'])), pd.to_datetime(max(dataframe[dataframe['Year'] == year]['Date'])), colors='gold')

    # remove unnecessary lines
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('white') 
    
    # set length of x-axis, remove tick marks
    ax.set_xlim(pd.to_datetime(min(dataframe[dataframe['Year'] == year]['Date'])), pd.to_datetime(max(dataframe[dataframe['Year'] == year]['Date'])))
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    
    # have only min, max, and 0 tick marks, make it all white
    ax.set_yticks([min(df['plus_minus']), 0, max(df['plus_minus'])])
    ax.tick_params(axis='y', colors='white')
    
    return fig


def fetch_team_playoff_outcome(team, year, df):
    
    # take in dataframe, filter on year and team
    event_result = df[(df['Team'] == team) & (df['Year'] == year)][['Event', 'Result']]
    
    # if the team and year combo is in the dataframe
    if event_result.shape[0]:
        event = event_result['Event'].values[0]
        result = event_result['Result'].values[0]
        
        # if their final series ended in a win, they must have won the whole WS
        if result == 'W':
            s = "Won the World Series!"
            return s
        
        # they did not win their final series, list round they lost in 
        else:
            s = f"Lost in the {event}"
            return s
    
    # team and year combo not in dataframe, a few cases where names do not match
    else: 
        s = 'Did not reach playoffs / No data avaliable.'
        return s
    
    
def leauge_teams(user_div):
    
    # checking for which division user selected, adds team colors as well for charting
    if user_div == 'AL East':
        team1 = 'Boston Red Sox'
        team2 = 'Tampa Bay Devil Rays'
        team3 = 'Tampa Bay Rays'
        team4 = 'Toronto Blue Jays'
        team5 = 'Baltimore Orioles'
        team6 = 'New York Yankees'
        team7 = None
        team8 = None
        team9 = None 
        color_dic = {
            'Boston Red Sox' : '#BD3039',
            'Tampa Bay Devil Rays' : '#8FBCE6',
            'Tampa Bay Rays' : '#8FBCE6',
            'Toronto Blue Jays' : '#134A8E',
            'Baltimore Orioles' : '#DF4601',
            'New York Yankees' : '#0C2340'
        }
    if user_div == 'AL Central':
        team1 = 'Minnesota Twins'
        team2 = 'Cleveland Indians'
        team3 = 'Cleveland Guardians'
        team4 = 'Detroit Tigers'
        team5 = 'Chicago White Sox'
        team6 = 'Kansas City Royals'
        team7 = None
        team8 = None
        team9 = None        
        color_dic = {
            'Minnesota Twins' : '#002B5C',
            'Cleveland Indians' : '#E50022',
            'Cleveland Guardians' : '#E50022',
            'Detroit Tigers' : '#FA4616',
            'Chicago White Sox' : '#C4CED4',
            'Kansas City Royals' : '#BD9B60'
        }
    if user_div == 'AL West':
        team1 = 'Texas Rangers'
        team2 = 'Houston Astros'
        team3 = 'California Angels'
        team4 = 'Anaheim Angels'
        team5 = 'LA Angels of Anaheim'
        team6 = 'Los Angeles Angels'
        team7 = 'Seattle Mariners'
        team8 = 'Oakland Athletics'
        team9 = None  
        color_dic = {
            'Texas Rangers' : '#003278',
            'Houston Astros' : '#EB6E1F',
            'California Angels' : '#BA0021',
            'Anaheim Angels' : '#BA0021',
            'LA Angels of Anaheim' : '#BA0021',
            'Los Angeles Angels' : '#BA0021',
            'Seattle Mariners' : '#005C5C',
            'Oakland Athletics' : '#003831'
        }
    if user_div == 'NL East':
        team1 = 'Atlanta Braves'
        team2 = 'Philadelphia Phillies'
        team3 = 'Miami Marlins'
        team4 = 'New York Mets'
        team5 = 'Washington Senators'
        team6 = 'Washington Nationals'
        team7 = None
        team8 = None
        team9 = None  
        color_dic = {
            'Atlanta Braves' : '#13274F',
            'Philadelphia Phillies' : '#E81828',
            'Miami Marlins' : '#00A3E0',
            'New York Mets' : '#FF5910',
            'Washington Senators' : '#AB0003',
            'Washington Nationals' : '#AB0003'
        }
    if user_div == 'NL Central':
        team1 = 'Milwaukee Brewers'
        team2 = 'Cincinnati Reds'
        team3 = 'Chicago Cubs'
        team4 = 'St. Louis Cardinals'
        team5 = 'Pittsburgh Pirates'
        team6 = None
        team7 = None
        team8 = None
        team9 = None
        color_dic = {
            'Milwaukee Brewers': '#85714D',
            'Cincinnati Reds': '#C6011F',
            'Chicago Cubs': '#0E3386',
            'St. Louis Cardinals': '#C41E3A',
            'Pittsburgh Pirates': '#FDB827'
        }
    if user_div == 'NL West':
        team1 = 'Los Angeles Dodgers'
        team2 = "Arizona D'Backs"
        team3 = 'San Francisco Giants'
        team4 = 'San Diego Padres'
        team5 = 'Colorado Rockies'
        team6 = None
        team7 = None
        team8 = None
        team9 = None
        color_dic = {
            'Los Angeles Dodgers' : '#005A9C',
            "Arizona D'Backs" : '#A71930',
            'San Francisco Giants' : '#FD5A1E',
            'San Diego Padres' : '#2F241D',
            'Colorado Rockies' : '#333366'
        }  
    return team1, team2, team3, team4, team5, team6, team7, team8, team9, color_dic


def fetch_penent_race_data(df_p_m, team1, team2, team3, team4, team5, team6, team7, team8, team9, year):
    
    df = df_p_m
    
    # filter on all teams in selected division
    df = df[(df['Team'] == team1) | (df['Team'] == team2) | (df['Team'] == team3) | (df['Team'] == team4) | (df['Team'] == team5) | (df['Team'] == team6) | (df['Team'] == team7) | (df['Team'] == team8) | (df['Team'] == team9)]
    
    # filter on year
    df = df[df['Year'] == year]  

    # change Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # set Date as index, sorts the values
    df.set_index('Date', inplace=True)
    
    return df


def chart_penent_races(ut, df, color_dic):
    
    # create figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # set entire background to match streamlit
    fig.set_facecolor('#0f1116')
    ax.set_facecolor('#0f1116')
    
    # plot each team given in their team color
    for team in ut:
        subset_df = df[df['Team'] == team]
        ax.plot(subset_df.index, subset_df['plus_minus'], label=team, color=color_dic.get(team))

   
    # blend x axis into background, let y be white, only tick for min, max, 0
    ax.tick_params(axis='x', colors='#0f1116')
    ax.tick_params(axis='y', colors='white')
    ax.set_yticks([min(df['plus_minus']), 0, max(df['plus_minus'])])
    
    # remove unnecessary lines
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('white')
    
    # add baseline at y=0
    ax.axhline(y=0, color='white', linewidth=1)
    
    # add legend that blends into background, shows team colors
    ax.legend(facecolor='#0f1116', edgecolor='#0f1116', labelcolor='white')
    
    return fig



def chart_playoff_races(df, year):
    
    color_dic = {
        'Boston Red Sox' : '#BD3039',
        'Tampa Bay Devil Rays' : '#8FBCE6',
        'Tampa Bay Rays' : '#8FBCE6',
        'Toronto Blue Jays' : '#134A8E',
        'Baltimore Orioles' : '#DF4601',
        'New York Yankees' : '#0C2340',
        'Minnesota Twins' : '#002B5C',
        'Cleveland Indians' : '#E50022',
        'Cleveland Guardians' : '#E50022',
        'Detroit Tigers' : '#FA4616',
        'Chicago White Sox' : '#C4CED4',
        'Kansas City Royals' : '#BD9B60',
        'Texas Rangers' : '#003278',
        'Houston Astros' : '#EB6E1F',
        'California Angels' : '#BA0021',
        'Anaheim Angels' : '#BA0021',
        'LA Angels of Anaheim' : '#BA0021',
        'Los Angeles Angels' : '#BA0021',
        'Seattle Mariners' : '#005C5C',
        'Oakland Athletics' : '#003831',
        'Atlanta Braves' : '#13274F',
        'Philadelphia Phillies' : '#E81828',
        'Miami Marlins' : '#00A3E0',
        'New York Mets' : '#FF5910',
        'Washington Senators' : '#AB0003',
        'Washington Nationals' : '#AB0003',
        'Milwaukee Brewers': '#85714D',
        'Cincinnati Reds': '#C6011F',
        'Chicago Cubs': '#0E3386',
        'St. Louis Cardinals': '#C41E3A',
        'Pittsburgh Pirates': '#FDB827',
        'Los Angeles Dodgers' : '#005A9C',
        "Arizona D'Backs" : '#A71930',
        'San Francisco Giants' : '#FD5A1E',
        'San Diego Padres' : '#2F241D',
        'Colorado Rockies' : '#333366'
        }  


    df = df[df['Year'] == year]
    
    df.Date = df.Date.astype('datetime64[ns]')
    
    # smooth the values slightly, get less pointed lines, more rounded
    df['smoothed_value'] = df['plus_minus'].rolling(window=3, center=True).mean()
    
    data_year = df.drop_duplicates(subset=['Team', 'Date'])

    # Create a figure and axis
    fig, ax = plt.subplots()
    
    fig.set_facecolor('#0f1116')
    ax.set_facecolor('#0f1116')

    # Get unique team names
    teams = data_year['Team'].unique()

    # Plot each team's data as a separate line
    for team in teams:
        team_data = data_year[data_year['Team'] == team]
        ax.plot(team_data['Date'], team_data['plus_minus'], label=team, color=color_dic.get(team))

    # blend x axis into background, let y be white, only tick for min, max, 0
    ax.tick_params(axis='x', colors='#0f1116')
    ax.tick_params(axis='y', colors='white')
    ax.set_yticks([min(df['plus_minus']), 0, max(df['plus_minus'])])
    
    # remove unnecessary lines
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('white')
    
    # add baseline at y=0
    ax.axhline(y=0, color='white', linewidth=1)
    
    # add legend that blends into background, shows team colors
    ax.legend(facecolor='#0f1116', edgecolor='#0f1116', labelcolor='white', loc='upper left', fontsize = 7)

    return fig
