import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from alive_progress import alive_bar
import time
import urllib.parse
from functools import wraps
from time import time, sleep
import ratelimiter


load_dotenv()

API_ID = os.getenv('SPOT_ID')
API_SECRET = os.getenv('SPOT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=API_ID,
                                                           client_secret=API_SECRET))

def format_spotify_query(artist, track):
    artist_encoded = urllib.parse.quote(f"artist:{artist}")
    track_encoded = urllib.parse.quote(f"track:{track}")
    return f"{artist_encoded}+{track_encoded}"

# Define a rate limiter decorator
def rate_limiter(max_calls, period):
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Clear out calls that are outside the time window
            nonlocal calls
            now = time()
            calls = [call for call in calls if now - call < period]
            
            # Enforce rate limit by waiting if needed
            if len(calls) >= max_calls:
                wait_time = period - (now - calls[0])
                sleep(wait_time)
                now = time()
                calls = [call for call in calls if now - call < period]

            # Make the API call and record the timestamp
            result = func(*args, **kwargs)
            calls.append(time())
            return result

        return wrapper
    return decorator


# Apply the rate limiter with a limit of 10 calls per 30 seconds
MAX_CALLS = 1
PERIOD = 1

@rate_limiter(MAX_CALLS, PERIOD)
def extract_track_info(artist_name, track_name, time_played):
    retry = 0
    query = format_spotify_query(artist_name, track_name)
    # Search for track information
    result = sp.search(q=query, limit=1, type='track')
    track = result.get('tracks', {}).get('items', [])

    if track:
        track_data = track[0]
        album = track_data.get('album', {}) 
        album_name = album.get('name', track_name)
        release_date = album.get('release_date', "No release date")
        popularity = track_data.get('popularity', 0)
        return {
            'trackName': track_name,
            'artistName': artist_name,
            'msPlayed': time_played,
            'albumName': album_name,
            'releaseDate': release_date,
            'trackPop': popularity
        } 
    else:
        return {
            'trackName': track_name,
            'artistName': artist_name,
            'msPlayed': time_played,
            'albumName': "Error",
            'releaseDate': "Error",
            'trackPop': 0
        }

def main(name):
    df = pd.read_csv(f'data/Stream_hist_{name}.csv')
    
    track_info_list = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        with alive_bar(len(df)) as bar:
            future_to_row = {
                executor.submit(
                    extract_track_info,
                    row['artistName'],
                    row['trackName'],
                    row['msPlayed']
                ): row for _, row in df.iterrows()
            }
            
            for future in as_completed(future_to_row):
                track_info = future.result()
                track_info_list.append(track_info)
                bar() 

    info_df = pd.DataFrame(track_info_list)
    info_df.to_csv(f'test/track_info_{name}.csv', index=False)

if __name__ == "__main__":
    main('elwin')

