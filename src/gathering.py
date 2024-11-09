import pandas as pd

def extract_year(value):
    try:
        # If it's a full date, extract the year
        return pd.to_datetime(value, errors='coerce').year
    except:
        # If conversion fails, return None or a specific value (e.g., NaN)
        return None

def main():

    artists = pd.read_csv('data/artists_final.csv')
    artists = artists.rename(columns={
        'name':'artistName',
        'genres':'artistGenre',
        'popularity':'artistPop',
        'related_artists':'artistRelated'
    })

    track_ambre = pd.read_csv('data/track_info_ambre.csv')
    track_ambre['listener'] = 'Ambre'

    track_arnaud = pd.read_csv('data/track_info_arnaud.csv')
    track_arnaud['listener'] = 'Arnaud'

    track_elwin = pd.read_csv('data/track_info_elwin.csv')
    track_elwin['listener'] = 'Elwin'

    track_fanny = pd.read_csv('data/track_info_fan.csv')
    track_fanny['listener'] = 'Fanny'

    track_oli = pd.read_csv('data/track_info_oli_small.csv')
    track_oli['listener'] = 'Olivier'

    track_df = pd.concat([track_ambre,track_arnaud,track_elwin, track_fanny, track_oli])

    final_df = track_df.merge(artists, how='inner', on='artistName')
    
    final_df['artistGenre'] = final_df['artistGenre'].str.replace(r"[\[\]']", "", regex=True)
    final_df['artistRelated'] = final_df['artistRelated'].str.replace(r"[\[\]']", "", regex=True)

    final_df.to_csv('data/spotify_info_final.csv')

if __name__ == '__main__':
    main()



