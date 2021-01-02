import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
import sys

# import dataset
df = pd.read_csv('pass_and_game_data.csv', index_col=0)

# fix John Stafford to Matthew Stafford
df.replace(to_replace='John Stafford', value='Matthew Stafford', inplace=True)

def passing_summary(player_name, year):

  plt.style.use('fast')
  player = df.loc[(df['season'] == year) & (df['name'] == player_name)]
    
  #grab completions, incompletions, interceptions, and tds separately
  complete = player.loc[player['pass_type'] == 'COMPLETE']
  incomplete = player.loc[player['pass_type'] == 'INCOMPLETE']
  interception = player.loc[player['pass_type'] == 'INTERCEPTION']
  touchdown = player.loc[player['pass_type'] == 'TOUCHDOWN']

  fig, ax = plt.subplots(figsize=(8, 10))

  # scatter plot the different pass attempts
  ax.scatter(complete['x_coord'], complete['y_coord'], color='blue', alpha=0.65, edgecolors='white')
  ax.scatter(incomplete['x_coord'], incomplete['y_coord'], color='red', alpha=0.65, edgecolors='white')
  ax.scatter(touchdown['x_coord'], touchdown['y_coord'], color='blue', alpha=0.8, edgecolors='white', linewidth=2, s=125)
  ax.scatter(interception['x_coord'], interception['y_coord'], color='red', alpha=0.8, edgecolors='white', linewidth=2, s=125)

  # set ticks
  ax.set_yticks(np.arange(-20, 70, 10))
  ax.set_xticks(np.linspace(-53.3/2, 53.3/2, 4))
  ax.tick_params(axis='x', colors="white", grid_alpha=0.4)
  ax.tick_params(axis='y', colors="white", grid_alpha=0.4)
  plt.setp(ax.spines.values(), color='white', alpha=0.2, linewidth=1)

  # line of scrimmage, hash marks, out of bounds
  ax.hlines(0, -53.3/2, 53.3/2, color='white', linewidth=3, linestyles='dashed', alpha=0.5)
  ax.vlines(x=-18.5/2, ymin=-10, ymax=50, color='white', linewidth=4, linestyle='dotted', alpha=0.5)
  ax.vlines(x=18.5/2, ymin=-10, ymax=50, color='white', linewidth=4, linestyle='dotted', alpha=0.5)
  ax.vlines(x=-54.1/2, ymin=-10, ymax=50, color='white', linewidth=6, linestyle='solid', alpha=.7)
  ax.vlines(x=54.1/2, ymin=-10, ymax=50, color='white', linewidth=6, linestyle='solid', alpha=.7)
  ax.set_xticklabels([])

  # set the background color of our plot to football field green
  ax.set_facecolor('#196f0c')
  fig.set_facecolor('#444444')
 
    
  # set the legend and title
  ax.legend(['Complete Pass', 'Incomplete Pass', 'Touchdown', 'Interception'], 
            ncol=1, loc='upper left', facecolor='#C0C0C0', bbox_to_anchor=(1.05, 1), prop={'size': 18})
  ax.set_title(f'\n {player_name.upper()} PASSING SUMMARY, {str(year)}  \n', color='white', fontsize=24)

# Main Program 
qb_names = df['name'].unique() 

while True:
    print('Which quarterback\'s passes would you like to visualize today?')
    print('Please type "help" if you need a list of names to choose from.')
    print('Type "quit" to exit.')
    player_name = input('Please type their first and last name: ')
    player_name = player_name.title()
    
    if player_name == 'Help':
        print(qb_names)
    elif player_name == 'Quit':
        sys.exit()
    else:
        break
while True:
    year = input('Which season\'s stats would you like to see: 2017, 2018, or 2019?: ')
    if year == 'quit':
        sys.exit()
    else:
        year = int(year)
        years = [2017, 2018, 2019]
        if year in years:
            break
        else:
            print(f'{year} is not valid, please enter a valid year.')

passing_summary(player_name, year)