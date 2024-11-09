db <- read.csv(here::here("spotify_info_final.csv"))
db <- db %>% select(-Unnamed..0)

library(dplyr)

counts <- db %>% count(artistName)
View(counts)

lana_del_rey_rows <- db %>% filter(artistName == "Lana Del Rey")
View(lana_del_rey_rows)

charlixcx <- db %>% filter(artistName == "Charli xcx")
View(charlixcx)
