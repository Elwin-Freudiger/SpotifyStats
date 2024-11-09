import pandas as pd

# Load the data
df = pd.read_csv('data/spotify_info.csv')

# Drop unnecessary columns
df = df.drop(columns=['Unnamed: 0'], errors='ignore')

# Standardize "No genres available" as NaN for consistency
df['artistGenre'] = df['artistGenre'].replace("No genres available", pd.NA)

# Standardize quotation marks in genre and related artist columns
df['artistGenre'] = df['artistGenre'].str.replace(r'["“”]', '', regex=True)
df['artistRelated'] = df['artistRelated'].str.replace(r'["“”]', '', regex=True)

# Correct release dates (Example: set all future dates to NaN)
import datetime
current_year = datetime.datetime.now().year
df['releaseDate'] = df['releaseDate'].apply(lambda x: x if x <= current_year else pd.NA)

# Optional: Drop rows with extremely faulty data (like blank album names and tracks)
df = df.dropna(subset=['trackName', 'artistName', 'albumName', 'releaseDate'])

# Display cleaned dataset
print(df.head())
df.to_csv('data/spotify_clean.csv')
