"""
This script changes the Json listening history data and transforms it into a classic dataframe. 
"""

import pandas as pd #load package
#this is the list of json files to extract the history
file_list = ["data/StreamingHistory_music_0.json", "data/StreamingHistory_music_1.json","data/StreamingHistory_music_2.json"]

streaming_df = pd.DataFrame() #create an empty df

#loop every file extract the listening history and add it to the df
for file in file_list:
    temp_df = pd.read_json(file)
    streaming_df = pd.concat([streaming_df, temp_df], axis=0, ignore_index=True)

#remove the listening time stamp, group by sum to get the total listening time of every song.
streaming_df = (streaming_df
                .drop(columns='endTime')
                .groupby(by="trackName", as_index=False)
                .agg(msPlayed=('msPlayed', 'sum'),            
                     artistName=('artistName', 'first'))
                )

#streaming_df.to_csv('data/Stream_hist.csv')

    
