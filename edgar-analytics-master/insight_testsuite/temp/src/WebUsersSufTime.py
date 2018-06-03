
# coding: utf-8

# In[495]:


def usersresults(IP_USERS, target):
    IP_USERS_search = np.core.defchararray.find(IP_USERS,target)
    IP_USERS_search_pos = np.where(IP_USERS_search == 0)
    return(IP_USERS_search_pos)

def timeformat(time1d,time1h):
    import datetime, time
    time1a = list(map(int,time1d.split('-')))
    time1b = list(map(int,time1h.split(':')))
    t1 = datetime.datetime(time1a[0], time1a[1], time1a[2],time1b[0], time1b[1],time1b[2])
    return(t1)

import csv
import numpy as np
import datetime,time
import os

cwd = os.getcwd()
# cwd = '/Users/qinli/Documents/GitHub/edgar-analytics-master'
if os.path.exists(cwd+'/src') == False :
    print('Work directory is incorrect, it must be changed to edgar-analytics-master')
    cwd = input("Work directory : ")
    os.chdir(cwd)

period_file = open('./input/inactivity_period.txt','r')
period = int(period_file.read().splitlines()[0])
period_file.close()

Fout_zip = open('./output/sessionization.txt','w')

with open('./input/log.csv', newline='') as csvfile:         
    csvdata = csv.reader(csvfile,delimiter=' ', quotechar='|')
    INFO = [] 
    IP = []
    T1 = np.zeros((1,3),int)

    for index, row in enumerate(csvdata):
        if index == 0 :        # skip first line
            continue
        index = index - 1  
        info = row[0].split(',')              # info : ip, date, time, zone, cik, accession, extention, code,
                                              #        size, idx, norefer, noaagent, find, crawler, browser
        if index == 0 :
            TIME0 = timeformat(info[1],info[2])      # Initial time
            TT1 = 0
        TIME1 = timeformat(info[1],info[2])
        TIMEPASS = (TIME1-TIME0).total_seconds()
        
        
        IP_ONLY = [x[0] for x in INFO]
        if len(INFO) == 0 :
            pos = []
        else :
            pos = (usersresults(IP_ONLY,info[0]))[0]
        if len(INFO) == 0  or pos.size == 0 :
            T2 = np.copy(T1)
            T2[:] = T1[:]
            T2[0,0] = TIMEPASS        
            T2[0,1] = TIMEPASS
            T2[0,2] = TIMEPASS
            INFO.append([info[0],T2,info[1],info[2],info[1],info[2],1,1])  #[IP, [starttime endtime currenttim], \ 
                                                                             #startdate,time,enddate,time,duration, \
                                                                             # documents
        else :
            if TIMEPASS - INFO[pos[0]][1][0,1] <= period :  
                INFO[pos[0]][1][0,1] = TIMEPASS
                INFO[pos[0]][4] = info[1]
                INFO[pos[0]][5] = info[2]   
                INFO[pos[0]][7] += 1
                INFO[pos[0]][6] = 1 + INFO[pos[0]][1][0,1] - INFO[pos[0]][1][0,0]
#-----------------------Delete response time more than 2sec users
        if TIMEPASS - TT1 > 0 :
            TT1 = TIMEPASS
            for x in INFO :
                x[1][0,2] = TIMEPASS - x[1][0,1]
            response = [x[1][0,2] for x in INFO]
            response_greater_than_2 = [t for t,x in enumerate(response) if x > period]
            for x in response_greater_than_2:
                output = INFO[x][0] + ',' + INFO[x][2] + ' ' + INFO[x][3] + ',' +                          INFO[x][4] + ' ' + INFO[x][5] + ',' + str(INFO[x][6]) + ','                         + str(INFO[x][7])
                Fout_zip.write(output)
                Fout_zip.write('\n')
            for x in response_greater_than_2 : 
                INFO.remove(INFO[x])
    for x,y in enumerate(INFO) :
        output = INFO[x][0] + ',' + INFO[x][2] + ' ' + INFO[x][3] + ',' +                  INFO[x][4] + ' ' + INFO[x][5] + ',' + str(INFO[x][6]) + ','                 + str(INFO[x][7])
        Fout_zip.write(output)
        Fout_zip.write('\n')
Fout_zip.close()




