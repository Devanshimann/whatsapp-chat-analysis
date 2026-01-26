from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

extract=URLExtract()
def fetch(selected,df):
    if selected!="overall":
        df=df[df['sender']==selected]
    num_msg=df.shape[0]
    words=[]
    for msg in df['message']:
        words.extend(msg.split())
    media = df[df['message'].str.contains("omitted", case=False, na=False)].shape[0]
    links=[]
    links.extend(extract.find_urls(msg))
    return num_msg,len(words),media,len(links)
def busy(df):
    x=df['sender'].value_counts().head()
    df=round((df['sender'].value_counts()/df.shape[0])*100,2).reset_index().rename({'sender':'name','user':'percent'})
    print(df)
    return x,df
def word(selected,df):
    if selected!="overall":
        df=df[df['sender']==selected]
    wc=WordCloud(width=500,height=500,background_color='white')
    dfwc=wc.generate(df['message'].str.cat(sep=' '))
    return dfwc
def common(selected,df):
    if selected!="overall":
        df=df[df['sender']==selected]
    f=open("stop_hinglish.txt",'r')
    stop=f.read()
    temp=df[df['message']!='<image omitted>\n']
    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop:
                words.append(word)
    returndf=pd.DataFrame(Counter(words).most_common(20))
    return returndf

def emojihelper(selected,df):
    if selected!="overall":
        df=df[df['sender']==selected]
    emojilist=[]
    for msg in df['message']:
        for c in msg:
          if emoji.is_emoji(c): 
            emojilist.append(c)
    if len(emojilist) == 0:
        return pd.DataFrame(columns=['emoji', 'count'])
    emojidf=pd.DataFrame(Counter(emojilist).most_common(len(Counter(emojilist))),columns=['emoji','count'])
    return emojidf

def month(selected,df):
    if selected!="overall":
        df=df[df['sender']==selected]
    timeline=df.groupby(['year','month_name','month']).count()['message'].reset_index()
    
    time=[]
    for i in range(timeline.shape[0]):
      time.append(timeline['month_name'][i]+'-'+str(timeline['year'][i]))
    return timeline,time
def day(selected,df):
    if selected!="overall":
        df=df[df['sender']==selected]
    return df['day_name'].value_counts()
def month_activity(selected,df):
    if selected!="overall":
        df=df[df['sender']==selected]
    return df['month_name'].value_counts()
    
    



    
