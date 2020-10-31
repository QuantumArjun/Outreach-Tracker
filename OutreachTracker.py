#!/usr/bin/env python
# coding: utf-8

import csv

#Fields to modify
inputFile = 'lvf_early_vote_02_messages.csv' #Change to name of input file
outputFile = 'output.csv'
beginningTime = "17"
endTime = "20"

#In the Data Dictionary, the email is stored as the key, and the [message, date] is stored as the value
dataDict = {}
countDict = {} #{date: {email: count}}
finalOutput = []


# In[48]:


def readCSV():
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        next(csv_reader)

        #Looping through the CSV, storing messages as {email: [(message, date), (message, date)]}
        #Looping through the CSV, storing messages as {date: [(email, message), (email, message)]}
        for row in csv_reader:
            currDate = parseDate(row[0])
            currTime = int(getTime(row[0]))
            if currTime >= int(beginningTime) and currTime <= int(endTime):
                if (row[7] != ""):
                    #row7 = email, row3 = message, row[4] = first name, row[5] = last name
                    currEntry = (row[7], row[4], row[5])
                    if currDate in dataDict:
                        dataDict[currDate].append(currEntry)
                    else:
                        dataDict[currDate] = [currEntry]   

#Converting '2020-09-25 20:33:49.979033Z' to '09-25'
def parseDate(date):
    return (date[5:10])

def getTime(date):
    return date[11:13]

#Fetching the number of emails per user per date
def count():
    for date in dataDict:
        currEntry = dataDict[date]
        countDict[date] = {}
        for field in currEntry:
            email = field[0]
            if email in countDict[date]:
                countDict[date][email]["count"] += 1
            else:
                countDict[date][email] = {"count": 1, "firstName": field[1], "lastName": field[2]}

def createOutput():
    for date in countDict:
        for entry in countDict[date]:
            finalOutput.append([date, entry, countDict[date][entry]["firstName"], countDict[date][entry]["lastName"], countDict[date][entry]["count"]])

fields = ['Date', 'E-mail', "First Name", "Last Name", 'Number of Messages'] 

def writeToCSV():
    with open(outputFile, 'w') as csvfile:  # Just use 'w' mode in 3.x
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  

        # writing the fields  
        csvwriter.writerow(fields)  

        # writing the data rows  
        csvwriter.writerows(finalOutput)

def mainFunc():
    readCSV()
    count()
    createOutput()
    writeToCSV()

mainFunc()
