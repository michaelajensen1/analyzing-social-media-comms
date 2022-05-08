# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:16:38 2022

@author: Michael
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#Importing Snapchat Data
with open("chat_history.json", "r") as read_file:
    data = json.load(read_file)

#Extracting the list of dicts for received and sent messages
received_saved = data.get('Received Saved Chat History')
sent_saved = data.get('Sent Saved Chat History')

#Converting the list of dicts to dataframes
received_df = pd.DataFrame(received_saved)
sent_df = pd.DataFrame(sent_saved)

#Querying the dataframes to pull out messages sent to and from Daniella
received_df.query('From == "silvastreak27"',inplace = True)
received_df['Created'] = pd.to_datetime(received_df['Created']) #Converts the 'Created' column to datetime

sent_df.query('To == "silvastreak27"', inplace = True)
sent_df['Created'] = pd.to_datetime(sent_df['Created']) #Converts the 'Created' column to datetime


#Preparing data for plotting by grouping sent and received messages by month
received_monthly_group = received_df.groupby(pd.Grouper(key='Created', axis=0, freq='M'))['Text'].count()
sent_monthly_group = sent_df.groupby(pd.Grouper(key='Created', axis=0, freq='M'))['Text'].count()

received_monthly_group = pd.DataFrame(received_monthly_group) #GroupBy returns series, so converting back to df
sent_monthly_group = pd.DataFrame(sent_monthly_group) #GroupBy returns series, so converting back to df

comms = pd.merge(received_monthly_group, sent_monthly_group, on = "Created") #Merging sent and received dfs to single df
comms.index = comms.index.strftime('%b %Y') #Converting datetime index to month and year string
comms = comms.rename(columns={"Text_x": "Sent by Daniella", "Text_y": "Sent by Michael"})
comms.drop(index=comms.index[0:5],
                            axis = 0,
                            inplace = True) #Removing data before Jan 1 2018

#Plotting Figures
ax = comms.plot(kind="bar")
fig = ax.get_figure() #Get a Matplotlib figure from the axes object for formatting purposes
fig.set_size_inches(35, 25) #Change the plot dimensions (width, height)
ax.set_xlabel("Month", fontsize = 30) #Change the axes labels
ax.set_ylabel("Messages Sent", fontsize = 30)
plt.xticks(fontsize = 30)
plt.yticks(fontsize = 30)
plt.title("Snapchat Messages Between Michael and Daniella", fontsize = 40)
plt.legend(prop = {"size":30})
plt.savefig("Snapchat Communication.png")

# #Creating Word Cloud for Messages Sent by Michael
# text = " ".join(i for i in sent_df.Text)
# stopwords = set(STOPWORDS)
# wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
# plt.figure( figsize=(30,20))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()

# #Creating Word Cloud for Messages Sent by Daniella
# text2 = " ".join(i for i in received_df.Text)
# wordcloud2 = WordCloud(stopwords=stopwords, background_color="white").generate(text2)
# plt.figure( figsize=(30,20))
# plt.imshow(wordcloud2, interpolation='bilinear')
# plt.axis("off")
# plt.show()