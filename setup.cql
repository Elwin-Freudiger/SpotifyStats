// Création des contraintes d'unicité
CREATE CONSTRAINT FOR (a:Artist) REQUIRE a.name IS UNIQUE;
CREATE CONSTRAINT FOR (t:Track) REQUIRE t.name IS UNIQUE;
CREATE CONSTRAINT FOR (al:Album) REQUIRE al.name IS UNIQUE;
CREATE CONSTRAINT FOR (l:Listener) REQUIRE l.name IS UNIQUE;

// Importation des artistes
LOAD CSV WITH HEADERS FROM 'file:///spotify_info.csv' AS row
MERGE (artist:Artist {name: row.artistName})
SET artist.popularity = toInteger(row.artistPop),
    artist.genres = split(row.artistGenre, ', ');

// Importation des albums
LOAD CSV WITH HEADERS FROM 'file:///spotify_info.csv' AS row
MERGE (album:Album {name: row.albumName})
SET album.releaseDate = toInteger(row.releaseDate);

// Importation des pistes
LOAD CSV WITH HEADERS FROM 'file:///spotify_info.csv' AS row
MERGE (track:Track {name: row.trackName})
SET track.popularity = toInteger(row.trackPop),
    track.msPlayed = toInteger(row.msPlayed);

// Création des relations entre pistes et artistes
LOAD CSV WITH HEADERS FROM 'file:///spotify_info.csv' AS row
MATCH (track:Track {name: row.trackName})
MATCH (artist:Artist {name: row.artistName})
MERGE (track)-[:PERFORMED_BY]->(artist);

// Création des relations entre albums et pistes
LOAD CSV WITH HEADERS FROM 'file:///spotify_info.csv' AS row
MATCH (track:Track {name: row.trackName})
MATCH (album:Album {name: row.albumName})
MERGE (album)-[:CONTAINS]->(track);

// Importation des auditeurs et relations avec les pistes
LOAD CSV WITH HEADERS FROM 'file:///spotify_info.csv' AS row
MERGE (listener:Listener {name: row.listener})
WITH listener, row
MATCH (track:Track {name: row.trackName})
MERGE (listener)-[:LISTENS_TO]->(track);

// Création des relations entre artistes similaires
LOAD CSV WITH HEADERS FROM 'file:///spotify_info.csv' AS row
MATCH (artist:Artist {name: row.artistName})
FOREACH (related IN split(row.artistRelated, ', ') |
    MERGE (relatedArtist:Artist {name: related})
    MERGE (artist)-[:RELATED_TO]->(relatedArtist)
);
