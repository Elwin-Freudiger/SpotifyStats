library(tidyverse)

# Define the range of dates
date_range <- seq.Date(as.Date("2023-10-08"), as.Date("2024-10-20"), by = "day")

# Load the datasets
ambre <- read_csv("data/timeserie/Stream_hist_ambre.csv")
arnaud <- read_csv("data/timeserie/Stream_hist_arnaud.csv")
elwin <- read_csv("data/timeserie/Stream_hist_elwin.csv")
fanny <- read_csv("data/timeserie/Stream_hist_fan.csv")
olivier <- read_csv("data/timeserie/Stream_hist_oli.csv")

# Combine listeners into a list
listeners <- list(ambre = ambre, arnaud = arnaud, elwin = elwin, fanny = fanny, olivier = olivier)

# Process each listener
processed_listeners <- listeners %>%
  imap(~ .x %>%
         mutate(day = as.Date(endTime)) %>%            # Extract day
         group_by(day) %>%                             # Group by day
         summarise(msPlayed = sum(msPlayed),           # Sum daily listening time
                   .groups = "drop") %>%
         complete(day = date_range,                   # Fill in all missing days
                  fill = list(msPlayed = 0)) %>%       # Set missing `msPlayed` to 0
         mutate(!! .y := cumsum(msPlayed)) %>%         # Compute cumulative sum
         select(day, !! .y)                           # Keep only day and cumulative sum
  )

ts_spotify <- reduce(processed_listeners, full_join, by = "day") 

ts_long <- ts_spotify %>% pivot_longer(cols= -day,
                                       names_to = "listener",
                                       values_to = "cumsum")


ts_long %>%
  ggplot(aes(x=day,y=cumsum/3.6e+6, color=listener)) +
  geom_line() +
  theme_minimal()+
  labs(title="Evolution of the listening history",
       x="Date",
       y="Listening time (hours)") +
  ylim(c(0,760))