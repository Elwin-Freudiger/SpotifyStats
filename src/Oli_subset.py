import pandas as pd

df = pd.read_csv('data/track_info_oli.csv')

subset_df = df.sample(n=1500, random_state=42)
subset_df_drop = subset_df[subset_df['albumName']!="Error"]

subset_df_drop.to_csv('data/track_info_oli_small.csv')

