from dotenv import load_dotenv
import os
import pylast
import pandas as pd
from tqdm import tqdm

load_dotenv()

API_KEY = os.getenv('KEY')
API_SECRET = os.getenv('SECRET')

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET)

def get_artist_tags(artist_name):
    try:
        artist = network.get_artist(artist_name)
        tags = artist.get_top_tags(limit=3) 
        
        if tags:
            tag_names = [tag.item.name for tag in tags]
            return ', '.join(tag_names) 
        else:
            return "No tags"
        
    except pylast.WSError as e:
        print(f"Error fetching tags for {artist_name}: {e}")
        return "No tags"  

if __name__ == '__main__':

    input_csv = 'data/Stream_hist.csv' 
    output_csv = 'data/Genre_hist.csv'  

    hist_df = pd.read_csv(input_csv)
    artist_df = hist_df.groupby(by='artistName', as_index=False).agg({'msPlayed':'sum'})
    
    if 'artistName' not in hist_df.columns:
        raise ValueError("CSV must contain an 'artistName' column")
    
    artist_list = artist_df['artistName']
    
    data = []

    for artist in tqdm(artist_list, desc="Fetching artist tags"):
        tag = get_artist_tags(artist)
        data.append(tag)
    
    artist_df['Genre'] = data
    artist_df.to_csv(output_csv, index=False)