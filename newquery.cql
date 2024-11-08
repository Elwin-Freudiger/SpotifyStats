// most popular artists
MATCH (a:Artist)-[:PERFORMED_BY]-(t:Track)
RETURN a.name AS Artist, AVG(t.popularity) AS AvgPopularity
ORDER BY AvgPopularity DESC
LIMIT 10;

