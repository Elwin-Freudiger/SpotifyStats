"""
This script changes the Json listening history data and transforms it into a dataframe. 
"""
#load packages
import pandas as pd 
import glob


def main(person):
    
    streaming_df = pd.DataFrame() #create an empty df

    #loop every file extract the listening history and add it to the df
    for file in glob.glob(f"data/StreamingHistory_music_*_{person}.json"):
        temp_df = pd.read_json(file)
        streaming_df = pd.concat([streaming_df, temp_df], axis=0, ignore_index=True)

    #remove the listening time stamp, group by sum to get the total listening time of every song.
    streaming_df = (streaming_df
                    .drop(columns='endTime')
                    .groupby(by="trackName", as_index=False)
                    .agg(msPlayed=('msPlayed', 'sum'),            
                        artistName=('artistName', 'first'))
                    )
    
    stream_hist = streaming_df[streaming_df['msPlayed'] >= 180000]

    stream_hist.to_csv(f'data/Stream_hist_{person}.csv')

if __name__ == "__main__":
    main("arnaud")

    
