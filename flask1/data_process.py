import os
import re
import shutil
import numpy
from pyxdameraulevenshtein import damerau_levenshtein_distance_seqs
import matplotlib.pyplot as plt

num_path = "./hazardlog_input"
files = os.listdir(num_path)
parameter_number = 5                                    #the number of required parameters
document_number = len(files)
nominalSequence = "tuwtdw"
plot_bar_x = []
plot_bar_y = []
legs_number = 0
arms_number = 0
maxforceratio_figure = []
average_collisionforce_ratio_figure = []
average_distance_figure = []
img_path_list = []
# empty the img folder before generate new images
img_path = "./static/img"
shutil.rmtree(img_path)
os.mkdir(img_path)

#a loop which can be used to process all documents to get needed data
for i in range(document_number):
    allparameters_original_list = []                        #A list which stores all needed parameters from the HazardLog
    allparameters_processed_list = []                       #A 2D list, every element in this list cotains the needed parameters for one simulation run
    all_actionsequence_list = []                            #all actionsequences extracted from one HazardLog
    different_actionsequence_list = []                      #differnt actionsequences from one HazardLog
    collisionforce_ratio_list = []
    max_force_list = []
    str_different_actionsequence_list = []
    distance_list = []
    #actionsequences_number_list = []
    distance_number_list = []
    flag = False
    if i <= 8:
        file_path_input = "./hazardlog_input/HazardLog_0%s.txt"%str(i+1) # HazardLog_TestCase_C_Random_01.txt
    else:
        file_path_input = "./hazardlog_input/HazardLog_%s.txt"%str(i+1) # HazardLog_TestCase_C_Random_10.txt
    file_path_output = "./hazardlog_output/Output_HazardLog%s.txt"%str(i+1)
    file_out = open(file_path_output,'w',encoding='UTF-8')
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
    length_allparameters = len(allparameters_original_list)
    row_allparameters_processed_list = length_allparameters//parameter_number
    allparameters_processed_list = numpy.array(allparameters_original_list).reshape(row_allparameters_processed_list,parameter_number)
    #print(allparameters_original_list)
    #print(allparameters_processed_list)
    
    for data in allparameters_original_list:
        if re.match('[{](.*?)[}]',data) != None:
            all_actionsequence_list.append(data)
    for data in all_actionsequence_list:
        if not data in different_actionsequence_list:
            different_actionsequence_list.append(data)
    length_differentactionsequences = len(different_actionsequence_list)
    #calculate percentage of legs and arms
    for data in allparameters_original_list:
        if data == "legs":
            legs_number += 1
        if data == "arms":
            arms_number += 1
    #tansfer the action sequence to string
    for data in different_actionsequence_list:
        data = re.sub('transition','t',data)
        data = re.sub('pickUpPart','u',data)
        data = re.sub('wait','w',data)
        data = re.sub('putDownPart','d',data)
        data = re.sub('{|}|,','',data)
        str_different_actionsequence_list.append(data)
    #print(str_different_actionsequence_list) 
    plot_bar_x.append(str_different_actionsequence_list)        #x axis for bar plot
    distance_list = damerau_levenshtein_distance_seqs(nominalSequence,str_different_actionsequence_list)
    #print(distance_list)

    # build a Index_list list to store the index info for allparameters_processed_list
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

    n = 0
    while n < length_differentactionsequences:
        m = 0
        max_force = 0.0
        actionsequences_number = 0
        #print('The actionsequence is:',different_actionsequence_list[n])
        #print('The number of simulation runs:')
        actionsequence = different_actionsequence_list[n]
        order_actionsequence = str(n + 1)
        file_out.write('\nThe actionsequence ')
        file_out.write(order_actionsequence)
        file_out.write(' is: ')
        file_out.write(actionsequence)
        file_out.write('\nThe relevant simulation run and affected body part: ')
        while m < row_allparameters_processed_list:
            if Index_list[n][m] == 1:
                #print(allparameters_processed_list[m][0])
                simulation_run = allparameters_processed_list[m][0]
                affected_bodypart = allparameters_processed_list[m][1]
                file_out.write(simulation_run)
                file_out.write(' and ')
                file_out.write(affected_bodypart)
                file_out.write(',')
                actionsequences_number += 1
                force = float(allparameters_processed_list[m][3])
                limit_force = float (allparameters_processed_list[m][2])
                if force > max_force:
                    max_force = force                                        #maximal force in each actionsequence
                    collisionforce_ratio = max_force / limit_force            #maximal force ratio in each actionsequence
                    collisionforce_ratio_list.append(collisionforce_ratio)
                    max_force_list.append(max_force)
            m += 1

        #print('The maximal force is:',max_force)
        distance = str(distance_list[n])
        distance_number_list.append(distance_list[n])                  #y axis for bar plot
        file_out.write('\nThe distance with nominalSequence is: ')
        file_out.write(distance)
        max_force_str=str(max_force)
        collisionforce_ratio_str = str(collisionforce_ratio)
        file_out.write('\nThe maximal collision force is: ')
        file_out.write(max_force_str)
        file_out.write('N')
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
    
#draw a bar figure for each HazardLog
for i in range(document_number):
    img_path = 'img/Distance Bar Figure%s.png'%str(i+1)
    img_path_list.append(img_path)
    plt.figure(figsize=(16,8))
    plt.bar(plot_bar_x[i],plot_bar_y[i],color = '#078079')
    plt.xticks(rotation=-60)
    plt.yticks(plot_bar_y[i])
    plt.xlabel('actionsequences')
    plt.ylabel('Distance')
    plt.title('Distance Summary of HazardLog%s'%str(i+1))
    plt.savefig('./static/img/Distance Bar Figure%s'%str(i+1),dpi = 100)
    plt.close()
print(img_path_list)
#draw a pie figure for affected_bodypart
labels = ['arms','legs']
explode = (0,0.1)
x = [arms_number,legs_number]
colors = ['#078079','darkorange']
plt.pie(x,labels=labels,colors=colors, autopct = '%1.1f%%',explode = explode,shadow = True)
plt.axis('equal')
plt.title('Affected Bodypart of all Hazardlogs')
plt.savefig('./static/img/Affected Bodypart of all Hazardlogs',dpi = 100)
plt.close()

#draw a combination figure for maxmal force ratio and average force ratio
#x = [range(1,document_number)]
plt.xlabel('Number of HazardLog')
plt.ylabel('Force Ratio(MaxForce/LimitForce)')
plt.title('Maxmal force ratio and average force ratio')
x = numpy.arange(1,document_number+1)
plt.bar(x,maxforceratio_figure,color = '#078079',label='maxmal force ratio')
plt.plot(x,average_collisionforce_ratio_figure,color = 'darkorange',marker='*',label = 'average force ratio')
plt.xticks(x)
plt.legend()
plt.savefig('./static/img/Maxmal force ratio and average force ratio',dpi = 100)
plt.close()
#plt.show()

#draw a bar figure for average distance
plt.xlabel('Number of HazardLog')
plt.ylabel('Average Distance')
plt.title('Average Distance Distribution')
x = numpy.arange(1,document_number+1)
plt.bar(x,average_distance_figure,color = '#078079')
plt.xticks(x)
plt.savefig('./static/img/Average Distance',dpi = 100)
plt.close()

print("process finish")
