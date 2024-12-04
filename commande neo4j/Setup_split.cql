// Step 1: Import Tracks, Albums, and link to Artists with release year
LOAD CSV WITH HEADERS FROM 'file:///Tracks.csv' AS row
MERGE (t:Track {
    id: row.trackID, 
    name: row.trackName, 
    release_date: row.releaseDate, 
    popularity: toFloat(row.trackPop)
})
MERGE (a:Artist {name: row.artistName})
MERGE (al:Album {name: row.albumName, release_date: toInteger(row.releaseDate)})
MERGE (year:Year {value: toInteger(row.releaseDate)})  // Create a Year node
MERGE (al)-[:RELEASED_IN]->(year)                     // Link Album to its release year
MERGE (t)-[:PERFORMED_BY]->(a)
MERGE (al)-[:CONTAINS]->(t);

// Step 2: Import Artist details, including genres and related artists
LOAD CSV WITH HEADERS FROM 'file:///Artists.csv' AS row
MERGE (a:Artist {name: row.artistName})
SET a.popularity = toFloat(row.artistPop)

// Split the artistGenre string into individual genres
WITH a, row, split(row.artistGenre, ', ') AS genres
UNWIND genres AS genre
MERGE (g:Genre {name: genre})
MERGE (a)-[:IN_GENRE]->(g)

// After processing genres, continue with related artists
WITH a, row, split(row.artistRelated, ', ') AS related_artists
UNWIND related_artists AS related_artist
MERGE (related:Artist {name: related_artist})
MERGE (a)-[:RELATED_TO]->(related);

// Step 3: Import Listening History and link to Tracks
LOAD CSV WITH HEADERS FROM 'file:///Listening_History.csv' AS row
MATCH (t:Track {id: row.trackID})
MERGE (l:Listener {name: row.listener})
MERGE (l)-[r:LISTENED_TO]->(t)
SET r.msPlayed = toInteger(row.msPlayed);
