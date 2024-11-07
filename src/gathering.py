import pandas as pd

def extract_year(value):
    try:
        # If it's a full date, extract the year
        return pd.to_datetime(value, errors='coerce').year
    except:
        # If conversion fails, return None or a specific value (e.g., NaN)
        return None

def main():
    track_ambre = pd.read_csv('data/track_info_ambre.csv')
    artist_ambre = pd.read_csv('data/artist_info_ambre.csv')
    #artist_ambre = artist_ambre[artist_ambre['genres']!= "['No genres available']"]
    track_ambre['listener'] = 'Ambre'
    artist_ambre = artist_ambre.rename(columns={
        'name':'artistName',
        'genres':'artistGenre',
        'popularity':'artistPop',
        'related_artists':'artistRelated'
    })
    spot_ambre = track_ambre.merge(artist_ambre, how='left', on='artistName')

    track_arnaud = pd.read_csv('data/track_info_arnaud.csv')
    artist_arnaud = pd.read_csv('data/artist_info_arnaud.csv')
    #artist_arnaud = artist_arnaud[artist_arnaud['genres']!= "['No genres available']"]
    track_arnaud['listener'] = 'Arnaud'
    artist_arnaud = artist_arnaud.rename(columns={
        'name':'artistName',
        'genres':'artistGenre',
        'popularity':'artistPop',
        'related_artists':'artistRelated'
    })
    spot_arnaud = track_arnaud.merge(artist_arnaud, how='left', on='artistName')

    track_elwin = pd.read_csv('data/track_info_elwin.csv')
    artist_elwin = pd.read_csv('data/artist_info_elwin.csv')
    track_elwin['listener'] = 'Elwin'
    artist_elwin = artist_elwin.rename(columns={
        'name':'artistName',
        'genres':'artistGenre',
        'popularity':'artistPop',
        'related_artists':'artistRelated'
    })
    spot_elwin = track_elwin.merge(artist_elwin, how='left', on='artistName')

    track_fanny = pd.read_csv('data/track_info_fan.csv')
    artist_fanny = pd.read_csv('data/artist_info_fan.csv')
    track_fanny['listener'] = 'Fanny'
    artist_fanny = artist_fanny.rename(columns={
        'name':'artistName',
        'genres':'artistGenre',
        'popularity':'artistPop',
        'related_artists':'artistRelated'
    })
    spot_fanny = track_fanny.merge(artist_fanny, how='left', on='artistName')

    track_oli = pd.read_csv('data/track_info_oli.csv')
    artist_oli = pd.read_csv('data/artist_info_oli.csv')
    track_oli['listener'] = 'Olivier'
    artist_oli = artist_oli.rename(columns={
        'name':'artistName',
        'genres':'artistGenre',
        'popularity':'artistPop',
        'related_artists':'artistRelated'
    })
    spot_oli = track_oli.merge(artist_oli, how='left', on='artistName')
    final_df = pd.concat([spot_ambre,spot_arnaud,spot_elwin, spot_fanny, spot_oli])
    final_df['releaseDate'] = final_df['releaseDate'].apply(extract_year)
    final_df['artistGenre'] = final_df['artistGenre'].str.replace(r"[\[\]']", "", regex=True)
    final_df['artistRelated'] = final_df['artistRelated'].str.replace(r"[\[\]']", "", regex=True)

    final_df.to_csv('data/spotify_info.csv')

if __name__ == '__main__':
    main()



