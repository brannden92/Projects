import pandas as pd
import requests
import json
from collections import defaultdict

# Defining game type so I can add the "all playoffs" option as it isn't default API command
D = "&game_type='D'" # Division Series
F ="&game_type='F'"  # Wild Card Series
L = "&game_type='L'" # League Championship Series
W = "&game_type='W'" # World Series
P = D+F+L+W          # All Playoffs
R = "&game_type='R'" # Regular Season
A = "&game_type='A'" # All-Star Game
S = "&game_type='S'" # Spring Training

def _get_stats_from_api(season, result_count, sort_column, stat_type='hitting', game_type=R):
    '''return information from MLB API.'''
    ### directs to correct function based on hit or pitch
    stat_factory_reg = {'hitting': _mlb_hitting_api_to_row, 'pitching': _mlb_pitching_api_to_row}
    
    url = f"http://lookup-service-prod.mlb.com/json/named.leader_{stat_type}_repeater.bam?sport_code='mlb'&results={result_count}{game_type}&season={season}&sort_column={sort_column}" 
    response_dict = requests.get(url).json()
    raw_rows = response_dict[f'leader_{stat_type}_repeater'][f'leader_{stat_type}_mux']['queryResults']['row']
    row_factory = stat_factory_reg[stat_type]
    return [row_factory(raw_row) for raw_row in raw_rows]

def _mlb_hitting_api_to_row(raw_row):
    '''map dict from MLB API to standardized dict to convert into DataFrame'''
    return {
        'Name': raw_row['name_display_first_last'],
        'Position': raw_row['pos'],
        'Team': raw_row['team_abbrev'],
        'G': raw_row['g'],
        'AB': raw_row['ab'],
        'H': raw_row['h'],
        'R': raw_row['r'],
        'HR': raw_row['hr'],
        'RBI': raw_row['rbi'],
        'SB': raw_row['sb'],
        'BB': raw_row['bb'],
        'Ks': raw_row['so'],
        'AVG': raw_row['avg'],
        'OBP': raw_row['obp'],
        'OPS': raw_row['ops']
        }

def _mlb_pitching_api_to_row(raw_row):
    '''map dict from MLB API to standardized dict to convert into DataFrame'''
    return {
        'Name': raw_row['name_display_first_last'],
        'Team': raw_row['team_abbrev'],
        'G': raw_row['g'],
        'W': raw_row['w'],
        'L': raw_row['l'],
        'SV':raw_row['sv'],
        'IP': raw_row['ip'],
        'ERA': raw_row['era'],
        'WHIP': raw_row['whip'],
        'Ks': raw_row['so'],
        'BB': raw_row['bb'],
        }

def _create_data_frame_from_stats(mlb_stats):
    '''Create a DataFrame from requested stats'''
    df_dict = defaultdict(list)
    for row in mlb_stats:
        for key, value in row.items():
            df_dict[key].append(value)
            
    df_range = range(1, len(mlb_stats)+1)
    return pd.DataFrame(data=df_dict, index=df_range)

def export_to_csv(df,file_name='MLB_data'):
    '''Export DataFrame to csv file'''
    df.to_csv(f'{file_name}.csv', index=False)
    
def main(season, result_count, category, stat_type='hitting', game_type=R):
    '''Request MLB stats from API and create a DataFrame'''
    stats = _get_stats_from_api(season, result_count, category, stat_type, game_type)
    y = _create_data_frame_from_stats(stats)
    export_to_csv(y)
    
## strictly for scripts
if __name__ == '__main__':
    main(2020,10,'hr','hitting',R)
    
## example - getting top 20 homerun hitters from 1990 regular season
# x = _get_stats_from_api(1990,20,'hr','hitting')
# y = _create_data_frame_from_stats(x)
# print(y)