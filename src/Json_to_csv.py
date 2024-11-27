"""
This script changes the Json listening history data and transforms it into a dataframe. 
"""
#load packages
import pandas as pd 
import glob


def person(person):
    
    streaming_df = pd.DataFrame() #create an empty df

    #loop every file extract the listening history and add it to the df
    for file in glob.glob(f"data/raw_json/StreamingHistory_music_*_{person}.json"):
        temp_df = pd.read_json(file)
        streaming_df = pd.concat([streaming_df, temp_df], axis=0, ignore_index=True)

    #remove the listening time stamp, group by sum to get the total listening time of every song.
    """
    streaming_df = (streaming_df
                    .drop(columns='endTime')
                    .groupby(by="trackName", as_index=False)
                    .agg(msPlayed=('msPlayed', 'sum'),            
                        artistName=('artistName', 'first'))
                    )
    """

    streaming_df.to_csv(f'data/timeserie/Stream_hist_{person}.csv')
def main():
    peoples = ["ambre", "arnaud", "elwin", "fan", "oli"]
    for unit in peoples:
        person(unit)

if __name__ == "__main__":
    main()

    
