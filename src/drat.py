import sqlite3
import scipy
import numpy as np
import matplotlib.pyplot as plt
import requests
import collections
import pandas as pd
import lxml
import urllib.request
import urllib
import builtins
import request
from lxml import html
from requests_ntlm import HttpNtlmAuth
import datetime

###################################################################################
Wescrapping Data Anaylsis Project
###################################################################################

now = datetime.datetime.now()
print("Today's Date: ", now.date())
print("Last Time Page Was Updated: ", now.strftime('%H:%M:%S'))

# initilization of webscraping from the online database

url = 'https://url-used.com'
closedDataUrl = 'https://second-url-used.com'
r = requests.get(url, auth=HttpNtlmAuth('domain\\username','password'))
rClosed = requests.get(closedDataUrl, auth=HttpNtlmAuth('domain\\username','password'))
data = r.text
dataClosed = rClosed.text

# Setting Pandas Dataframe to parse the data from the online database

df = pd.read_html(data)
df_closed = pd.read_html(dataClosed)

# The dictionary to define the key and values that will be evaluated in this dashboard

# This code define the values for the keys in closedData_dict
c_ID = df_closed[5][2][1:]
c_program = df_closed[5][4][1:]
c_dateCreated = df_closed[5][6][1:]
c_closedDate = df_closed[5][7][1:]
c_Type = df_closed[5][8][1:]
c_cause4req = df_closed[5][10][1:]
c_Stat = df_closed[5][11][1:]
c_Cell = df_closed[5][12][1:]

closedData_dict = {
    'ID' : c_ID,
    'Program' : c_program,
    'Created On' : c_dateCreated,
    'Type' : c_Type,
    'Cause for Request' : c_cause4req,
    'Status' : c_Stat,
    'Cell' : c_Cell,
    'Closed Date' : c_closedDate
}

# Keeps the dictionary ordered the way it is listed
c_dataDict = collections.OrderedDict(closedData_dict)

# This code define the values for the keys in data_dict

id_num = df[6][2][2:]
program = df[6][5][2:]
dateCreated = df[6][9][2:]
dtype = df[6][10][2:]
issueDesc = df[6][11][2:]
cause4req = df[6][12][2:]
stat = df[6][13][2:]
cell = df[6][14][2:]
stat = df[6][16][2:]

# The dictionary to define the key and values that will be evaluated in this dashboard

datadict = {
    'ID' : id_num,
    'Program' : program,
    'Created On' : dateCreated,
    'Type' : dtype,
    'Desciption of Issue' : issueDesc,
    'Cause for Request' : cause4req,
    'Status' : stat,
    'Cell' : cell,
    'Status' : stat
}

# Keeps the dictionary ordered the way it is listed
data_dict = collections.OrderedDict(datadict)

# The organized dataframe after sorting out unwanted information from the previous df
# This will be used as the main dataframe

mainDf = pd.DataFrame(data_dict)
mainDf.set_index('ID', inplace=True)
print(mainDf)

# Closed Dataframe information
closedDf = pd.DataFrame(c_dataDict)
closedDf.set_index('ID', inplace=True)
#print(closedDf)

# Function that automatically calculates the number of request in the online database
def count():
    count = 0
    for info in mainDf['Program']:
        count += 1
    return(count)

def c_count():
    c_count = 0
    for info in closedDf['Program']:
        c_count += 1
    return(c_count)

# Code that groups set categories together from the main dataframe

rGroup = mainDf[['Created On', 'Cause for Request', 'Cell', 'Status', 'Number','Type']]

c_Group = closedDf[['Created On', 'Cause for Request', 'Cell', 'Status', 'Closed Date', 'Number', 'Type']]

# This code will allow you to isolate categories of data that will allow you to compute the size in the upcoming codes
# Have to compute the size because all of the data in the online database is text... guess you can say I'm text mining

reqGroup = rGroup.groupby('Cause for Request')
cellGroup = rGroup.groupby('Cell')
statGroup = rGroup.groupby('Status')
numGroup = rGroup.groupby('Number')
typeGroup = rGroup.groupby('Type')

c_reqGroup = c_Group.groupby('Cause for Request')
c_cellGroup = c_Group.groupby('Cell')
c_StatGroup = c_Group.groupby('Status')
c_NoGroup = c_Group.groupby('Number')
c_TypeGroup = c_Group.groupby('Type')

# Creates the graphs that shows number records that are open vs. closed
from collections import Counter
list1 = c_No
counts = Counter(list1)
mcpn = counts.most_common(21)
df = pd.DataFrame(mcpn)
df.columns = ['Numbers', 'Number Requested']

list2 = p_no
counts1 = Counter(list2)
mcpn1 = counts1.most_common(11)
df2 = pd.DataFrame(mcpn1)
df2.columns = ['Numbers', 'Number Requested']

fig, axs = plt.subplots(ncols=2, figsize=(15, 6))

for i, data in enumerate(mcpn):
    mrpnOpen = df.plot(kind='bar',ax=axs[0],legend=None, title="Most Requested Number (Open)", color='purple')
    noPlot.set_ylabel('# of Request')
    mrpnClosed = df2.plot(kind='bar',ax=axs[1],legend=None, title="Most Requested Number (Closed)", color='green')

# Prints out the Most Requested for the open and closed tickets
print(df)
print(df2)

# Creates the bar graph based on the number of request per cell
c_cellTotal = c_cellGroup.size()
cellTotal = cellGroup.size()
fig, axs = plt.subplots(ncols=2, figsize=(15, 6))
plt.tight_layout()

for i, data in enumerate(cellTotal):
    cellPlot = cellTotal.plot(kind='bar',ax=axs[0],legend=None,
                              title="Open Cell Request", color='indianred')
    cellPlot.set_ylabel('# of Request')
    c_cellPlot = c_cellTotal.plot(kind='bar',ax=axs[1],legend=None,
                                  title="Closed Cell Request", color='darkred')

#Prints Numerical Data for the Open and Closed Request

print("Open Data")
print(cellTotal)
print("Total Number of Open Data Request: ", count())
print("\n\n")
print("Closed Data")
print(c_cellTotal)
print("Total Number of Closed Data Request: " , c_count())

# This code outputs the cause for request per cell in the form of stacked bar graphs. Open vs Closed.

matplotlib.style.use('ggplot')
cvr = mainDf.groupby(['Cell', 'Cause for Request'])['Cell'].count().unstack('Cause for Request').fillna(0)
cvrPrint = cvr.plot(kind='bar', stacked = True, title="Cells Vs. Cause For Request (Open)")
cvrPrint.set_ylabel('# of Request')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(15, 8)
print(cvrPrint)

cvrChart = mainDf.groupby(['Cell', 'Cause for Request'])
cs = cvrChart.size()
print(cs) #Prints the numerical data for the graph

matplotlib.style.use('ggplot') #Graph for Closed data
c_cvr = closedDf.groupby(['Cell', 'Cause for Request'])['Cell'].count().unstack('Cause for Request').fillna(0)
c_cvrPrint = c_cvr.plot(kind='bar', stacked = True, title="Cells Vs. Cause For Request (Closed)")
c_cvrPrint.set_ylabel('# of Request')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(15, 8)
print(c_cvrPrint)

c_cvrChart = closedDf.groupby(['Cell', 'Cause for Request'])
c = c_cvrChart.size()
print(c)

# Creates the pie chart based on the Cause of request
# Pie chart, where the slices will be ordered and plotted counter-clockwise:

labels = 'Damaged', 'Lost', 'Not Functional', 'Not Issued'
reqTotal = reqGroup.size()
explode = (0, 0.2, 0, 0)  # only "explode" the 2nd slice (i.e. 'Lost')

fig1, ax1 = plt.subplots()
ax1.pie(reqTotal, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
print(reqTotal)
print("\nThe total count of open request:", count())

##Closed Request
labels = 'Damaged', 'Lost', 'Not Functional', 'Not Issued'
c_reqTotal = c_reqGroup.size()
explode = (0, 0.2, 0, 0)  # only "explode" the 2nd slice (i.e. 'Lost')

fig1, ax1 = plt.subplots()
ax1.pie(c_reqTotal, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
print(c_reqTotal)
print("\nThe total count of closed request:", c_count())

###################################################################################

