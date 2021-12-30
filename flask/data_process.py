import os
import re
import shutil
import numpy
from pyxdameraulevenshtein import damerau_levenshtein_distance_seqs
import matplotlib.pyplot as plt

'''set flags to get different output report'''
ActionSequence_flag = True
Simulationrun_flag = False
AffectedBodyPart_flag = True
Distance_flag = True
MaxForce_flag = True
CollisionForceRatio_flag = True 

'''deal with muti-input hazardlogs, get the number of input hazardlogs'''
num_path = "./hazardlog_input"
files = os.listdir(num_path)
document_number = len(files)


nominalSequence = "tuwtdw"
parameter_number = 5

'''figure generation parameters'''
plot_bar_x = []
plot_bar_y = []
legs_number = 0
arms_number = 0
maxforceratio_figure = []
average_collisionforce_ratio_figure = []
average_distance_figure = []

'''empty the img folder before generate new images'''
img_path = "./static/img"
shutil.rmtree(img_path)
os.mkdir(img_path)


inputhazardlog_folderpath = "./hazardlog_input"
screenshots_folderpath = "./static/Screenshots"
screenshots_path =[]

'''a function which can generate a list to get all parameters'''
def generation_paralist (file_path_input):

    allparameters_original_list = []                        #A list which stores all needed parameters from the HazardLog
    allparameters_processed_list = []                       #A 2D list, every element in this list cotains the needed parameters of a hazard
    flag = False
    parameter_number = 5
    with open(file_path_input,'r') as file: 
        contents = file.readlines()
        for lines in contents:
            if lines.startswith("-----------------"):
                flag = True
                num = 0
            if flag:
                if "Simulation run" in lines:
                    a = lines
                    a = re.sub(' Simulation run: |\n','',a)
                    allparameters_original_list.append(a)
                    num += 1
                if "Affected Body Part" in lines:
                    b = lines
                    b = re.sub(' Affected Body Part: |\n','',b)
                    allparameters_original_list.append(b)
                    num += 1
                if "Collision Force Limit:" in lines:
                    c = lines
                    c = re.sub(' Collision Force Limit: |N|\n','',c)
                    CollisionForceLimit = c
                    allparameters_original_list.append(c)
                    num += 1
                if "Collision Force:" in lines:
                    d = lines
                    d = re.sub(' Collision Force: |N|\n','',d)
                    allparameters_original_list.append(d)
                    num += 1

                if "In Action Sequence:" in lines:
                    e = lines
                    e = re.sub(' In Action Sequence: |\n','',e)
                    allparameters_original_list.append(e)
                    num += 1
                    if num != parameter_number:
                        del allparameters_original_list[-num:]

    return allparameters_original_list
'''a function to get the subfile path under a folder'''
def getsubfilepath(filepath):
    targetfile_path_list = []
    filename = os.listdir(filepath)
    for data in filename:
        targetfile_path = filepath + "/" + data
        targetfile_path_list.append(targetfile_path)
    return targetfile_path_list
'''a function which used to generate final visual data for flask application'''
def generation_vsdata(filepath):
    allparameters_original_list = []                        #A list which stores all needed parameters from the HazardLog
    allparameters_processed_list = []                       #A 2D list, every element in this list cotains the needed parameters of a hazard
    num = 0
    with open(filepath,'r') as file:
        contents = file.readlines()
        for lines in contents:
            if "The actionsequence" in lines:
                a = lines
                a = re.sub('The actionsequence', 'Action Sequence', a)
                a = re.sub(' is', '', a)
                allparameters_original_list.append(a)
            if "The relevant simulation run" in lines:
                b = lines
                b = re.sub('The relevant simulation run', 'Simulation Run', b)
                allparameters_original_list.append(b)
            if "The affected body part" in lines:
                c = lines
                c = re.sub('The affected body part', 'Affected Body Part', c)
                allparameters_original_list.append(c)
            if "The distance with nominalSequence" in lines:
                d = lines
                d = re.sub('The distance with nominalSequence is', 'Distance', d)
                allparameters_original_list.append(d)
            if "The maximal collision force is" in lines:
                e = lines
                e = re.findall(r"\d+\.?\d*",e)
                force = float(e[0])
                e = 'Max. Collision Force: ' + str(format(force,'.1f')) + ' N\n'
                allparameters_original_list.append(e)
            if "The collision force ratio is" in lines:
                f = lines
                f = re.findall(r"\d+\.?\d*", f)
                ratio = float(f[0])
                f = "Coll. Force Ratio: " + str(format(ratio, '.1f')) + '\n'
                allparameters_original_list.append(f)
            if "-------------------" in lines:
                num += 1
    length = len(allparameters_original_list)
    row = length // num
    allparameters_processed_list = numpy.array(allparameters_original_list).reshape(num,row)
    return allparameters_processed_list


scr_dic = []
allparameters_original_list = []                        #A list which stores all needed parameters from the HazardLog
allparameters_processed_list = []                       #A 2D list, every element in this list cotains the needed parameters for one hazard
all_actionsequence_list = []                            #all actionsequences extracted from one HazardLog
different_actionsequence_list = []                      #differnt actionsequences from one HazardLog
collisionforce_ratio_list = []
max_force_list = []
str_different_actionsequence_list = []
distance_list = []
distance_number_list = []

inputhazardlog_path = getsubfilepath(inputhazardlog_folderpath)
file_path_input = inputhazardlog_path[0]
file_path_output = "./hazardlog_output/Output_HazardLog.txt"
file_out = open(file_path_output,'w',encoding='UTF-8')

'''transfer original list to 5*n list, 5 is the parameter number, n is the number of hazards in input file'''
allparameters_original_list = generation_paralist (file_path_input)
length_allparameters = len(allparameters_original_list)
row_allparameters_processed_list = length_allparameters//parameter_number
allparameters_processed_list = numpy.array(allparameters_original_list).reshape(row_allparameters_processed_list,parameter_number)

'''extract all different action sequences, and store them in different_actionsequence_list'''
for data in allparameters_original_list:
    if re.match('[{](.*?)[}]',data) != None:
        all_actionsequence_list.append(data)
for data in all_actionsequence_list:
    if not data in different_actionsequence_list:
        different_actionsequence_list.append(data)
length_differentactionsequences = len(different_actionsequence_list)

'''tansfer the action sequence to string'''
for data in different_actionsequence_list:
    data = re.sub('transition','t',data)
    data = re.sub('pickUpPart','u',data)
    data = re.sub('wait','w',data)
    data = re.sub('putDownPart','d',data)
    data = re.sub('{|}|,','',data)
    str_different_actionsequence_list.append(data)

plot_bar_x.append(str_different_actionsequence_list)        #x axis for bar plot
distance_list = damerau_levenshtein_distance_seqs(nominalSequence,str_different_actionsequence_list)

'''build a Index_list list to store the index info for allparameters_processed_list'''
row_index_list = row_allparameters_processed_list + 1
columns_index_list = length_differentactionsequences + 1
Index_list = numpy.zeros([columns_index_list,row_index_list])
n = 0
while n< length_differentactionsequences:
    m=0
    while m < row_allparameters_processed_list:
        if allparameters_processed_list[m][4] == different_actionsequence_list[n]:
            Index_list[n][m] = 1
        m += 1
    n += 1

'''calculate percentage of legs and arms'''
if AffectedBodyPart_flag:
    for data in allparameters_original_list:
        if data == "legs":
            legs_number += 1
        if data == "arms":
            arms_number += 1

'''generate output hazardlog'''
n = 0
while n < length_differentactionsequences:
    m = 0
    max_force = 0.0
    actionsequences_number = 0
    actionsequence = different_actionsequence_list[n]
    order_actionsequence = str(n + 1)
    '''write hazard actionsequence in output'''
    if ActionSequence_flag:
        file_out.write('\nThe actionsequence ')
        file_out.write(order_actionsequence)
        file_out.write(' is: ')
        file_out.write(actionsequence)
    while m < row_allparameters_processed_list:
        if Index_list[n][m] == 1:
            if Simulationrun_flag:
                simulation_run = allparameters_processed_list[m][0]
                file_out.write('\nThe relevant simulation run: ')
                file_out.write(simulation_run)
            if AffectedBodyPart_flag:
                affected_bodypart = allparameters_processed_list[m][1]
                file_out.write('\nThe affected body part: ')
                file_out.write(affected_bodypart)
            actionsequences_number += 1
            '''calculate max force and force ratio'''
            force = float(allparameters_processed_list[m][3])
            limit_force = float (allparameters_processed_list[m][2])
            if force > max_force:
                max_force = force                                        #maximal force in each actionsequence
                collisionforce_ratio = max_force / limit_force            #maximal force ratio in each actionsequence
                '''two list for figure generation'''
                collisionforce_ratio_list.append(collisionforce_ratio)
                max_force_list.append(max_force)
        m += 1

    #print('The maximal force is:',max_force)
    distance = str(distance_list[n])
    distance_number_list.append(distance_list[n])                  #y axis for bar plot
    if Distance_flag:
        file_out.write('\nThe distance with nominalSequence is: ')
        file_out.write(distance)

    if MaxForce_flag:
        max_force_str=str(max_force)
        file_out.write('\nThe maximal collision force is: ')
        file_out.write(max_force_str)
        file_out.write('N')
    if CollisionForceRatio_flag:
        collisionforce_ratio_str = str(collisionforce_ratio)
        file_out.write('\nThe collision force ratio is: ')
        file_out.write(collisionforce_ratio_str)
    file_out.write('\n-------------------')
    n += 1
plot_bar_y.append(distance_number_list)

#data for draw a bar figure
maxforceratio = (max(max_force_list)) / limit_force
maxforceratio_figure.append(maxforceratio)
average_collisionforce_ratio_figure.append(numpy.mean(collisionforce_ratio_list))
average_distance_figure.append(numpy.mean(distance_list))

#Summary
totalnumber_actionsequense = str(length_differentactionsequences)
average_collisionforce_ratio = str(numpy.mean(collisionforce_ratio_list))
max_force_total = str(max(max_force_list))
average_distance = str(numpy.mean(distance_list))
file_out.write('\nSummary: ')
file_out.write('\nThe total number of all different actionsequences: ')
file_out.write(totalnumber_actionsequense)
file_out.write('\nThe average of all collision force ratio: ')
file_out.write(average_collisionforce_ratio)
file_out.write('\nThe maximal collision force of all actionsequence: ')
file_out.write(max_force_total)
file_out.write('N')
file_out.write('\nThe average distance for all actionsequences is: ')
file_out.write(average_distance)
file_out.close()

'''generate a dictionary for final visualization, the dictionary contains the screenshots img path and corresponding
 hazarad information'''
flask_data = generation_vsdata(file_path_output)
m = n = 0
flask_info =[]
para_num = len(flask_data[0])
sim_num = len(flask_data)
for m in range(sim_num):
    a = ''
    for n in range(para_num):
        a += flask_data[m][n]
        n += 1
    m += 1
    flask_info.append(a)
print(flask_info)
filelist = os.listdir(screenshots_folderpath)
filelist.sort()
for file in filelist:
    screenshotspath = 'Screenshots/'+file
    screenshots_path.append(screenshotspath)
num = len(flask_info)
i = 0
for i in range(num):
    dic = {'screenshotspath':screenshots_path[i],'hazardinfo':flask_info[i]}
    scr_dic.append(dic)
    i += 1


#draw a bar figure for each HazardLog
if Distance_flag:
    img_path = 'img/Distance Bar Figure.png'
    plt.figure(figsize=(16,8))
    plt.bar(plot_bar_x[0],plot_bar_y[0],color = '#078079')
    plt.xticks(rotation=-60)
    plt.yticks(plot_bar_y[0])
    plt.xlabel('actionsequences')
    plt.ylabel('Distance')
    plt.title('Distance Summary of HazardLog')
    plt.savefig('./static/img/Distance Bar Figure',dpi = 100)
    plt.close()


#draw a pie figure for affected_bodypart
if AffectedBodyPart_flag:
    labels = ['arms','legs']
    explode = (0,0.1)
    x = [arms_number,legs_number]
    colors = ['#078079','darkorange']
    plt.pie(x,labels=labels,colors=colors, autopct = '%1.1f%%',explode = explode,shadow = True)
    plt.axis('equal')
    plt.title('Affected Bodypart of all Hazardlogs')
    plt.savefig('./static/img/Affected Bodypart of all Hazardlogs',dpi = 100)
    plt.close()


print("process finish")
