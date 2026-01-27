import pandas as pd
import re
def preprocess(data):
    pattern = r"(\d{2}\/\d{2}\/\d{2}),\s(\d{1,2}:\d{2}:\d{2}\s?[AP]M)\] "
    parts = re.split(pattern, data)

    parts = parts[1:]

    dates = []
    times = []
    messages = []

    for i in range(0, len(parts), 3):
      dates.append(parts[i])
      times.append(parts[i+1])
      messages.append(parts[i+2])
    df = pd.DataFrame({
    "date": dates,
    "time": times,
    "message": messages
    })
    df["time"] = df["time"].str.replace("\u202f", " ", regex=False)



    df["datetime"] = pd.to_datetime(
    df["date"] + " " + df["time"],
    format="%d/%m/%y %I:%M:%S %p"
  )
  
    print(len(df), "messages parsed successfully!")
    def extract_sender_message(msg):  

      if ":" in msg:
        parts = msg.split(":", 1)
        sender = parts[0].strip()
        message = parts[1].strip()
      else:
        sender = None
        message = msg.strip()
      return sender, message

    df['sender'], df['clean_message'] = zip(*df['message'].apply(extract_sender_message))
    
    
    df['year'] = df['datetime'].dt.year
    df['month']=df['datetime'].dt.month
    df['day_name']=df['datetime'].dt.day_name()
    df['month_name']=df['datetime'].dt.month_name()
    df['date_only'] = df['datetime'].dt.date  
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    period=[]
    for hour in df[['day_name','hour']]['hour']:
      if hour==23:
        period.append(str(hour)+'-'+str('00'))
      elif hour==0:
        period.append(str(hour)+'-'+str('1'))
      else:
        period.append(str(hour)+'-'+str(hour+1))
    df['period']=period
       
    

    return df
  