# -*- coding: utf-8 -*-
"""
Created on Fri May  6 17:09:32 2022

@author: Michael
"""

import json
import matplotlib.pyplot as plt
import pandas as pd

#Importing Facebook Data
with open("message_1.json", "r") as read_file:
    data = json.load(read_file)

messages = data.get('messages') #Extracting messages list of dicts from data dict
messages = pd.DataFrame(messages) #Converting the list of dicts to dataframes
messages['timestamp_ms'] = pd.to_datetime(messages['timestamp_ms'], unit='ms') #Converting message/conversation timestamps to datetime

#Calculating total time voice/video talk
total_talk_time = messages['call_duration'].sum() #Total time in seconds spent talking in this thread
talk_hours = total_talk_time // 3600
talk_minutes = ((total_talk_time / 3600) - talk_hours) * 60
print('Daniella and Michael have voice or video called for a total of ' + str(talk_hours) + ' hours and ' + str(talk_minutes) + ' minutes.')

#Preparing activity for plotting
sent_by_dani = messages.loc[messages['sender_name'] == 'Daniella Silva'] #Separating messages sent by Daniella
sent_by_michael = messages.loc[messages['sender_name'] == 'Michael Jensen'] #Separating messages sent by Michael

sent_by_dani_grouped = sent_by_dani.groupby(pd.Grouper(key='timestamp_ms', axis=0, freq='M'))['timestamp_ms'].count()
sent_by_dani_grouped = pd.DataFrame([sent_by_dani_grouped]).transpose()
sent_by_dani_grouped = sent_by_dani_grouped.rename(columns={'timestamp_ms': 'Sent by Daniella'})

sent_by_michael_grouped = sent_by_michael.groupby(pd.Grouper(key='timestamp_ms', axis=0, freq='M'))['timestamp_ms'].count()
sent_by_michael_grouped = pd.DataFrame([sent_by_michael_grouped]).transpose()
sent_by_michael_grouped = sent_by_michael_grouped.rename(columns={'timestamp_ms': 'Sent by Michael'})

grouped_activity = pd.merge(sent_by_dani_grouped, sent_by_michael_grouped, on='timestamp_ms')
grouped_activity.index = grouped_activity.index.strftime('%b %Y') #Converting datetime index to month and year string

#Plotting activity
ax = grouped_activity.plot(kind="bar")
fig = ax.get_figure() #Get a Matplotlib figure from the axes object for formatting purposes
fig.set_size_inches(35, 25) #Change the plot dimensions (width, height)
ax.set_xlabel("Month", fontsize = 30) #Change the axes labels
ax.set_ylabel("Activity (messages, calls, shares, etc.)", fontsize = 30)
plt.xticks(fontsize = 30)
plt.yticks(fontsize = 30)
plt.title("Facebook Messenger Activity Between Michael and Daniella", fontsize = 40)
plt.legend(prop = {"size":30})
plt.savefig("FB Messenger Communication.png")

