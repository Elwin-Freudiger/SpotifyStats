MATCH (listener:Listener {name: 'Ambre'})-[:LISTENS_TO]->(track:Track)-[:PERFORMED_BY]->(artist:Artist)-[:RELATED_TO]->(related:Artist)
RETURN DISTINCT related.name AS RelatedArtists;

MATCH (album:Album {name: 'Feu'})-[:CONTAINS]->(track:Track)
RETURN track.name AS TrackName, track.popularity AS Popularity
ORDER BY track.popularity DESC;

MATCH (listener:Listener {name: 'Ambre'})-[:LISTENS_TO]->(track:Track)-[:PERFORMED_BY]->(artist:Artist)
UNWIND artist.genres AS genre
RETURN genre, COUNT(*) AS Frequency
ORDER BY Frequency DESC;

MATCH (artist:Artist)
RETURN artist.name AS ArtistName, artist.popularity AS Popularity
ORDER BY artist.popularity DESC LIMIT 10;

MATCH (listener1:Listener)-[:LISTENS_TO]->(track:Track)-[:PERFORMED_BY]->(artist:Artist)<-[:PERFORMED_BY]-(track2:Track)<-[:LISTENS_TO]-(listener2:Listener)
WHERE listener1 <> listener2
RETURN listener1.name AS Listener1, listener2.name AS Listener2, artist.name AS SharedArtist, COUNT(track) AS CommonTracks
ORDER BY CommonTracks DESC;

MATCH (target:Listener {name: 'Ambre'})-[:LISTENS_TO]->(:Track)-[:PERFORMED_BY]->(artist:Artist)
WITH target, COLLECT(artist) AS knownArtists

MATCH (similarListener:Listener)-[:LISTENS_TO]->(track:Track)-[:PERFORMED_BY]->(artist:Artist)
WHERE similarListener <> target AND NOT artist IN knownArtists
RETURN artist.name AS RecommendedArtist, COUNT(similarListener) AS PopularityAmongSimilarListeners
ORDER BY PopularityAmongSimilarListeners DESC;

MATCH (listener:Listener)-[:LISTENS_TO]->(:Track)-[:PERFORMED_BY]->(artist:Artist)
UNWIND artist.genres AS genre
WITH listener, genre
MATCH (listener2:Listener)-[:LISTENS_TO]->(:Track)-[:PERFORMED_BY]->(artist2:Artist)
WHERE genre IN artist2.genres AND listener <> listener2
RETURN listener.name AS Listener1, listener2.name AS Listener2, genre AS SharedGenre
ORDER BY SharedGenre;   