#artists genre
library(dplyr)

# drop the rows where there are "no genres available" for each db
df_ambre <- read.csv("data/artist_info_ambre.csv")
df_arnaud <- read.csv("data/artist_info_arnaud.csv")
df_elwin <- read.csv("data/artist_info_elwin.csv")
df_fan <- read.csv("data/artist_info_fan.csv")
df_oli <- read.csv("data/artist_info_oli.csv")


df_ambre_clean <- df_ambre %>% filter(genres != "['No genres available']")
df_arnaud_clean <- df_arnaud %>% filter(genres != "['No genres available']")
df_elwin_clean <- df_elwin %>% filter(genres != "['No genres available']")
df_fan_clean <- df_fan %>% filter(genres != "['No genres available']")
df_oli_clean <- df_oli %>% filter(genres != "['No genres available']") %>% filter(genres != "['Error']")
 

# only one db with all the csv (unique value) called "artistsDB"
artistsDBALL <- bind_rows(df_ambre, df_arnaud, df_elwin, df_fan, df_oli) %>% distinct(name, .keep_all=TRUE)
artistsDB <- bind_rows(df_ambre_clean, df_arnaud_clean, df_elwin_clean, df_fan_clean, df_oli_clean) %>% distinct(name, .keep_all=TRUE)


# Look for the rows on the new db where there is in the column "Related_artists" the value is equal to : "[]" or "no similar artists"

filtered_artistsDB <- artistsDB %>% 
  filter(related_artists %in% c("[]", "No similar artists"))
artistsDB <- artistsDB %>% filter(!(artistsDB$related_artists %in% c("[]", "No similar artists")))
artistsDB <- artistsDB %>% select(-X)


write.csv(artistsDB, "final_data/artists_final.csv", row.names = FALSE)


