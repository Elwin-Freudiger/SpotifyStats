import pandas as pd

original_df = pd.read_csv("data/clean_data/spotify_info.csv")

original_df = (
    original_df
    .assign(
       trackPop = lambda df: df['trackPop'].astype('int'),
       artistPop = lambda df: df['artistPop'].astype('int'),
       releaseDate = lambda df: df['releaseDate'].str[:4].astype('int')
       )
    .drop(columns=["Unnamed: 0.1"])

)

songs_df = original_df[['trackName', 'artistName', 'albumName', 'releaseDate', 'trackPop']].drop_duplicates().reset_index(drop=True)
songs_df['trackID'] = "T" + songs_df.index.astype(str)

artists_df = original_df[['artistName', 'artistPop', 'artistGenre', 'artistRelated']].drop_duplicates().reset_index(drop=True)

<<<<<<< Updated upstream
listening_history_df = original_df.merge(
    songs_df[['trackID', 'trackName', 'artistName']],
    how='left',
    on=['trackName', 'artistName']
)
=======
listening_history_df = original_df.merge(songs_df[['trackID', 'trackName', 'artistName']], how='left', on=['trackName', 'artistName'])
>>>>>>> Stashed changes
listening_history_df = listening_history_df[['listener', 'trackID', 'msPlayed']]

songs_df.to_csv("data/clean_data/Tracks.csv", index=False)
artists_df.to_csv("data/clean_data/Artists.csv", index=False)
listening_history_df.to_csv("data/clean_data/Listening_History.csv", index=False)
