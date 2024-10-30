import pandas as pd
from dotenv import load_dotenv #type:ignore
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import aiohttp
import asyncio
from ratelimit import limits, sleep_and_retry
from tqdm.asyncio import tqdm_asyncio

load_dotenv()

API_ID = os.getenv('SPOT_ID')
API_SECRET = os.getenv('SPOT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=API_ID,
                                                           client_secret=API_SECRET))

INITIAL_REQUESTS_LIMIT = 180  # Initial requests limit
REQUEST_PERIOD = 60  # Period in seconds for request limits
RETRY_BACKOFF = 2  # Multiplier for exponential backoff
MAX_RETRY_ATTEMPTS = 5  # Limit the retry attempts

@sleep_and_retry
async def fetch_artist_info(artist_name, session, request_limit):
    retry_attempts = 0
    while retry_attempts < MAX_RETRY_ATTEMPTS:
        try:
            params = {'q': artist_name, 'type': 'artist', 'limit': 1}
            async with session.get("https://api.spotify.com/v1/search", params=params) as response:
                if response.status == 429:  # Rate limit error
                    retry_attempts += 1
                    retry_after = int(response.headers.get("Retry-After", REQUEST_PERIOD))  # Wait time in seconds
                    request_limit = max(1, request_limit // 2)  # Reduce limit by half each time
                    print(f"Rate limited. Retrying after {retry_after} seconds with new limit: {request_limit}")
                    await asyncio.sleep(retry_after * (RETRY_BACKOFF ** retry_attempts))  # Exponential backoff
                    continue  # Retry after waiting

                result = await response.json()
                artist_items = result.get('artists', {}).get('items', [])

                if artist_items:
                    artist_data = artist_items[0]
                    genres = artist_data.get('genres', [])
                    popularity = artist_data.get('popularity', 0)  # Default to 0 if no popularity is available
                    if not genres:
                        genres = ["No genres available"]

                    artist_id = artist_data.get('id')
                    similar_artists_data = sp.artist_related_artists(artist_id)
                    similar_artists = [artist['name'] for artist in similar_artists_data['artists'][:3]]
                    
                    return {
                        'name': artist_name,
                        'genres': genres,
                        'popularity': popularity,
                        'related_artists': similar_artists
                    }
                else:
                    return {'name': artist_name, 'genres': ["Not found"], 'popularity': 0, 'related_artists': ["None"]}
        
        except aiohttp.ClientConnectionError as e:
            retry_attempts += 1
            wait_time = REQUEST_PERIOD * (RETRY_BACKOFF ** retry_attempts)
            print(f"Connection error: {e}. Retrying in {wait_time} seconds (Attempt {retry_attempts}/{MAX_RETRY_ATTEMPTS})...")
            await asyncio.sleep(wait_time)
            continue 

        except Exception as e:
            print(f"Error fetching info for {artist_name}: {e}")
            return {'name': artist_name, 'genres': ["Error"], 'popularity': 0, 'related_artists': ["Error"]}

    print(f"Failed to fetch info for {artist_name} after {MAX_RETRY_ATTEMPTS} attempts.")
    return {'name': artist_name, 'genres': ["Error"], 'popularity': 0, 'related_artists': ["Error"]}


async def gather_artist_info(artist_names):
    """
    Gathers artist info concurrently for all unique artists in the list, with a progress bar.
    """
    access_token = sp.auth_manager.get_access_token(as_dict=False)
    request_limit = INITIAL_REQUESTS_LIMIT

    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {access_token}"}) as session:
        tasks = [fetch_artist_info(artist_name, session, request_limit) for artist_name in artist_names]
        artist_data = await tqdm_asyncio.gather(*tasks, desc="Fetching artist info", total=len(tasks))
        return artist_data

def main(name):
    df = pd.read_csv(f'data/Stream_hist_{name}.csv')
    artist_list = df['artistName'].unique()
    artist_info = asyncio.run(gather_artist_info(artist_list))
    artist_df = pd.DataFrame(artist_info)
    artist_df.to_csv(f"data/artist_info_{name}.csv", index=False)

def main2():
    df = pd.read_csv('data/artist_info_oli.csv')
    df_short = df[df['popularity']==0]
    df_initial = df[df['popularity']!=0]
    artist_list = df_short['name']
    artist_info = asyncio.run(gather_artist_info(artist_list))
    artist_df = pd.DataFrame(artist_info)
    updated_df = pd.concat([artist_df, df_initial])
    updated_df.to_csv('data/artist_info_oli_final.csv')


if __name__ == "__main__":
    main2()
