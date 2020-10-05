#!/usr/bin/env python
# coding: utf-8

# In[14]:


import csv


# In[15]:


#In the Data Dictionary, the email is stored as the key, and the [message, date] is stored as the value
dataDict = {}
countDict = {} #{date: {email: count}}


# In[16]:


def readCSV():
    with open('lvf_ballot_chase_01_messages.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        next(csv_reader)

        #Looping through the CSV, storing messages as {email: [(message, date), (message, date)]}
        #Looping through the CSV, storing messages as {date: [(email, message), (email, message)]}
        for row in csv_reader:
            currDate = parseDate(row[0])
            if (row[7] != ""):
                #row7 = email, row3 = message
                currEntry = (row[7], row[3])
                if currDate in dataDict:
                    dataDict[currDate].append(currEntry)
                else:
                    dataDict[currDate] = [currEntry]   


# In[17]:


print(dataDict)


# In[12]:


#Converting '2020-09-25 20:33:49.979033Z' to '09-25'
def parseDate(date):
    return (date[5:11])


# In[21]:


#Fetching the number of emails per user per date
def count():
    for date in dataDict:
        messageList = dataDict[date]
        countDict[date] = {}
        for message in messageList:
            email = message[0]
            if email in countDict[date]:
                countDict[date][email] += 1
            else:
                countDict[date][email] = 1


# In[23]:


def writeToCSV():
    with open('output.csv', 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, countDict.keys())
        w.writeheader()
        w.writerow(countDict)


# In[ ]:


def mainFunc():
    readCSV()
    count()
    writeToCSV()

