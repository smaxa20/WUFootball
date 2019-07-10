import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)

# Change the file name of the Excel sheet of raw data under 'input_file_name'
input_file_name = "GeorgeFox2018DefensiveBreakdown.xlsx"
# The Excel file should be placed in a file called 'Data' the directory directly up the tree from this file
input_file_name = "../../Data/" + input_file_name
# Make sure to specify the correct sheet name
sheet = "Fox Scout Data"
# Change the file name of the csv file for the report under 'output_file_name'
output_file_name = "report.csv"
# The report csv file will be place in a folder called 'Reports' in the directory directly up the tree from this file
output_file_name = "../../Reports/" + output_file_name

data = pd.read_excel(input_file_name, sheet, index_col = None, header = 0, na_values = ' ')
data = data.reset_index()
del data['index']
data = data.dropna(how = 'all')
data = data.fillna(1001)

# Uncomment below if the Excel sheet is set up with extra, undesired columns
# Switch the values in undesired_columns to the names of the undesired columns

# undesired_columns = np.array(['ODK'])
# for col_name in undesired_columns:
#     del data[col_name]


# This loop and the astype functions above convert all of the numerical data from floats to ints
PLAY_NUM = data.loc[:,'PLAY #'].astype('int32')
DN = data.loc[:,'DN'].astype('int32')
DIST = data.loc[:,'DIST'].astype('int32')
HASH = data.loc[:,'HASH']
YARD_LN = data.loc[:,'YARD LN'].astype('int32')
PLAY_TYPE = data.loc[:,'PLAY TYPE']
GN_LS = data.loc[:,'GN/LS'].astype('int32')
RESULT = data.loc[:,'RESULT']
OFF_FORM = data.loc[:,'OFF FORM']
FRONT = data.loc[:,'FRONT'].astype('int32')
BLITZ = data.loc[:,'BLITZ']
S_ALIGN = data.loc[:,'S ALIGN'].astype('int32')
COVERAGE = data.loc[:,'COVERAGE'].astype('int32')

new_data = []
i = 0
while i < len(PLAY_NUM):
    row = {
        'PLAY #' : PLAY_NUM[i],
        'DN' : DN[i],
        'DIST' : DIST[i],
        'HASH' : HASH[i],
        'YARD LN' : YARD_LN[i],
        'PLAY TYPE' : PLAY_TYPE[i],
        'GN/LS' : GN_LS[i],
        'RESULT' : RESULT[i],
        'OFF FORM' : OFF_FORM[i],
        'FRONT' : FRONT[i],
        'BLITZ' : BLITZ[i],
        'S ALIGN' : S_ALIGN[i],
        'COVERAGE' : COVERAGE[i]
    }
    new_data.append(row)
    i += 1
data = pd.DataFrame.from_records(new_data)
data = data[['PLAY #', 'DN', 'DIST', 'HASH', 'YARD LN', 'PLAY TYPE', 'GN/LS', 'RESULT', 'OFF FORM', 'FRONT', 'BLITZ', 'S ALIGN', 'COVERAGE']]



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

# print("\n\n\n\n******* Safety Alignment Report *******")

safety_alignment_report = []
down = 0
while down < 5:
    if down == 0:
        label = 'Total'
        size = len(PLAY_NUM)
        down_data = data
    elif down == 1:
        label = '1st Down'
        size = len(first_down)
        down_data = first_down
    elif down == 2:
        label = '2nd Down'
        size = len(second_down)
        down_data = second_down
    elif down == 3:
        label = '3rd Down'
        size = len(third_down)
        down_data = third_down
    else:
        label = '4th Down'
        size = len(fourth_down)
        down_data = fourth_down
    row = {
        '' : label
    }
    safety = 0
    while safety < 4:
        percentage = str(np.around(float(len(down_data.loc[down_data['S ALIGN'] == safety])) / float(size) * 100, 2))
        if safety == 1:
            if float(percentage) == 0:
                row['1 Safety'] = '--'
            else:
                row['1 Safety'] = percentage + '% (' + str(len(down_data.loc[down_data['S ALIGN'] == safety])) + '/' + str(size) + ')'
        else:
            if float(percentage) == 0:
                row[str(safety) + ' Safeties'] = '--'
            else:
                row[str(safety) + ' Safeties'] = percentage + '% (' + str(len(down_data.loc[down_data['S ALIGN'] == safety])) + '/' + str(size) + ')'
        safety += 1
    safety_alignment_report.append(row)
    down += 1

safety_alignment_report = pd.DataFrame.from_records(safety_alignment_report)
safety_alignment_report = safety_alignment_report[['', '0 Safeties', '1 Safety', '2 Safeties', '3 Safeties']]
# print(safety_alignment_report)




# print("\n\n\n\n******* Coverage Report *******")

coverage_report = []
coverage = 0
while coverage < 9:
    if coverage == 5:
        new_coverage = 20
    elif coverage == 6:
        new_coverage = 34
    elif coverage == 7:
        new_coverage = 41
    elif coverage == 8:
        new_coverage = 43
    else:
        new_coverage = coverage
    row = {
        'Coverage' : new_coverage
    }
    safety = 0
    while safety < 4:
        percentage = str(np.around(float(len(data.loc[data['S ALIGN'] == safety].loc[data.loc[data['S ALIGN'] == safety]['COVERAGE'] == new_coverage])) / float(len(data.loc[data['S ALIGN'] == safety])) * 100, 2))
        if safety == 1:
            if float(percentage) == 0:
                row['1 Safety'] = '--'
            else:
                row['1 Safety'] = percentage + '% (' + str(len(data.loc[data['S ALIGN'] == safety].loc[data.loc[data['S ALIGN'] == safety]['COVERAGE'] == new_coverage])) + '/' + str(len(data.loc[data['S ALIGN'] == safety])) + ')'
        else:
            if float(percentage) == 0:
                row[str(safety) + ' Safeties'] = '--'
            else:
                row[str(safety) + ' Safeties'] = percentage + '% (' + str(len(data.loc[data['S ALIGN'] == safety].loc[data.loc[data['S ALIGN'] == safety]['COVERAGE'] == new_coverage])) + '/' + str(len(data.loc[data['S ALIGN'] == safety])) + ')'
        safety += 1
    coverage_report.append(row)
    coverage += 1

coverage_report = pd.DataFrame.from_records(coverage_report)
coverage_report = coverage_report[['Coverage', '0 Safeties', '1 Safety', '2 Safeties', '3 Safeties']]
# print(coverage_report)




negative_results = []
exp_pass_results = []
exp_run_results = []
shot_results = []
g_negative_count = 0
i = -1
while i+1 < len(PLAY_NUM):
    negative_count = 0
    exp_pass_count = 0
    exp_run_count = 0
    shot_count = 0
    while True:
        i += 1
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
                
        # if (GN_LS[i] <= 0 or result == 'Fumble' or result == 'Fumble, Def TD' or result == 'INT' or result == 'INT, Def TD' or result == 'Safety') and ODK[i] == 'O':
        if GN_LS[i] < 0 or result == 'Fumble' or result == 'Fumble, Def TD' or result == 'INT' or result == 'INT, Def TD' or result == 'Safety':
            negative_count += 1
            g_negative_count += 1
        elif GN_LS[i] >= 16 and PLAY_TYPE[i] == 'Pass':
            exp_pass_count += 1
            if GN_LS[i] >= 20:
                shot_count += 1
        elif GN_LS[i] >= 12 and PLAY_TYPE[i] == 'Run':
            exp_run_count += 1

        if i+1 == len(PLAY_NUM) or PLAY_NUM[i+1] - PLAY_NUM[i] > 1 or result == 'Fumble' or result == 'Complete, Fumble' or result == 'Rush, Fumble' or result == 'Sack, Fumble' or result == 'Scramble, Fumble' or result == 'Fumble, Def TD' or result == 'Complete, Fumble, Def TD' or result == 'Rush, Fumble, TD' or result == 'Sack, Fumble, Def TD' or result == 'Scramble, Fumble, Def TD' or result == 'Interception' or result == "interception, Def TD" or result == 'Sack, Safety' or result == 'Rush, Safety' or result == 'Complete, Safety' or result == 'Scramble, Safety':
            for x in range(negative_count):
                negative_results.append(result)
            for x in range(exp_pass_count):
                exp_pass_results.append(result)
            for x in range(exp_run_count):
                exp_run_results.append(result)
            for x in range(shot_count):
                shot_results.append(result)
            break




# print("\n\n\n\n******* EXPLOSIVE PLAY REPORT *******")

run_plays = data.loc[data['PLAY TYPE'] == 'Run']
run_plays = run_plays.loc[run_plays['GN/LS'] <= 110]
explosive_runs = run_plays.loc[run_plays['GN/LS'] >= 12]
explosive_runs = explosive_runs.reset_index()
del explosive_runs['index']
pass_plays = data.loc[data['PLAY TYPE'] == 'Pass']
pass_plays = pass_plays.loc[pass_plays['RESULT'] != 'Interception']
pass_plays = pass_plays.loc[pass_plays['RESULT'] != 'Interception, Def TD']
pass_plays = pass_plays.loc[pass_plays['GN/LS'] <= 110]
explosive_passes = pass_plays.loc[pass_plays['GN/LS'] >= 16]
explosive_passes = explosive_passes.reset_index()
del explosive_passes['index']
explosive_runs.insert(len(explosive_runs.columns), 'DRIVE RESULT', exp_run_results)
explosive_runs = explosive_runs.replace(1001, '--')
explosive_passes.insert(len(explosive_passes.columns), 'DRIVE RESULT', exp_pass_results)
explosive_passes = explosive_passes.replace(1001, '--')

# print("\n\n\n******* RUN PLAYS *******")
# print(explosive_runs)

# print("\n\n\n******* PASS PLAYS *******")
# print(explosive_passes)




# print("\n\n\n\n******* NEGATIVE PLAY REPORT *******\n\n\n")

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
negative_plays = negative_plays.replace(1001, '--')
# print(negative_plays)




# print("\n\n\n\n******* SHOT PLAY REPORT *******\n\n\n")

shot_plays = pass_plays.loc[pass_plays['GN/LS'] >= 20]
shot_plays.insert(len(shot_plays.columns), 'DRIVE RESULT', shot_results)
shot_plays = shot_plays.reset_index()
del shot_plays['index']
shot_plays = shot_plays.replace(1001, '--')
# print(shot_plays)




with open(output_file_name, 'a') as f:
    if len(safety_alignment_report) > 0:
        f.write('Safety Alignment Report,\n')
        safety_alignment_report.to_csv(f, index=False)
    else:
        f.write('No data for Safety Alignment Report,\n')

    if len(coverage_report) > 0:
        f.write('\nCoverage Report,\n')
        coverage_report.to_csv(f, index=False)
    else:
        f.write('\nNo data for Coverage Report,\n')

    if len(explosive_runs) > 0:
        f.write('\nExplosive Runs,\n')
        explosive_runs.to_csv(f, index=False)
    else:
        f.write('\nNo data for Explosive Runs,\n')

    if len(explosive_passes) > 0:
        f.write('\nExplosive Passes,\n')
        explosive_passes.to_csv(f, index=False)
    else:
        f.write('\nNo data for Explosive Passes,\n')

    if len(negative_plays) > 0:
        f.write('\nNegative Plays,\n')
        negative_plays.to_csv(f, index=False)
    else:
        f.write('\nNo data for Negative Plays,\n')

    if len(shot_plays) > 0:
        f.write('\nShot Plays,\n')
        shot_plays.to_csv(f, index=False)
    else:
        f.write('\nNo data for Shot Plays,\n')