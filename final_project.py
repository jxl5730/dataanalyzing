#!/usr/bin/env python
# coding: utf-8

# In[1]:


import finalproject_data
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
get_ipython().system('pip install statsmodels.api')
import statsmodels.api as sm
dfvideo=finalproject_data.dfvideo
dfuser=finalproject_data.dfuser
videos=finalproject_data.videos
users=finalproject_data.users


# In[2]:


dfu=dfuser.reset_index(drop=True)
sub = dfu['Subscribers'].tolist()
for video in videos:
    i=videos.index(video)
    dfvideo.loc[video,'Subscribers']=sub[i]
    values=dfvideo.loc[video,'Est. Video Value']
    views=dfvideo.loc[video,'Video Views']
    likes=dfvideo.loc[video,'Likes']
    dislikes=dfvideo.loc[video,'Dislikes']
    comm=dfvideo.loc[video,'Comments']
    subs=dfvideo.loc[video,'Subscribers']
    temp = re.findall('[0-9.]+',values)
    estv=int((float(temp[0])+float(temp[1]))/2*1000)
    dfvideo.loc[video,'Est. Avg Video Value']=str(estv)
    dfvideo.loc[video,'View Ratio']=int(views)/int(subs)
    dfvideo.loc[video,'Like Ratio']=int(likes)/int(views)
    dfvideo.loc[video,'Dislike Ratio']=int(dislikes)/int(views)
    dfvideo.loc[video,'Engagement Ratio']=int(comm)/int(views)
    
dfvideo


# In[3]:


df = dfvideo.reset_index(drop=True)
labels = ['V1', 'V2', 'V3', 'V4', 'V5']
dislikes_count = df['Dislikes'].astype(int).tolist()
likes_count= df['Likes'].astype(int).tolist()
views_count=df['Video Views'].astype(int).tolist()

x = np.arange(len(labels))  
width = 0.35  
fig, ax = plt.subplots()
rects1 = ax.bar(x - width, dislikes_count, width, label='dislikes')
rects2 = ax.bar(x, likes_count, width, label='likes')
rects3 = ax.bar(x + width, views_count, width, label='views')

ax.set_ylabel('Numbers')
ax.set_title('Video feedbacks')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()

plt.show()


# In[4]:


X = df[['Video Views','Likes','Comments']].astype(float)
y = df['Est. Avg Video Value'].astype(float)
model = sm.OLS(y, X).fit()
model.summary()


# In[5]:


X = df[['Video Views']].astype(float)
y = df['Est. Avg Video Value'].astype(float)
model = sm.OLS(y, X).fit()
predictions = model.predict(X)
model.summary()


# In[6]:


plt.scatter(X, y)
plt.plot(X, predictions, color='red')
plt.show()


# In[7]:


for user in users:
    values=dfuser.loc[user,'Est. Partner Earning(Monthly)'].split('-')
    temp=[]
    for v in values:
        if 'K' in v:
            t = re.findall('[0-9.]+',v)
            tem=int(float(t[0])*1000)
        else:
            t = re.findall('[0-9.]+',v)
            tem=int(float(t[0]))
        temp.append(tem)
    estv=int((float(temp[0])+float(temp[1]))/2)
    dfuser.loc[user,'Est. Avg Partner Earning(Monthly)']=str(estv)
    earn=dfuser.loc[user,'Est. Potential Earnings']
    vdnum=dfuser.loc[user,'Total Videos']
    total_v=dfuser.loc[user,'Total Video Views']
    dfuser.loc[user,'Average video views']=int(total_v)/int(vdnum)   
    if 'M' in earn:
        n = re.findall('[0-9.]+',earn)
        v=int(float(n[0])*1000000)
    if 'K' in earn:
        n = re.findall('[0-9.]+',earn)
        v=int(float(n[0])*1000)
    dfuser.loc[user,'Est. Avg Earning per video']=str(v)
dfuser
        


# In[8]:


dfus = dfuser.reset_index(drop=True)


# In[9]:


X = dfus[['Subscribers','Total Video Views','Average video views']]
y = dfus['Est. Avg Partner Earning(Monthly)']
model = sm.OLS(y.astype(float), X.astype(float)).fit()
model.summary()


# In[10]:


X = dfus[['Average video views']].astype(float)
Y = dfus['Est. Avg Partner Earning(Monthly)'].astype(float)
model = sm.OLS(Y, X).fit()
predictions = model.predict(X)
model.summary()


# In[11]:


plt.scatter(X,Y)
plt.plot(X, predictions, color='red')
plt.show()


# In[12]:


X = dfus[['Subscribers','Average video views','Total Videos','Total Video Views']]
y = dfus['Est. Avg Earning per video']
model = sm.OLS(y.astype(float), X.astype(float)).fit()
model.summary()


# In[13]:


X = dfus[['Average video views']].astype(float)
y = dfus['Est. Avg Earning per video'].astype(float)
model = sm.OLS(y, X).fit()
predictions = model.predict(X)
model.summary()


# In[14]:


plt.scatter(X,y)
plt.plot(X, predictions, color='red')
plt.show()


# In[15]:


from bs4 import BeautifulSoup
import urllib
import requests
req = requests.get('https://influencermarketinghub.com/youtube-money-calculator/')
soup = BeautifulSoup(req.content, 'html.parser')
tags=soup('div')
for tag in tags:
    cl=tag.get('class')
    info=tag.get_text().strip()
    if cl==['mks_pullquote', 'mks_pullquote_left']:
        infor=info
print(infor)
inform=infor.split(' ')
words=[]
for word in inform:
    if '$' in word:
        words.append(word)
cpm=words[-1]


# In[16]:


CPM = re.findall('[0-9.]+',cpm)
dfus.loc[:,'CPM']=CPM
dfus.loc[:,'Est. video Earning CPM based']=dfus.loc[:,'Average video views'].astype(float)/1000*dfus.loc[:,'CPM'].astype(float)
dfus


# In[17]:


X = dfus.loc[:,'Average video views'].astype(float)
Y = dfus.loc[:,'Est. video Earning CPM based'].astype(float)
Z=dfus.loc[:,'Est. Avg Earning per video'].astype(float)
plt.scatter(X,Z)
plt.plot(X, Y, color='red')
plt.show()

