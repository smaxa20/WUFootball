import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)

# Change the file name of the Excel sheet of raw data under 'input_file_name'
input_file_name = "Practice2019.xlsx"
# The Excel file should be placed in a file called 'Data' the directory directly up the tree from this file
input_file_name = "../Data/" + input_file_name
# Make sure to specify the correct sheet name
sheet = "LaVerne Drives"
# Change the file name of the csv file for the report under 'output_file_name'
output_file_name = "report.csv"
# The report csv file will be place in a folder called 'Reports' in the directory directly up the tree from this file
output_file_name = "../Reports/" + output_file_name

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


got_first_down = data.loc[data['GN/LS'] >= data['DIST']]
not_first_down = data.loc[data['GN/LS'] < data['DIST']]

third_down = data.loc[data['DN'] == 3]
third_down_stop = not_first_down.loc[data['DN'] == 3]
third_down_conversion = got_first_down.loc[data['DN'] == 3]

fourth_down = data.loc[data['DN'] == 4]
fourth_down = fourth_down.loc[fourth_down['ODK'] != 'K']
fourth_down_stop = not_first_down.loc[data['DN'] == 4]
fourth_down_stop = fourth_down_stop.loc[fourth_down_stop['ODK'] != 'K']
fourth_down_conversion = got_first_down.loc[data['DN'] == 4]
fourth_down_conversion = fourth_down_conversion.loc[fourth_down_conversion['ODK'] != 'K']

formations = set(OFF_FORM)
plays = set(OFF_PLAY)

print('\n \n \n \n')

drive_summary = []
exp_run_results = []
exp_pass_results = []
negative_results = []
shot_results = []
redzone_results = []
goalline_results = []
third_down_results = []
third_down_conversion_results = []
third_down_stop_results = []
fourth_down_results = []
fourth_down_conversion_results = []
fourth_down_stop_results = []
i = -1
while i+1 < len(PLAY_NUM):
    play_count = 0
    yard_count = 0
    run_count = 0
    pass_count = 0
    exp_run_count = 0
    exp_pass_count = 0
    negative_count = 0  
    shot_count = 0
    redzone_count = 0  
    goalline_count = 0
    third_down_count = 0
    third_down_conversion_count = 0
    third_down_stop_count = 0
    fourth_down_count = 0
    fourth_down_conversion_count = 0
    fourth_down_stop_count = 0
    while True:
        i += 1
        play_count += 1
        yard_count += GN_LS[i]

        if PLAY_TYPE[i] == 'Run':
            run_count += 1
            if GN_LS[i] >= 12:
                exp_run_count += 1 
        elif PLAY_TYPE[i] == 'Pass':
            pass_count += 1
            if GN_LS[i] >= 20:
                shot_count += 1
            if GN_LS[i] >= 16:
                exp_pass_count += 1

        if YARD_LN[i] <= 25 and YARD_LN[i] > 0 and PLAY_TYPE[i] != 'Extra Pt.':
            redzone_count += 1
        
        if YARD_LN[i] <= 5 and YARD_LN[i] > 0 and PLAY_TYPE[i] != 'Extra Pt.':
            goalline_count += 1

        if DN[i] == 3:
            third_down_count += 1
            if DIST[i] <= GN_LS[i]:
                third_down_conversion_count += 1
            else:
                third_down_stop_count += 1

        if DN[i] == 4 and ODK[i] != 'K':
            fourth_down_count += 1
            if DIST[i] <= GN_LS[i]:
                fourth_down_conversion_count += 1
            else:
                fourth_down_stop_count += 1
           
        result = RESULT[i]
        if i+1 == len(PLAY_NUM) or PLAY_NUM[i+1] - PLAY_NUM[i] > 1 or result == 'Fumble' or result == 'Complete, Fumble' or result == 'Rush, Fumble' or result == 'Sack, Fumble' or result == 'Scramble, Fumble' or result == 'Fumble, Def TD' or result == 'Complete, Fumble, Def TD' or result == 'Rush, Fumble, TD' or result == 'Sack, Fumble, Def TD' or result == 'Scramble, Fumble, Def TD' or result == 'Interception' or result == "interception, Def TD" or result == 'Sack, Safety' or result == 'Rush, Safety' or result == 'Complete, Safety' or result == 'Scramble, Safety':
            if DN[i] == 4 and (result == 'Complete' or result == 'Incomplete' or result == 'Rush' or result == 'Scramble' or result == 'Penalty' or result == 'Sack'):
                result = 'Downs'
            elif result == 'Complete, TD':
                result = 'Pass TD'
            elif result == 'Rush, TD':
                result = 'Rush TD'
            elif result == 'Scramble, TD':
                result = 'Scramble TD'
            elif result == 'Good' and PLAY_TYPE[i] == 'Extra Pt.':
                if RESULT[i-1] == 'Complete, TD':
                    result = 'Pass TD + PAT'
                elif RESULT[i-1] == 'Rush, TD':
                    result = 'Rush TD + PAT'
                elif RESULT[i-1] == 'Scramble, TD':
                    result = 'Scramble TD + PAT'
            elif result == 'Miss' and PLAY_TYPE[i] == 'Extra Pt.':
                if RESULT[i-1] == 'Complete, TD':
                    result = 'Pass TD - PAT'
                elif RESULT[i-1] == 'Rush, TD':
                    result = 'Rush TD - PAT'
                elif RESULT[i-1] == 'Scramble, TD':
                    result = 'Scramble TD - PAT'
            elif result == 'Good' and PLAY_TYPE[i] == 'FG':
                result = 'Made FG'
            elif result == 'Miss' and PLAY_TYPE[i] == 'FG':
                result = 'Missed FG'
            elif result == 'Fumble' or result == 'Complete, Fumble' or result == 'Rush, Fumble' or result == 'Sack, Fumble' or result == 'Scramble, Fumble':
                result = 'Fumble'
            elif result == 'Fumble, Def TD' or result == 'Complete, Fumble, Def TD' or result == 'Rush, Fumble, TD' or result == 'Sack, Fumble, Def TD' or result == 'Scramble, Fumble, Def TD':
                result = 'Fumble, Def TD'
            elif result == 'Interception':
                result = 'INT'
            elif result == 'Interception, Def TD':
                result = 'INT, Def TD'
            elif result == 'Sack, Safety' or result == 'Rush, Safety' or result == 'Complete, Safety' or result == 'Scramble, Safety':
                result = 'Safety'
            elif PLAY_TYPE[i] == 'Punt':
                result = 'Punt'
            elif PLAY_TYPE[i] == 'KO':
                result = RESULT[i-1]

            RESULT[i] = result

        if (GN_LS[i] < 0 or result == 'Fumble' or result == 'Fumble, Def TD' or result == 'INT' or result == 'INT, Def TD' or result == 'Safety') and ODK[i] == 'O':
            negative_count += 1

        if i+1 == len(PLAY_NUM) or PLAY_NUM[i+1] - PLAY_NUM[i] > 1 or result == 'Fumble' or result == 'Complete, Fumble' or result == 'Rush, Fumble' or result == 'Sack, Fumble' or result == 'Scramble, Fumble' or result == 'Fumble, Def TD' or result == 'Complete, Fumble, Def TD' or result == 'Rush, Fumble, TD' or result == 'Sack, Fumble, Def TD' or result == 'Scramble, Fumble, Def TD' or result == 'Interception' or result == "interception, Def TD" or result == 'Sack, Safety' or result == 'Rush, Safety' or result == 'Complete, Safety' or result == 'Scramble, Safety':
            this_drive = {
                'Play Count' : play_count,
                'Avg yd/play' : np.around(yard_count/play_count,2),
                'Run' : run_count,
                'Pass' : pass_count,
                'Explosives' : exp_run_count + exp_pass_count,
                'Negatives' : negative_count,
                'Drive Result' : result
            }

            for x in range(exp_run_count):
                exp_run_results.append(result)

            for x in range(exp_pass_count):
                exp_pass_results.append(result)

            for x in range(negative_count):
                negative_results.append(result)

            for x in range(shot_count):
                shot_results.append(result)

            for x in range(redzone_count):
                redzone_results.append(result)

            for x in range(goalline_count):
                goalline_results.append(result)

            for x in range(third_down_count):
                third_down_results.append(result)

            for x in range(third_down_conversion_count):
                third_down_conversion_results.append(result)

            for x in range(third_down_stop_count):
                third_down_stop_results.append(result)

            for x in range(fourth_down_count):
                fourth_down_results.append(result)

            for x in range(fourth_down_conversion_count):
                fourth_down_conversion_results.append(result)

            for x in range(fourth_down_stop_count):
                fourth_down_stop_results.append(result)

            drive_summary.append(this_drive)
            break

print("******* DRIVE SUMMARY *******\n\n")

drive_summary = pd.DataFrame.from_records(drive_summary)
drive_summary = drive_summary[['Play Count', 'Avg yd/play', 'Run', 'Pass', 'Explosives', 'Negatives', 'Drive Result']]
drive_summary.reset_index()
# del drive_summary['index']
print(drive_summary)




print("\n\n\n\n******* EXPLOSIVE PLAY REPORT *******")

run_plays = data.loc[data['PLAY TYPE'] == 'Run']
explosive_runs = run_plays.loc[run_plays['GN/LS'] >= 12]
explosive_runs = explosive_runs.reset_index()
del explosive_runs['index']
pass_plays = data.loc[data['PLAY TYPE'] == 'Pass']
explosive_passes = pass_plays.loc[pass_plays['GN/LS'] >= 16]
explosive_passes = explosive_passes.reset_index()
del explosive_passes['index']

explosive_runs.insert(len(explosive_runs.columns), 'DRIVE RESULT', exp_run_results)
explosive_passes.insert(len(explosive_passes.columns), 'DRIVE RESULT', exp_pass_results)

print("\n\n\n******* RUN PLAYS *******")
print(explosive_runs)

print("\n\n\n******* PASS PLAYS *******")
print(explosive_passes)



print("\n\n\n\n******* NEGATIVE PLAY REPORT *******\n\n\n")

negative_plays = data.loc[data['GN/LS'] < 0]
nonnegative_plays = data.loc[data['GN/LS'] >= 0]

# Use nonnegative_plays here instead of data 
# because we only want to add plays not previously added in the creation of negative_plays
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Fumble'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Complete, Fumble'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Rush, Fumble'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Sack, Fumble'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Scramble, Fumble'])

negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Fumble, Def TD'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Complete, Fumble, Def TD'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Rush, Fumble, Def TD'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Sack, Fumble, Def TD'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Scramble, Fumble, Def TD'])

negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Sack, Safety'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Rush, Safety'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Complete, Safety'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Scramble, Safety'])

negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Interception'])
negative_plays = negative_plays.append(nonnegative_plays.loc[nonnegative_plays['RESULT'] == 'Interception, Def TD'])

negative_plays = negative_plays.sort_values( 'PLAY #')
negative_plays = negative_plays.reset_index()
del negative_plays['index']
negative_plays.insert(len(negative_plays.columns), 'DRIVE RESULT', negative_results)
print(negative_plays)



print("\n\n\n\n******* SHOT PLAY REPORT *******\n\n\n")

shot_plays = pass_plays.loc[pass_plays['GN/LS'] >= 20]
shot_plays.insert(len(shot_plays.columns), 'DRIVE RESULT', shot_results)
shot_plays = shot_plays.reset_index()
del shot_plays['index']
print(shot_plays)




print("\n\n\n\n******* RED ZONE REPORT *******\n\n\n")

plays_in_redzone = data.loc[data['YARD LN'] <= 25]
plays_in_redzone = plays_in_redzone.loc[plays_in_redzone['YARD LN'] > 0]
plays_in_redzone = plays_in_redzone.loc[plays_in_redzone['PLAY TYPE'] != 'Extra Pt.']
plays_in_redzone.insert(len(plays_in_redzone.columns), 'DRIVE RESULT', redzone_results)
plays_in_redzone = plays_in_redzone.reset_index()
del plays_in_redzone['index']
print(plays_in_redzone)




print("\n\n\n\n ******* GOAL LINE REPORT *******\n\n\n")

plays_on_goalline = data.loc[data['YARD LN'] <= 5]
plays_on_goalline = plays_on_goalline.loc[plays_on_goalline['YARD LN'] > 0]
plays_on_goalline = plays_on_goalline.loc[plays_on_goalline['PLAY TYPE'] != 'Extra Pt.']
plays_on_goalline.insert(len(plays_on_goalline.columns), 'DRIVE RESULT', goalline_results)
plays_on_goalline = plays_on_goalline.reset_index()
del plays_on_goalline['index']
print(plays_on_goalline)




print("\n\n\n\n******* 3RD DOWN REPORT *******")

if len(third_down) != 0:
    string = np.array(["Conversion Rate: ", len(third_down_conversion), "/", len(third_down), " = ", np.around(float(len(third_down_conversion)) / float(len(third_down)) * 100, 2), "%"])
else:
    string = np.array(["Conversion Rate: ", len(third_down_conversion), "/", len(third_down), " = 0.0%"])
print(''.join(string))

run_count = third_down.loc[third_down['PLAY TYPE'] == 'Run'].size / 11
run_conversion_count = third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Run'].size / 11
if run_count != 0:
    string = np.array(["Rushing Conversion Rate: ", run_conversion_count, "/", run_count, " = ", np.around(float(run_conversion_count) / float(run_count) * 100, 2), "%"])
else:
    string = np.array(["Rushing Conversion Rate: ", run_conversion_count, "/", run_count, " = 0.0%"])
print(''.join(string))

pass_count = third_down.loc[third_down['PLAY TYPE'] == 'Pass'].size / 11
pass_conversion_count = third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Pass'].size / 11
if pass_count != 0:
    string = np.array(["Passing Conversion Rate: ", pass_conversion_count, "/", pass_count, " = ", np.around(float(pass_conversion_count) / float(pass_count) * 100, 2), "%"])
else:
    string = np.array(["Passing Conversion Rate: ", pass_conversion_count, "/", pass_count, " = 0.0%"])
print(''.join(string))
print('\n\n')


print("TOTAL\n")

count = len(third_down)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = third_down.loc[third_down['PLAY TYPE'] == 'Run'].size / 11
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = third_down.loc[third_down['PLAY TYPE'] == 'Pass'].size / 11
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

third_down = third_down.reset_index()
del third_down['index']

if len(third_down) > 0:
    third_down.insert(len(third_down.columns), 'DRIVE RESULT', third_down_results)
    print(third_down)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(third_down.loc[third_down['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(third_down.loc[third_down['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\n******* GAINED FIRST DOWN *******\n")

count = len(third_down_conversion)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Run'].size / 11
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Pass'].size / 11
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

third_down_conversion = third_down_conversion.reset_index()
del third_down_conversion['index']

if len(third_down_conversion) > 0:
    third_down_conversion.insert(len(third_down_conversion.columns), 'DRIVE RESULT', third_down_conversion_results)
    print(third_down_conversion)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(third_down_conversion.loc[third_down_conversion['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(third_down_conversion.loc[third_down_conversion['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\n******* STOPPED SHORT *******\n")

count = len(third_down_stop)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = third_down_stop.loc[third_down_stop['PLAY TYPE'] == 'Run'].size / 11
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = third_down_stop.loc[third_down_stop['PLAY TYPE'] == 'Pass'].size / 11
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

third_down_stop = third_down_stop.reset_index()
del third_down_stop['index']

if len(third_down_stop) > 0:
    third_down_stop.insert(len(third_down_stop.columns), 'DRIVE RESULT', third_down_stop_results)
    print(third_down_stop)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(third_down_stop.loc[third_down_stop['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(third_down_stop.loc[third_down_stop['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")




print("\n\n\n\n******* 4th DOWN REPORT *******")

if len(fourth_down) != 0:
    string = np.array(["Conversion Rate: ", len(fourth_down_conversion), "/", len(fourth_down), " = ", np.around(float(len(fourth_down_conversion)) / float(len(fourth_down)) * 100, 2), "%"])
else:
    string = np.array(["Conversion Rate: ", len(fourth_down_conversion), "/", len(fourth_down), " = 0.0%"])
print(''.join(string))

run_count = fourth_down.loc[fourth_down['PLAY TYPE'] == 'Run'].size / 11
run_conversion_count = fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Run'].size / 11
if run_count != 0:
    string = np.array(["Rushing Conversion Rate: ", run_conversion_count, "/", run_count, " = ", np.around(float(run_conversion_count) / float(run_count) * 100, 2), "%"])
else:
    string = np.array(["Rushing Conversion Rate: ", run_conversion_count, "/", run_count, " = 0.0%"])
print(''.join(string))

pass_count = fourth_down.loc[fourth_down['PLAY TYPE'] == 'Pass'].size / 11
pass_conversion_count = fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Pass'].size / 11
if pass_count != 0:
    string = np.array(["Passing Conversion Rate: ", pass_conversion_count, "/", pass_count, " = ", np.around(float(pass_conversion_count) / float(pass_count) * 100, 2), "%"])
else:
    string = np.array(["Passing Conversion Rate: ", pass_conversion_count, "/", pass_count, " = 0.0%"])
print(''.join(string))
print('\n\n')


print("TOTAL\n")

count = len(fourth_down)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = fourth_down.loc[fourth_down['PLAY TYPE'] == 'Run'].size / 11
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = fourth_down.loc[fourth_down['PLAY TYPE'] == 'Pass'].size / 11
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

fourth_down = fourth_down.reset_index()
del fourth_down['index']

if len(fourth_down) > 0:
    fourth_down.insert(len(fourth_down.columns), 'DRIVE RESULT', fourth_down_results)
    print(fourth_down)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(fourth_down.loc[fourth_down['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(fourth_down.loc[fourth_down['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\n******* GAINED FIRST DOWN *******\n")

count = len(fourth_down_conversion)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Run'].size / 11
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Pass'].size / 11
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

fourth_down_conversion = fourth_down_conversion.reset_index()
del fourth_down_conversion['index']

if len(fourth_down_conversion) > 0:
    fourth_down_conversion.insert(len(fourth_down_conversion.columns), 'DRIVE RESULT', fourth_down_conversion_results)
    print(fourth_down_conversion)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(fourth_down_conversion.loc[fourth_down_conversion['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(fourth_down_conversion.loc[fourth_down_conversion['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\n******* STOPPED SHORT *******\n")

count = len(fourth_down_stop)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = fourth_down_stop.loc[fourth_down_stop['PLAY TYPE'] == 'Run'].size / 11
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = fourth_down_stop.loc[fourth_down_stop['PLAY TYPE'] == 'Pass'].size / 11
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

fourth_down_stop = fourth_down_stop.reset_index()
del fourth_down_stop['index']

if len(fourth_down_stop) > 0:
    fourth_down_stop.insert(len(fourth_down_stop.columns), 'DRIVE RESULT', fourth_down_stop_results)
    print(fourth_down_stop)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(fourth_down_stop.loc[fourth_down_stop['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(fourth_down_stop.loc[fourth_down_stop['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")

print('\n\n\n\n')


with open(output_file_name, 'a') as f:
    if len(drive_summary) > 0:
        f.write('Drive Summary,\n')
        drive_summary.to_csv(f, index=False)
    else:
        f.write('No data for Drive Summary,\n')

    if len(explosive_runs) > 0:
        f.write('\n,Explosive Runs,\n')
        explosive_runs.to_csv(f, index=False)
    else:
        f.write('\n,No data for Explosive Runs,\n')

    if len(explosive_passes) > 0:
        f.write('\n,Explosive Passes,\n')
        explosive_passes.to_csv(f, index=False)
    else:
        f.write('\n,No data for Explosive Passes,\n')

    if len(negative_plays) > 0:
        f.write('\n,Negative Plays,\n')
        negative_plays.to_csv(f, index=False)
    else:
        f.write('\n,No data for Negative Plays,\n')

    if len(shot_plays) > 0:
        f.write('\n,Shot Plays,\n')
        shot_plays.to_csv(f, index=False)
    else:
        f.write('\n,No data for Shot Plays,\n')

    if len(plays_in_redzone) > 0:
        f.write('\n,Redzone,\n')
        plays_in_redzone.to_csv(f, index=False)
    else:
        f.write('\n,No data for Redzone,\n')

    if len(plays_on_goalline) > 0:
        f.write('\n,Goalline,\n')
        plays_on_goalline.to_csv(f, index=False)
    else:
        f.write('\n,No data for Goalline,\n')

    if len(third_down) > 0:
        f.write('\n,Third Down Total,\n')
        third_down.to_csv(f, index=False)
    else:
        f.write('\n,No data for Third Down Total,\n')

    if len(third_down_conversion) > 0:
        f.write('\n,Third Down Conversions,\n')
        third_down_conversion.to_csv(f, index=False)
    else:
        f.write('\n,No data for Third Down Conversions,\n')

    if len(third_down_stop) > 0:
        f.write('\n,Third Down Stops,\n')
        third_down_stop.to_csv(f, index=False)
    else:
        f.write('\n,No data for Third Down Stops,\n')

    if len(fourth_down) > 0:
        f.write('\n,Fourth Down Total,\n')
        fourth_down.to_csv(f, index=False)
    else:
        f.write('\n,No data for Fourth Down Total,\n')

    if len(fourth_down_conversion) > 0:
        f.write('\n,Fourth Down Conversions,\n')
        fourth_down_conversion.to_csv(f, index=False)
    else:
        f.write('\n,No data for Fourth Down Conversions,\n')

    if len(fourth_down_stop) > 0:
        f.write('\n,Fourth Down ,\n')
        fourth_down_stop.to_csv(f, index=False)
    else:
        f.write('\n,No data for Fourth Down Stops,\n')
