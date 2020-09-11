#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib
import requests
con = requests.get('https://www.noxinfluencer.com/youtube-video-rank')
soup = BeautifulSoup(con.content, 'html.parser')
tags=soup('a')
videolink={}
users=[]
videos=[]
userlink={}
detail={}
userdetail={}
for tag in tags:
    cl=tag.get('class')
    if cl==['video-title']:
        head1=tag.get_text()
        link1=tag.get('href')
        videolink[head1]=link1
        videos.append(head1)
    if cl==['video-info']:
        heading=tag.get_text()
        link=tag.get('href')
        videolink[heading]=link
        videos.append(heading)
for tag in tags:
    cl=tag.get('class')
    if cl==['detail-data', 'name']:
        name1=tag.get('title').strip()
        l1=tag.get('href')
        userlink[name1]=l1
        users.append(name1)
    if cl==['name']:
        name=tag.get_text().strip()
        l=tag.get('href')
        userlink[name]=l
        users.append(name)


# In[9]:


for video in videos:
    lk=videolink[video]
    c = requests.get(f'https://www.noxinfluencer.com{lk}')
    s = BeautifulSoup(c.content, 'html.parser')
    divs=s('div')
    detail[video]=[]
    for div in divs:
        c=div.get('class')
        num=div.get_text().strip()
        if c==["content"]:
            if '$' in num:
                detail[video].append(num)


# In[10]:

userdetails={}
for user in users:
    ulk=userlink[user]
    req = requests.get(f'https://www.noxinfluencer.com{ulk}')
    sp = BeautifulSoup(req.content, 'html.parser')
    ds=sp('div')
    userdetail[user]=[]
    for d in ds:
        cls=d.get('class')
        nu=d.get_text().strip()
        if cls==['card-content']:
            userdetail[user].append(nu)
    userdetails[user]=userdetail[user][1:]


# In[11]:


import pandas as pd
dfuser = pd.DataFrame.from_dict(userdetails,orient='index',columns=['Rank','Rating', 'Published Videos', 'Est. Partner Earning(Monthly)', 'Est. Potential Earnings'])
dfvideo= pd.DataFrame.from_dict(detail,orient='index',columns=['Est. Video Value'])


# In[19]:


import requests
import json
def get_data(user):
    api_key='AIzaSyBO6h7NiO6_sYMK0VnmXZUzkym-1r9Wltk'
    resp=requests.get(f'https://www.googleapis.com/youtube/v3/search?type=channel&part=snippet&q={user}&key={api_key}')
    js=resp.json()
    channelid=js['items'][0]['id']['channelId']
    res=requests.get(f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelid}&key={api_key}')
    st=res.json()
    stat=st['items'][0]['statistics']
    requ=requests.get(f'https://www.googleapis.com/youtube/v3/channels?part=snippet&maxResults=50&id={channelid}&key={api_key}')
    lc=requ.json()
    local=lc['items'][0]['snippet']
    dfuser.loc[user,'Description']=local['localized']['description']
    dfuser.loc[user,'Subscribers']=stat['subscriberCount']
    dfuser.loc[user,'Total Video Views']=stat['viewCount']
    dfuser.loc[user,'Total Videos']=stat['videoCount']
def get_vdata(video):
    api_key='AIzaSyBO6h7NiO6_sYMK0VnmXZUzkym-1r9Wltk'
    link=videolink[video]
    vid=link.split("/")[-1]
    r=requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={vid}&key={api_key}')
    statics=r.json()
    sta=statics['items'][0]['statistics']
    dfvideo.loc[video,'Video Views']=sta['viewCount']
    dfvideo.loc[video,'Likes']=sta['likeCount']
    dfvideo.loc[video,'Dislikes']=sta['dislikeCount']
    dfvideo.loc[video,'Comments']=sta['commentCount']  
for user in users:
    get_data(user)
for video in videos:
    get_vdata(video)


# In[ ]:




