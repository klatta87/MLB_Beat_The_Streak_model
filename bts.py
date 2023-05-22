# ------------------------------------------------------------- #
# --- Discussion #6 : Puthon Intro and Shock Analysis Intro --- #
# ---           Created on Thu Apr 20 09:59:27 2023         --- #
# ------------------------------------------------------------- #

#%%
import os
os.chdir("/Users/andy/Documents/Beat The Streak/04_23")

#%%
#! pip install pybaseball

#%%
import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt
import datetime
from datetime import date, timedelta, datetime
from pybaseball import  team_game_logs, statcast, statcast_single_game, retrosheet, batting_stats_range, pitching_stats_range, playerid_reverse_lookup, playerid_lookup, statcast_batter

#%%
pd.set_option('display.max_columns', None)

#%%
#Trying to loop together each day of stats into one dataframe
#Start with April bc seemes to fail if too many dates
start_date = date(2022, 4, 7)
#end_date = date(2022, 4, 10)
end_date = date(2022, 7, 17)

# Create empty list to store dataframes
dfs = []

# Loop over dates and append dataframes to list
for single_date in pd.date_range(start_date, end_date):
    time.sleep(15)
    data = batting_stats_range(single_date.strftime('%Y-%m-%d'), single_date.strftime('%Y-%m-%d'))
    dfs.append(pd.DataFrame(data))
    print(single_date)
    #except: 

# Concatenate dataframes
batter_single_date_df = pd.concat(dfs)

batter_single_date_df.to_csv('pt1_2022_batting_single_date.csv', index=False)

#%%
batter_single_date_df = pd.read_csv('pt1_2022_batting_single_date.csv')

batter_single_date_df.tail()

#%%
#Need to get the Retrosheet id so I can bring in starting lineup info
key_retro=[]
for id in batter_single_date_df['mlbID']:
  if playerid_reverse_lookup([id], key_type='mlbam')['key_retro'].empty:
    key_retro.append('No_Lookup')
  else:
    for id in playerid_reverse_lookup([id], key_type='mlbam')['key_retro']:
      key_retro.append(id)

batter_single_date_df['key_retro']=key_retro
batter_single_date_df.head()

#%%
#Bring in Retrosheet Game   Log Data
url = "https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/gamelog/GL2022.TXT"
player_game_log_2022 = pd.read_csv(url, delimiter=",", header=None)
player_game_log_2022.head()

#%%
#Give RetroSheet Data its column headers. 
player_game_log_2022.columns=["Date", "Number_of_Game", "Day_of_Week", "Visiting_Team", "Visiting_Legue", "Visiting_Team_Game_Number", "Home_Team", "Home_Team_League", "Home_Team_Game_Number", "Visiting_Score", "Home_Score", "Length_of_Game_Outs", "Day_Night", "Completion_Info", "Forfeit_Info", "Protest_Info", "Park_ID", "Attendance", "Game_Duration_Mins", "Visiting_Line_Score", "Home_Line_Score", "AB_Visiting_Team_Off_Stats", "H_Visiting_Team_Off_Stats", "2B_Visiting_Team_Off_Stats", "3B_Visiting_Team_Off_Stats", "HR_Visiting_Team_Off_Stats", "RBI_Visiting_Team_Off_Stats", "SH_Visiting_Team_Off_Stats", "SF_Visiting_Team_Off_Stats", "HBP_Visiting_Team_Off_Stats", "BB_Visiting_Team_Off_Stats", "IBB_Visiting_Team_Off_Stats", "SO_Visiting_Team_Off_Stats", "SB_Visiting_Team_Off_Stats", "CS_Visiting_Team_Off_Stats", "GIDP_Visiting_Team_Off_Stats", "1B_CI_Visiting_Team_Off_Stats", "LOB_Visiting_Team_Off_Stats", "Pitch_Used_Visiting_Team_Pitch_Stats", "Ind_ER_Visiting_Team_Pitch_Stats", "Team_ER_Visiting_Team_Pitch_Stats", "Wild_Pitches_Visiting_Team_Pitch_Stats", "Balks_Visiting_Team_Pitch_Stats", "PO_Visiting Team Defensive Stats", "Asst_Visiting Team Defensive Stats", "E_Visiting Team Defensive Stats", "PB_Visiting Team Defensive Stats", "DP_Visiting Team Defensive Stats", "TP_Visiting Team Defensive Stats", "AB_Home_Team_Off_Stats", "H_Home_Team_Off_Stats", "2B_Home_Team_Off_Stats", "3B_Home_Team_Off_Stats", "HR_Home_Team_Off_Stats", "RBI_Home_Team_Off_Stats", "SH_Home_Team_Off_Stats", "SF_Home_Team_Off_Stats", "HBP_Home_Team_Off_Stats", "BB_Home_Team_Off_Stats", "IBB_Home_Team_Off_Stats", "SO_Home_Team_Off_Stats", "SB_Home_Team_Off_Stats", "CS_Home_Team_Off_Stats", "GIDP_Home_Team_Off_Stats", "1B_CI_Home_Team_Off_Stats", "LOB_Home_Team_Off_Stats", "Pitch_Used_Home Team Pitching Stats", "Ind_ER_Home Team Pitching Stats", "Team_ER_Home Team Pitching Stats", "Wild_Pitches_Home Team Pitching Stats", "Balks_Home Team Pitching Stats", "PO_Home Team Defensive Stats", "Asst_Home Team Defensive Stats", "E_Home Team Defensive Stats", "PB_Home Team Defensive Stats", "DP_Home Team Defensive Stats", "TP_Home Team Defensive Stats", "HP_ID_Umpires", "HP_Nm_Umpires", "1B_ID_Umpires", "1B_Nm_Umpires", "2B_ID_Umpires", "2B_Nm_Umpires", "3B_ID_Umpires", "3B_Nm_Umpires", "LF_ID_Umpires", "LF_Nm_Umpires", "RF_ID_Umpires", "RF_NM_Umpires", "ID_Visiting_Mgr", "Nm_Visiting_Mgr", "ID_Home Manager", "Nm_Home Manager", "ID_Winning_Pitcher", "Nm_Winning_Pitcher", "ID_Losing_Pitcher", "Nm_Losing_Pitcher", "ID_Saving_Pitcher", "Nm_Saving_Pitcher", "ID_Game_Winning_RBI", "Nm_Game_Winning_RBI", "ID_Visiting_Starting_Pitcher", "Nm_Visiting_Starting_Pitcher", "ID_Home_Starting_Pitcher", "Nm_Home_Starting_Pitcher", "1_ID_Visiting_Starting_Batter", "1_Nm_Visiting_Starting_Batter", "1_DP_Visiting_Starting_Batter", "2_ID_Visiting_Starting_Batter", "2_Nm_Visiting_Starting_Batter", "2_DP_Visiting_Starting_Batter", "3_ID_Visiting_Starting_Batter", "3_Nm_Visiting_Starting_Batter", "3_DP_Visiting_Starting_Batter", "4_ID_Visiting_Starting_Batter", "4_Nm_Visiting_Starting_Batter", "4_DP_Visiting_Starting_Batter", "5_ID_Visiting_Starting_Batter", "5_Nm_Visiting_Starting_Batter", "5_DP_Visiting_Starting_Batter", "6_ID_Visiting_Starting_Batter", "6_Nm_Visiting_Starting_Batter", "6_DP_Visiting_Starting_Batter", "7_ID_Visiting_Starting_Batter", "7_Nm_Visiting_Starting_Batter", "7_DP_Visiting_Starting_Batter", "8_ID_Visiting_Starting_Batter", "8_Nm_Visiting_Starting_Batter", "8_DP_Visiting_Starting_Batter", "9_ID_Visiting_Starting_Batter", "9_Nm_Visiting_Starting_Batter", "9_DP_Visiting_Starting_Batter", "1_ID_Home_Starting_Batter", "1_Nm_Home_Starting_Batter", "1_DP_Home_Starting_Batter", "2_ID_Home_Starting_Batter", "2_Nm_Home_Starting_Batter", "2_DP_Home_Starting_Batter", "3_ID_Home_Starting_Batter", "3_Nm_Home_Starting_Batter", "3_DP_Home_Starting_Batter", "4_ID_Home_Starting_Batter", "4_Nm_Home_Starting_Batter", "4_DP_Home_Starting_Batter", "5_ID_Home_Starting_Batter", "5_Nm_Home_Starting_Batter", "5_DP_Home_Starting_Batter", "6_ID_Home_Starting_Batter", "6_Nm_Home_Starting_Batter", "6_DP_Home_Starting_Batter", "7_ID_Home_Starting_Batter", "7_Nm_Home_Starting_Batter", "7_DP_Home_Starting_Batter", "8_ID_Home_Starting_Batter", "8_Nm_Home_Starting_Batter", "8_DP_Home_Starting_Batter", "9_ID_Home_Starting_Batter", "9_Nm_Home_Starting_Batter", "9_DP_Home_Starting_Batter", "Addtl_Info", "Acquisition_Info"]

#%%
player_game_log_2022.head()

#%% 
#Format Retrosheet date as date
player_game_log_2022['Date'] = player_game_log_2022['Date'].astype(str)
player_game_log_2022['Date'] = player_game_log_2022['Date'].apply(lambda x: datetime.strptime(x, '%Y%m%d').date())

#%%
lineup_cols=[]
for pos in range(1,10):
    vis_col_nm = str(pos) + "_ID_Visiting_Starting_Batter"
    lineup_cols.append(vis_col_nm)
    hom_col_nm = str(pos) + "_ID_Home_Starting_Batter"
    lineup_cols.append(hom_col_nm)

#%%
lineup_cols
    
#%%
batter_single_date_df['Date'] = pd.to_datetime(batter_single_date_df['Date'])
#batter_single_date_df['key_retro'] = str(batter_single_date_df['key_retro'])
player_game_log_2022['Date'] = pd.to_datetime(player_game_log_2022['Date'])


#%%
#print(batter_single_date_df.dtypes)

#%%
#print(player_game_log_2022.dtypes)

#%%
#lineup_cols    
merged_dfs = [] 
for col in lineup_cols:
    merged_dfs.append(pd.merge(batter_single_date_df, player_game_log_2022,
                               left_on=['Date', 'key_retro'], 
                               right_on=['Date', col], how='inner'))

merged_df = pd.concat(merged_dfs, axis=0, ignore_index=True)
merged_df.head()

#%%
merged_df.head()

#%%
# define function to check which lineup column the value is in
def get_lineup_column(row):
    for i in range(1, 10):
        if row['key_retro'] == row[f'{i}_ID_Visiting_Starting_Batter']:
            return f'{i}'
        if row['key_retro'] == row[f'{i}_ID_Home_Starting_Batter']:
            return f'{i}'
    return None

#%%
# apply function to create new column
merged_df['lineup_pos'] = merged_df.apply(lambda row: get_lineup_column(row), axis=1)

merged_df.tail()

#%%
merged_df.to_csv('merged.csv', index=False)

#%%
#merged_df = pd.read_csv('merged.csv')
#merged_df.head()

#%%
#Create and indicator column for home/away
merged_df = merged_df.rename(columns={merged_df.columns[6]: 'Away'})
merged_df.columns

#%%
merged_df['Visiting_Team_Ind'] = np.where(merged_df['Away'] == '@', 1, 0)
#merged_df[['Away']]

#%%
#pitching_stats_range('2022-03-07', '2022-04-07')

#%% 
#Now time to get pitching stats
pitch_window = 20
start_date = date(2022, 4, 7)
end_date = date(2022, 7, 17)


# Create empty list to store dataframes
dfs = []

for single_date in pd.date_range(start_date + pd.DateOffset(days=1), end_date):
    beg_window = single_date - pd.DateOffset(days=pitch_window)
    end_window = single_date - pd.DateOffset(days=1)
    
    time.sleep(15)
    
    data = pitching_stats_range(beg_window.strftime('%Y-%m-%d'), end_window.strftime('%Y-%m-%d'))
    
    data['As_Of_Date'] = single_date.strftime('%Y-%m-%d')
    data['begin_window'] = max(start_date, beg_window).strftime('%Y-%m-%d')
    data['end_window'] = end_window.strftime('%Y-%m-%d')

    dfs.append(pd.DataFrame(data))
    print(single_date)

# Concatenate dataframes
pitching_df = pd.concat(dfs)

pitching_df['As_Of_Date'] = pd.to_datetime(pitching_df['As_Of_Date'])

pitching_df.to_csv('pt1_2022_pitching_stats_range.csv', index=False)

pitching_df.head()

#%%
#pitching_df = pd.read_csv('2022_pitching_stats_range.csv')
#pitching_df.head()

#%%
#Need to get the Retrosheet id so I can bring in starting lineup info
key_retro=[]
for id in pitching_df['mlbID']:
  if playerid_reverse_lookup([int(id)], key_type='mlbam')['key_retro'].empty:
    key_retro.append('No_Lookup')
  else:
    for id in playerid_reverse_lookup([int(id)], key_type='mlbam')['key_retro']:
      key_retro.append(id)

pitching_df['key_retro']=key_retro
pitching_df.head()

pitching_df.to_csv('2022_pitching_stats_range.csv', index=False)


pitching_df.tail()

#%%
home_batters = merged_df[merged_df['Visiting_Team_Ind']==0]
home_batters.head()

#%%

vis_batters = merged_df[merged_df['Visiting_Team_Ind']==1]
vis_batters.head()

#%%
#pitching_df.columns.str.replace(('Opp_Pitch_Last_'+str(pitch_window)+'_days'), '')
pitching_df = pitching_df.add_prefix('Opp_Pitch_Last_'+str(pitch_window)+'_days_')
pitching_df.tail()

#%%
print(pitching_df.dtypes)

#%%
pitching_df.tail()


#%%
home_batters_merged = pd.merge(home_batters, pitching_df, left_on=['Date', 'ID_Visiting_Starting_Pitcher'], 
                           right_on=[('Opp_Pitch_Last_'+str(pitch_window)+'_days_As_Of_Date'), ('Opp_Pitch_Last_'+str(pitch_window)+'_days_key_retro')], how='left')

#%%
vis_batters_merged = pd.merge(vis_batters, pitching_df, left_on=['Date', 'ID_Home_Starting_Pitcher'], 
                           right_on=[('Opp_Pitch_Last_'+str(pitch_window)+'_days_As_Of_Date'), ('Opp_Pitch_Last_'+str(pitch_window)+'_days_key_retro')], how='left')

dfs=[home_batters_merged, vis_batters_merged]

sp_merged_df = pd.concat(dfs)
sp_merged_df.tail()

#%%
sp_merged_df.to_csv('sp_merged.csv', index=False)

#%%
#Do the same thing but get the batters last 20 days
#Now time to get some historical batting stats
bat_window = 20
start_date = date(2022, 4, 7)
end_date = date(2022, 7, 17)


# Create empty list to store dataframes
dfs = []

for single_date in pd.date_range(start_date + pd.DateOffset(days=1), end_date):
    beg_window = single_date - pd.DateOffset(days=bat_window)
    end_window = single_date - pd.DateOffset(days=1)
    
    time.sleep(15)
    
    data = batting_stats_range(beg_window.strftime('%Y-%m-%d'), end_window.strftime('%Y-%m-%d'))
    
    data['As_Of_Date'] = single_date.strftime('%Y-%m-%d')
    data['begin_window'] = max(start_date, beg_window).strftime('%Y-%m-%d')
    data['end_window'] = end_window.strftime('%Y-%m-%d')

    dfs.append(pd.DataFrame(data))
    print(single_date)

# Concatenate dataframes
batting_hist_df = pd.concat(dfs)

batting_hist_df['As_Of_Date'] = pd.to_datetime(batting_hist_df['As_Of_Date'])

batting_hist_df.tail()


#%%
key_retro=[]
for id in batting_hist_df['mlbID']:
  if playerid_reverse_lookup([int(id)], key_type='mlbam')['key_retro'].empty:
    key_retro.append('No_Lookup')
  else:
    for id in playerid_reverse_lookup([int(id)], key_type='mlbam')['key_retro']:
      key_retro.append(id)

batting_hist_df['key_retro']=key_retro

#%%
batting_hist_df = batting_hist_df.add_prefix('Bat_Last_'+str(bat_window)+'_days_')
batting_hist_df.tail()

#%%

merged_hist_df = pd.merge(sp_merged_df, batting_hist_df, left_on=['Date', 'key_retro'], 
                           right_on=[('Bat_Last_'+str(bat_window)+'_days_As_Of_Date'),
                                     ('Bat_Last_'+str(bat_window)+'_days_key_retro')], how='left')
                           
merged_hist_df.tail()

#%%
merged_hist_df.to_csv('pt1_2022_merged_hist.csv', index=False)

#%%
print('It completed!')

#%%
print('end')
