# Getting Data from MLB API
### Overview
This program creates Pandas DataFrames from the MLB API where you can get hitting or pitching data specific to the year, how many rows you want the table to be, what statistic to sort the table by, and what game type you want the data.

### Skills used in this project
- Getting desired information from web API using requests and json packages into readable DataFrames
- Defining functions and feeding them into each other

### How to run
1. Installed required packages
```
$ pip -r requirements.txt
```
2. Run the script
```
$ python main.py
```
3. Get desired results
```
x = _get_stats_from_api(season, result_count, category, stat_type, game_type='R')
_create_data_frame_from_stats(x)
```
- season - integer for year you want statistics from.
- result_count - integer for how many results you want in your DataFrame.
- category - lowercase string for what statistic will be used to acquire/sort your players.
  - examples: 'hr' for homeruns, 'avg' for batting average, 'h' for hits.  
- stat_type - 'hitting' or 'pitching'
- game_type - uppercase string for type of games you want stats for, regular season by default.
  - examples: 'A'- All Star Game, 'D' - Division Series, 'W' for World Series, 'P' for all play off games
  

  
4. (optional) How to download csv file of results
```
x = _get_stats_from_api(season, result_count, sort_column, game_type='R')
y = _create_data_frame_from_stats(x)
export_to_csv(y,file_name='MLB_data')
```
- set new file name if wanted, defaults to "MLB_data.csv"

### Example - Top 20 homerun hitters from 1990 regular season
![](https://raw.githubusercontent.com/brannden92/Projects/main/MLB_api/example.png)
