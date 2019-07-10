import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)

# Change the file name of the Excel sheet under 'file_name'
file_name = "Practice2019.xlsx"
# The Excel file should be placed in a file called 'Data' the directory directly up the tree from this file
file = "../../Data/" + file_name
# Make sure to specify the correct sheet name
sheet = "Season Data Sheet"

data = pd.read_excel(file, sheet, index_col = None, header = 0, na_values = ' ')
data = data.reset_index()
del data['index']
data = data.dropna(how = 'all')
data = data.fillna(0)

# Uncomment if the Excel sheet is set up with extra, undesired columns
# Switch the values in undesired_columns to the names of the undesired columns

# undesired_columns = np.array(['ODK'])
# for col_name in undesired_columns:
#     del data[col_name]

DN = data.loc[:,'DN']
DIST = data.loc[:,'DIST']
HASH = data.loc[:,'HASH']
YARD_LN = data.loc[:,'YARD LN']
PLAY_TYPE = data.loc[:,'PLAY TYPE']
GN_LS = data.loc[:,'GN/LS']
RESULT = data.loc[:,'RESULT']
OFF_FORM = data.loc[:,'OFF FORM']
OFF_PLAY = data.loc[:,'OFF PLAY']

got_first_down = data.loc[data['GN/LS'] >= data['DIST']]
not_first_down = data.loc[data['GN/LS'] < data['DIST']]

first_down = data.loc[data['DN'] == 1]
first_down_stop = not_first_down.loc[data['DN'] == 1]
first_down_conversion = got_first_down.loc[data['DN'] == 1]

second_down = data.loc[data['DN'] == 2]
second_down_stop = not_first_down.loc[data['DN'] == 2]
second_down_conversion = got_first_down.loc[data['DN'] == 2]

third_down = data.loc[data['DN'] == 3]
third_down_stop = not_first_down.loc[data['DN'] == 3]
third_down_conversion = got_first_down.loc[data['DN'] == 3]

fourth_down = data.loc[data['DN'] == 4]
fourth_down_stop = not_first_down.loc[data['DN'] == 4]
fourth_down_conversion = got_first_down.loc[data['DN'] == 4]

formations = set(OFF_FORM)
plays = set(OFF_PLAY)

print('\n \n \n \n')

print("******* EACH TIME EACH FORMATION WAS USED *******\n\n")

i = 0
for form in formations:
    print('**** Formation: ' + str(form) + ' ****\n')

    plays_in_this_formation = []
    
    plays_in_this_formation = data.loc[data['OFF FORM'] == form]
    plays_in_this_formation = pd.DataFrame.from_records(plays_in_this_formation)
    plays_in_this_formation.reset_index()
    print(plays_in_this_formation)
    print('\n')

    if len(plays_in_this_formation) == 1:
        string = np.array([len(plays_in_this_formation), "total play run from the", str(form), "formation"])
    else:
        string = np.array([len(plays_in_this_formation), "total plays run from the", str(form), "formation"])
    print(' '.join(string))

    run_count = 0
    run_count += plays_in_this_formation.loc[plays_in_this_formation['PLAY TYPE'] == 'Run'].size / 9
    string = np.array([run_count, "run plays"])
    print(' '.join(string))

    pass_count = 0
    pass_count += plays_in_this_formation.loc[plays_in_this_formation['PLAY TYPE'] == 'Pass'].size / 9
    string = np.array([pass_count, "pass plays"])
    print(' '.join(string))

    penalty_plays = plays_in_this_formation.loc[plays_in_this_formation['RESULT'] == 'Penalty']

    defensive_penalty_count = 0
    defensive_penalty_count += penalty_plays.loc[penalty_plays['GN/LS'] > 0].size / 9
    if defensive_penalty_count == 1:
        string = np.array([defensive_penalty_count, "defensive penalty"])
    else:
        string = np.array([defensive_penalty_count, "defensive penalties"])
    print(' '.join(string))

    offensive_penalty_count = 0
    offensive_penalty_count += penalty_plays.loc[penalty_plays['GN/LS'] < 0].size / 9
    if offensive_penalty_count == 1:
        string = np.array([offensive_penalty_count, "offensive penalty"])
    else:
        string = np.array([offensive_penalty_count, "offensive penalties"])
    print(' '.join(string))

    yards = plays_in_this_formation.loc[:,'GN/LS']
    yards = np.array(yards)

    plays_no_pens = plays_in_this_formation.loc[plays_in_this_formation['RESULT'] != 'Penalty']
    yards_no_pen = plays_no_pens.loc[:,'GN/LS']
    yards_no_pen = np.array(yards_no_pen)

    avg = np.mean(yards)
    string = np.array(["Mean yards gained: ", avg, "yds"])
    print(''.join(string))

    med = np.median(yards)
    string = np.array(["Median yards gained: ", med, "yds"])
    print(''.join(string))

    long_play = np.max(yards)
    string = np.array(["Longest play: ", long_play, "yds"])
    print(''.join(string))

    short_play = np.min(yards)
    string = np.array(["Shortest play or Largest loss: ", short_play, "yds"])
    print(''.join(string))

    total = np.sum(yards)
    string = np.array(["Total yards from formation: ", total, "yds"])
    print(''.join(string))

    
    if defensive_penalty_count != 0 and offensive_penalty_count != 0:
        print('\nNot Including Penalties:')

        avg_no_pen = np.mean(yards_no_pen)
        string = np.array(["Mean yards gained: ", avg_no_pen, "yds"])
        print(''.join(string))

        med_no_pen = np.median(yards_no_pen)
        string = np.array(["Median yards gained: ", med_no_pen, "yds"])
        print(''.join(string))

        long_play_no_pen = np.max(yards_no_pen)
        string = np.array(["Longest play: ", long_play_no_pen, "yds"])
        print(''.join(string))

        short_play_no_pen = np.min(yards_no_pen)
        string = np.array(["Shortest play or Largest loss: ", short_play_no_pen, "yds"])
        print(''.join(string))

        total_no_pen = np.sum(yards_no_pen)
        string = np.array(["Total yards from formation: ", total_no_pen, "yds"])
        print(''.join(string))

    print('\n \n \n \n')
    i += 1


print("******* EACH TIME EACH PLAY WAS RUN *******\n\n")

i = 0
for play in plays:
    print('**** Play: ' + str(play) + ' ****\n')

    instances_of_this_play = []
    
    instances_of_this_play = data.loc[data['OFF PLAY'] == play]
    instances_of_this_play = pd.DataFrame.from_records(instances_of_this_play)
    instances_of_this_play.reset_index()
    print(instances_of_this_play)
    print('\n')

    if len(instances_of_this_play) == 1:
        string = np.array(["The", str(play), "play was run", len(instances_of_this_play), "time"])
    else:
        string = np.array(["The", str(play), "play was run", len(instances_of_this_play), "times"])
    print(' '.join(string))

    run_count = 0
    run_count += instances_of_this_play.loc[instances_of_this_play['PLAY TYPE'] == 'Run'].size / 9
    string = np.array([run_count, "run plays"])
    print(' '.join(string))

    pass_count = 0
    pass_count += instances_of_this_play.loc[instances_of_this_play['PLAY TYPE'] == 'Pass'].size / 9
    string = np.array([pass_count, "pass plays"])
    print(' '.join(string))

    penalty_plays = instances_of_this_play.loc[instances_of_this_play['RESULT'] == 'Penalty']

    defensive_penalty_count = 0
    defensive_penalty_count += penalty_plays.loc[penalty_plays['GN/LS'] > 0].size / 9
    if defensive_penalty_count == 1:
        string = np.array([defensive_penalty_count, "defensive penalty"])
    else:
        string = np.array([defensive_penalty_count, "defensive penalties"])
    print(' '.join(string))

    offensive_penalty_count = 0
    offensive_penalty_count += penalty_plays.loc[penalty_plays['GN/LS'] < 0].size / 9
    if offensive_penalty_count == 1:
        string = np.array([offensive_penalty_count, "offensive penalty"])
    else:
        string = np.array([offensive_penalty_count, "offensive penalties"])
    print(' '.join(string))

    yards = instances_of_this_play.loc[:,'GN/LS']
    yards = np.array(yards)

    plays_no_pens = instances_of_this_play.loc[instances_of_this_play['RESULT'] != 'Penalty']
    yards_no_pen = plays_no_pens.loc[:,'GN/LS']
    yards_no_pen = np.array(yards_no_pen)

    avg = np.mean(yards)
    string = np.array(["Mean yards gained: ", avg, "yds"])
    print(''.join(string))

    med = np.median(yards)
    string = np.array(["Median yards gained: ", med, "yds"])
    print(''.join(string))

    long_play = np.max(yards)
    string = np.array(["Longest play: ", long_play, "yds"])
    print(''.join(string))

    short_play = np.min(yards)
    string = np.array(["Shortest play or Largest loss: ", short_play, "yds"])
    print(''.join(string))

    total = np.sum(yards)
    string = np.array(["Total yards from formation: ", total, "yds"])
    print(''.join(string))

    
    if defensive_penalty_count != 0 and offensive_penalty_count != 0:
        print('\nNot Including Penalties:')

        avg_no_pen = np.mean(yards_no_pen)
        string = np.array(["Mean yards gained: ", avg_no_pen, "yds"])
        print(''.join(string))

        med_no_pen = np.median(yards_no_pen)
        string = np.array(["Median yards gained: ", med_no_pen, "yds"])
        print(''.join(string))

        long_play_no_pen = np.max(yards_no_pen)
        string = np.array(["Longest play: ", long_play_no_pen, "yds"])
        print(''.join(string))

        short_play_no_pen = np.min(yards_no_pen)
        string = np.array(["Shortest play or Largest loss: ", short_play_no_pen, "yds"])
        print(''.join(string))

        total_no_pen = np.sum(yards_no_pen)
        string = np.array(["Total yards from formation: ", total_no_pen, "yds"])
        print(''.join(string))


    print('\n \n \n \n')
    i += 1