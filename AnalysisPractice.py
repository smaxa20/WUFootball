import numpy as np
import pandas as pd

# Change the file name of the Excel sheet under 'file_name'
file_name = "UCFDataSample.xlsx"
# The Excel file should be placed in the directory directly up the tree from this file
file = "../" + file_name
# Make sure to specify the correct sheet name
sheet = "UCF Data Sample"

data = pd.read_excel(file, sheet, index_col = None, header = 0, na_values = ['NA'])
data = data.fillna(0)

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

plays_in_each_formation = []
i = 0
for form in formations:
    plays_in_each_formation.append(data.loc[data['OFF FORM'] == form])
    print(plays_in_each_formation[i])
    print('\n')

    if len(plays_in_each_formation[i]) == 1:
        string = np.array([len(plays_in_each_formation[i]), "total play run from the", form, "formation"])
    else:
        string = np.array([len(plays_in_each_formation[i]), "total plays run from the", form, "formation"])
    print(' '.join(string))

    run_count = 0
    run_count += plays_in_each_formation[i].loc[plays_in_each_formation[i]['PLAY TYPE'] == 'Run'].size / 9
    string = np.array([run_count, "run plays"])
    print(' '.join(string))

    pass_count = 0
    pass_count += plays_in_each_formation[i].loc[plays_in_each_formation[i]['PLAY TYPE'] == 'Pass'].size / 9
    string = np.array([pass_count, "pass plays"])
    print(' '.join(string))

    yards = plays_in_each_formation[i].loc[:,'GN/LS']
    yards = np.array(yards)

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

    print('\n \n \n \n')
    i += 1


print("******* EACH TIME EACH PLAY WAS RUN *******\n\n")

ordered_formations = []
i = 0
for play in plays:
    ordered_formations.append(data.loc[data['OFF PLAY'] == play])
    formations_for_this_play = ordered_formations[i].loc[:'OFF FORM']
    print(formations_for_this_play)
    print('\n')
    if len(formations_for_this_play) == 1:
        string = np.array([play, "was run 1 time"])
    else:
        string = np.array([play, "was run", len(formations_for_this_play), "times"])
    print(' '.join(string))

    yards = formations_for_this_play.loc[:,'GN/LS']
    yards = np.array(yards)

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

    print('\n \n \n \n')
    i += 1



print("******* ALL FIRST DOWN CONVERSIONS *******")

if len(data) != 0:
    string = np.array(["Conversion Rate:", float(len(got_first_down)) / float(len(data))])
else:
    string = np.array(["Conversion Rate: 0.0"])
print(' '.join(string))

run_count = 0
run_conversion_count = 0
run_count += data.loc[data['PLAY TYPE'] == 'Run'].size / 9
run_conversion_count += got_first_down.loc[got_first_down['PLAY TYPE'] == 'Run'].size / 9
if run_count != 0:
    string = np.array(["Rushing Conversion Rate:", float(run_conversion_count) / float(run_count)])
else:
    string = np.array(["Rushing Conversion Rate: 0.0"])
print(' '.join(string))

pass_count = 0
pass_conversion_count = 0
pass_count += data.loc[data['PLAY TYPE'] == 'Pass'].size / 9
pass_conversion_count += got_first_down.loc[got_first_down['PLAY TYPE'] == 'Pass'].size / 9
if pass_count != 0:
    string = np.array(["Passing Conversion Rate:", float(pass_conversion_count) / float(pass_count)])
else:
    string = np.array(["Passing Conversion Rate: 0.0"])
print(' '.join(string))
print('\n')

count = 0
count += len(got_first_down)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += got_first_down.loc[got_first_down['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += got_first_down.loc[got_first_down['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')


print(got_first_down)



print("\n\n\n\n******* FIRST DOWN *******")

if len(first_down) != 0:
    string = np.array(["Conversion Rate:", float(len(first_down_conversion)) / float(len(first_down))])
else:
    string = np.array(["Conversion Rate: 0.0"])
print(' '.join(string))

run_count = 0
run_conversion_count = 0
run_count += first_down.loc[first_down['PLAY TYPE'] == 'Run'].size / 9
run_conversion_count += first_down_conversion.loc[first_down_conversion['PLAY TYPE'] == 'Run'].size / 9
if run_count != 0:
    string = np.array(["Rushing Conversion Rate:", float(run_conversion_count) / float(run_count)])
else:
    string = np.array(["Rushing Conversion Rate: 0.0"])
print(' '.join(string))

pass_count = 0
pass_conversion_count = 0
pass_count += first_down.loc[first_down['PLAY TYPE'] == 'Pass'].size / 9
pass_conversion_count += first_down_conversion.loc[first_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
if pass_count != 0:
    string = np.array(["Passing Conversion Rate:", float(pass_conversion_count) / float(pass_count)])
else:
    string = np.array(["Passing Conversion Rate: 0.0"])
print(' '.join(string))
print('\n\n')


print("TOTAL\n")

count = 0
count += len(first_down)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += first_down.loc[first_down['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += first_down.loc[first_down['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(first_down) > 0:
    print(first_down)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(first_down.loc[first_down['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(first_down.loc[first_down['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\nGAINED FIRST DOWN\n")

count = 0
count += len(first_down_conversion)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += first_down_conversion.loc[first_down_conversion['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += first_down_conversion.loc[first_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(first_down_conversion) > 0:
    print(first_down_conversion)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(first_down_conversion.loc[first_down_conversion['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(first_down_conversion.loc[first_down_conversion['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\nSTOPPED SHORT\n")

count = 0
count += len(first_down_stop)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += first_down_stop.loc[first_down_stop['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += first_down_stop.loc[first_down_stop['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(first_down_stop) > 0:
    print(first_down_stop)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(first_down_stop.loc[first_down_stop['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(first_down_stop.loc[first_down_stop['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")




print("\n\n\n\n******* SECOND DOWN *******")

if len(second_down) != 0:
    string = np.array(["Conversion Rate:", float(len(second_down_conversion)) / float(len(second_down))])
else:
    string = np.array(["Conversion Rate: 0.0"])
print(' '.join(string))

run_count = 0
run_conversion_count = 0
run_count += second_down.loc[second_down['PLAY TYPE'] == 'Run'].size / 9
run_conversion_count += second_down_conversion.loc[second_down_conversion['PLAY TYPE'] == 'Run'].size / 9
if run_count != 0:
    string = np.array(["Rushing Conversion Rate:", float(run_conversion_count) / float(run_count)])
else:
    string = np.array(["Rushing Conversion Rate: 0.0"])
print(' '.join(string))

pass_count = 0
pass_conversion_count = 0
pass_count += second_down.loc[second_down['PLAY TYPE'] == 'Pass'].size / 9
pass_conversion_count += second_down_conversion.loc[second_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
if pass_count != 0:
    string = np.array(["Passing Conversion Rate:", float(pass_conversion_count) / float(pass_count)])
else:
    string = np.array(["Passing Conversion Rate: 0.0"])
print(' '.join(string))
print('\n\n')


print("TOTAL\n")

count = 0
count += len(second_down)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += second_down.loc[second_down['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += second_down.loc[second_down['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(second_down) > 0:
    print(second_down)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(second_down.loc[second_down['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(second_down.loc[second_down['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\nGAINED FIRST DOWN\n")

count = 0
count += len(second_down_conversion)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += second_down_conversion.loc[second_down_conversion['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += second_down_conversion.loc[second_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(second_down_conversion) > 0:
    print(second_down_conversion)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(second_down_conversion.loc[second_down_conversion['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(second_down_conversion.loc[second_down_conversion['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No data")


print("\n\n\nSTOPPED SHORT\n")

count = 0
count += len(second_down_stop)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += second_down_stop.loc[second_down_stop['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += second_down_stop.loc[second_down_stop['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(second_down_stop) > 0:
    print(second_down_stop)
    print("\nNumber of times that each formation was used:")
    container = []
    i = 0
    for form in formations:
        container.append(second_down_stop.loc[second_down_stop['OFF FORM'] == form])
        form_count = container[i].loc[:'OFF FORM']
        if len(form_count) != 0:
            string = np.array([form, ": ", len(form_count)])
            print(''.join(string))
        i += 1
    print("\nNumber of times that each play was used:")
    container = []
    i = 0
    for play in plays:
        container.append(second_down_stop.loc[second_down_stop['OFF PLAY'] == play])
        play_count = container[i].loc[:'OFF PLAY']
        if len(play_count) != 0:
            string = np.array([play, ": ", len(play_count)])
            print(''.join(string))
        i += 1
else:
    print("No Data")




print("\n\n\n\n******* THIRD DOWN *******")

if len(third_down) != 0:
    string = np.array(["Conversion Rate:", float(len(third_down_conversion)) / float(len(third_down))])
else:
    string = np.array(["Conversion Rate: 0.0"])
print(' '.join(string))

run_count = 0
run_conversion_count = 0
run_count += third_down.loc[third_down['PLAY TYPE'] == 'Run'].size / 9
run_conversion_count += third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Run'].size / 9
if run_count != 0:
    string = np.array(["Rushing Conversion Rate:", float(run_conversion_count) / float(run_count)])
else:
    string = np.array(["Rushing Conversion Rate: 0.0"])
print(' '.join(string))

pass_count = 0
pass_conversion_count = 0
pass_count += third_down.loc[third_down['PLAY TYPE'] == 'Pass'].size / 9
pass_conversion_count += third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
if pass_count != 0:
    string = np.array(["Passing Conversion Rate:", float(pass_conversion_count) / float(pass_count)])
else:
    string = np.array(["Passing Conversion Rate: 0.0"])
print(' '.join(string))
print('\n\n')


print("TOTAL\n")

count = 0
count += len(third_down)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += third_down.loc[third_down['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += third_down.loc[third_down['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(third_down) > 0:
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


print("\n\n\nGAINED FIRST DOWN\n")

count = 0
count += len(third_down_conversion)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += third_down_conversion.loc[third_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(third_down_conversion) > 0:
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


print("\n\n\nSTOPPED SHORT\n")

count = 0
count += len(third_down_stop)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += third_down_stop.loc[third_down_stop['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += third_down_stop.loc[third_down_stop['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(third_down_stop) > 0:
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




print("\n\n\n\n******* FOURTH DOWN *******")

if len(fourth_down) != 0:
    string = np.array(["Conversion Rate:", float(len(fourth_down_conversion)) / float(len(fourth_down))])
else:
    string = np.array(["Conversion Rate: 0.0"])
print(' '.join(string))

run_count = 0
run_conversion_count = 0
run_count += fourth_down.loc[fourth_down['PLAY TYPE'] == 'Run'].size / 9
run_conversion_count += fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Run'].size / 9
if run_count != 0:
    string = np.array(["Rushing Conversion Rate:", float(run_conversion_count) / float(run_count)])
else:
    string = np.array(["Rushing Conversion Rate: 0.0"])
print(' '.join(string))

pass_count = 0
pass_conversion_count = 0
pass_count += fourth_down.loc[fourth_down['PLAY TYPE'] == 'Pass'].size / 9
pass_conversion_count += fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
if pass_count != 0:
    string = np.array(["Passing Conversion Rate:", float(pass_conversion_count) / float(pass_count)])
else:
    string = np.array(["Passing Conversion Rate: 0.0"])
print(' '.join(string))
print('\n\n')


print("TOTAL\n")

count = 0
count += len(fourth_down)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += fourth_down.loc[fourth_down['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += fourth_down.loc[fourth_down['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(fourth_down) > 0:
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


print("\n\n\nGAINED FIRST DOWN\n")

count = 0
count += len(fourth_down_conversion)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += fourth_down_conversion.loc[fourth_down_conversion['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(fourth_down_conversion) > 0:
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


print("\n\n\nSTOPPED SHORT\n")

count = 0
count += len(fourth_down_stop)
string = np.array(["Total plays:", count])
print(' '.join(string))

run_count = 0
run_count += fourth_down_stop.loc[fourth_down_stop['PLAY TYPE'] == 'Run'].size / 9
string = np.array(["Run plays:", run_count])
print(' '.join(string))

pass_count = 0
pass_count += fourth_down_stop.loc[fourth_down_stop['PLAY TYPE'] == 'Pass'].size / 9
string = np.array(["Pass plays:", pass_count])
print(' '.join(string))
print('\n')

if len(fourth_down_stop) > 0:
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