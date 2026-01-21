from urlextract import URLExtract
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