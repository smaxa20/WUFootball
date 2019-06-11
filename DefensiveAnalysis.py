import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)

# Change the file name of the Excel sheet under 'file_name'
file_name = "GeorgeFox2018DefensiveBreakdown.xlsx"
# The Excel file should be placed in a file called 'Data' the directory directly up the tree from this file
file = "../Data/" + file_name
# Make sure to specify the correct sheet name
sheet = "Fox Scout Data"

data = pd.read_excel(file, sheet, index_col = None, header = 0, na_values = ' ')
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

print("\n\n\n\n******* Safety Alignment Report *******")

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
print(safety_alignment_report)




print("\n\n\n\n******* Coverage Report *******")

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
print(coverage_report)