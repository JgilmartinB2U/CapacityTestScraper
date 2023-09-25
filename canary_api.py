import requests
import pandas as pd
import json
import datetime
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def getDetailed(
        tags, 
        start_date, 
        end_date, 
        aggInterval = '00:05:00', 
        maxSize=1000000, 
        start_time = '00:00:00', 
        end_time = '23:59:59', 
        ):
    data = {}
    tag_list = tags
    data["startTime"] = start_date + 'T' + start_time
    data["endTime"] = end_date + 'T' + end_time
    data["maxSize"] = maxSize
    data['tags'] = tag_list 
    data["aggregateName"] = "TimeAverage2"
    data["aggregateInterval"] = aggInterval
    data['includeQuality'] = True
    dfs = []
    
    try:
        response = requests.get('http://192.168.40.33:55235/api/v2/getTagData2', data=data)
        file = open('response.txt', 'w')
        
        json_text = json.loads(response.text)
        f = open('response.txt', 'w')
        for tag in tag_list:
            try:
                df = pd.json_normalize(json_text['data'][tag])
                df['tag'] = tag
                dfs.append(df)
                
            except:
                print("ERROR IN API PULL, writing data for: ", tag)
                print(json_text)
                with open('data.json', 'w') as f:
                    json.dump(json_text, f)
        df = pd.concat(dfs)
        return df
    except Exception as e:
        print(f'ERROR {e}')
        print('Saving to file')
        with open('data.json', 'w') as f:
            json.dump(json_text, f)

def dfTranspose(df):
    df['t'] = pd.to_datetime(df['t'])
    pivot_df = df.pivot(index='t', columns='tag', values='v')
    # renamed = rename_columns(pivot_df)
    return pivot_df