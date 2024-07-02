from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

        #1. number of messages
    num_messages=df.shape[0]
        #2. number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
    #3. fetch no. of media messages
    num_media_msg=df[df['message']=='<Media omitted>\n'].shape[0]

    #4fetch number of links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_msg,len(links)
    
def fetch_most_busy_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
    columns={'index':'name','user':'percent'}
    )
    return x,df
def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_commwords(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return pd.DataFrame((Counter(words).most_common(80)),columns=["Words","Frequency"])

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time']=time
    return timeline