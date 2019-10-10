import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)

# Change the file name of the Excel sheet of raw data under 'input_file_name'
input_file_name = "Willamette2019Data.xlsx"
# The Excel file should be placed in a file called 'Data' the directory directly up the tree from this file
input_file_name = "../../Data/" + input_file_name
# Make sure to specify the correct sheet name
sheet = "Willamette Data"
# Change the file name of the csv file for the report under 'output_file_name'
output_file_name = "report.csv"
# The report csv file will be place in a folder called 'Reports' in the directory directly up the tree from this file
output_file_name = "../../Reports/" + output_file_name

data = pd.read_excel(input_file_name, sheet, index_col = None, header = 0, na_values = ' ')
data = data.sort_values('PLAY #')
data = data.reset_index()
del data['index']
data = data.dropna(how = 'all')
data = data.fillna(0)

# Uncomment below if the Excel sheet is set up with extra, undesired columns
# Switch the values in undesired_columns to the names of the undesired columns

# undesired_columns = np.array(['ODK'])
# for col_name in undesired_columns:
#     del data[col_name]

ODK = data.loc[:, 'ODK']
PLAY_NUM = data.loc[:,'PLAY #'].astype('int32')
DN = data.loc[:,'DN'].astype('int32')
DIST = data.loc[:,'DIST'].astype('int32')
HASH = data.loc[:,'HASH']
YARD_LN = data.loc[:,'YARD LN'].astype('int32')
PLAY_TYPE = data.loc[:,'PLAY TYPE']
GN_LS = data.loc[:,'GN/LS'].astype('int32')
RESULT = data.loc[:,'RESULT']
OFF_FORM = data.loc[:,'OFF FORM']
OFF_PLAY = data.loc[:,'OFF PLAY']

# This loop and the astype functions above convert all of the numerical data from floats to ints
new_data = []
i = 0
while i < len(PLAY_NUM):
    row = {
        'ODK' : ODK[i],
        'PLAY #' : PLAY_NUM[i],
        'DN' : DN[i],
        'DIST' : DIST[i],
        'HASH' : HASH[i],
        'YARD LN' : YARD_LN[i],
        'PLAY TYPE' : PLAY_TYPE[i],
        'GN/LS' : GN_LS[i],
        'RESULT' : RESULT[i],
        'OFF FORM' : OFF_FORM[i],
        'OFF PLAY' : OFF_PLAY[i]
    }
    new_data.append(row)
    i += 1
data = pd.DataFrame.from_records(new_data)
data = data[['ODK', 'PLAY #', 'DN', 'DIST', 'HASH', 'YARD LN', 'PLAY TYPE', 'GN/LS', 'RESULT', 'OFF FORM', 'OFF PLAY']]


formations = set(OFF_FORM)
printable_formations = []
for form in formations:
    plays_in_this_formation = data.loc[data['OFF FORM'] == form]
    plays_in_this_formation = pd.DataFrame.from_records(plays_in_this_formation)
    plays_in_this_formation.reset_index()
    printable_formations.append(plays_in_this_formation)


plays = set(OFF_PLAY)
printable_plays = []
for play in plays:
    instances_of_this_play = data.loc[data['OFF PLAY'] == play]
    instances_of_this_play = pd.DataFrame.from_records(instances_of_this_play)
    instances_of_this_play.reset_index()
    printable_plays.append(instances_of_this_play)


with open(output_file_name, 'a') as f:
    print("Writing Formations...")
    for form in printable_formations:
        if len(form) > 0:
            penalty_plays = form.loc[form['RESULT'] == 'Penalty']
            yards = np.array(form.loc[:,'GN/LS'])

            f.write(str(form.loc[:,'OFF FORM'][0]) + '\n')
            form.to_csv(f, index=False)
            f.write(str(len(form)) + ' total plays\n')
            f.write(str(len(form.loc[form['PLAY TYPE'] == 'Run'])) + ' run plays\n')
            f.write(str(len(form.loc[form['PLAY TYPE'] == 'Pass'])) + ' pass plays\n')

            f.write(str(len(penalty_plays.loc[penalty_plays['GN/LS'] > 0])))
            if (len(penalty_plays.loc[penalty_plays['GN/LS'] > 0]) == 1):
                f.write(' defensive penalty\n')
            else:
                f.write(' defensive penalties\n')
                
            f.write(str(len(penalty_plays.loc[penalty_plays['GN/LS'] < 0])))
            if (len(penalty_plays.loc[penalty_plays['GN/LS'] < 0]) == 1):
                f.write(' offensive penalty\n')
            else:
                f.write(' offensive penalties\n')

            f.write('Mean yards gained: ' + str(np.around(np.mean(yards), 1)) + 'yds\n')
            f.write('Median yards gained: ' + str(np.median(yards)) + 'yds\n')
            f.write('Largest gain: ' + str(int(np.max(yards))) + 'yds\n')
            f.write('Smallest gain/Largest loss: ' + str(int(np.min(yards))) + 'yds\n')
            f.write('Total yards gained: ' + str(int(np.sum(yards))) + 'yds\n')

            if len(penalty_plays) != 0:
                plays_no_pens = form.loc[form['RESULT'] != 'Penalty']
                yards_no_pen = plays_no_pens.loc[:,'GN/LS']
                yards_no_pen = np.array(yards_no_pen)

                f.write('\nNot Including Penalties:\n')
                f.write('Mean yards gained: ' + str(np.around(np.mean(yards_no_pen), 1)) + 'yds\n')
                f.write('Median yards gained: ' + str(np.median(yards_no_pen)) + 'yds\n')
                f.write('Largest gain: ' + str(int(np.max(yards_no_pen))) + 'yds\n')
                f.write('Smallest gain/Largest loss: ' + str(int(np.min(yards_no_pen))) + 'yds\n')
                f.write('Total yards gained: ' + str(int(np.sum(yards_no_pen))) + 'yds\n')
            f.write('\n')
    print("Done")
    print("Writing Plays...")
    for play in printable_plays:
        if len(play) > 0:
            penalty_plays = play.loc[play['RESULT'] == 'Penalty']
            yards = np.array(play.loc[:,'GN/LS'])

            f.write(str(play.loc[:,'OFF PLAY'][0]) + '\n')
            play.to_csv(f, index=False)
            f.write(str(len(play)) + ' total plays\n')
            f.write(str(len(play.loc[play['PLAY TYPE'] == 'Run'])) + ' run plays\n')
            f.write(str(len(play.loc[play['PLAY TYPE'] == 'Pass'])) + ' pass plays\n')

            f.write(str(len(penalty_plays.loc[penalty_plays['GN/LS'] > 0])))
            if (len(penalty_plays.loc[penalty_plays['GN/LS'] > 0]) == 1):
                f.write(' defensive penalty\n')
            else:
                f.write(' defensive penalties\n')
                
            f.write(str(len(penalty_plays.loc[penalty_plays['GN/LS'] < 0])))
            if (len(penalty_plays.loc[penalty_plays['GN/LS'] < 0]) == 1):
                f.write(' offensive penalty\n')
            else:
                f.write(' offensive penalties\n')

            f.write('Mean yards gained: ' + str(np.around(np.mean(yards), 1)) + 'yds\n')
            f.write('Median yards gained: ' + str(np.median(yards)) + 'yds\n')
            f.write('Largest gain: ' + str(int(np.max(yards))) + 'yds\n')
            f.write('Smallest gain/Largest loss: ' + str(int(np.min(yards))) + 'yds\n')
            f.write('Total yards gained: ' + str(int(np.sum(yards))) + 'yds\n')

            if len(penalty_plays) != 0:
                plays_no_pens = play.loc[play['RESULT'] != 'Penalty']
                yards_no_pen = plays_no_pens.loc[:,'GN/LS']
                yards_no_pen = np.array(yards_no_pen)

                f.write('\nNot Including Penalties:\n')
                f.write('Mean yards gained: ' + str(np.around(np.mean(yards_no_pen), 1)) + 'yds\n')
                f.write('Median yards gained: ' + str(np.median(yards_no_pen)) + 'yds\n')
                f.write('Largest gain: ' + str(int(np.max(yards_no_pen))) + 'yds\n')
                f.write('Smallest gain/Largest loss: ' + str(int(np.min(yards_no_pen))) + 'yds\n')
                f.write('Total yards gained: ' + str(int(np.sum(yards_no_pen))) + 'yds\n')
            f.write('\n')
    print("Done")
