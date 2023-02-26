SELECT roadno as name, sum(lengthkm) as length, max(width) AS width
FROM madagascar_roads_version4
GROUP BY roadno
HAVING roadno LIKE '%RNP%';

CREATE VIEW route_nationale AS
SELECT roadno as name, sum(lengthkm) as length, max(width) AS width
FROM madagascar_roads_version4
GROUP BY roadno
HAVING roadno LIKE '%RNP%';

CREATE VIEW route_reparation AS
SELECT r.name, r.length, r.width, b.depart, b.arrive, b.niveau
FROM bad_roads b
    JOIN route_nationale r ON b.roadno=r.name;

SELECT *
FROM route_reparation
WHERE (depart <= 8 AND 8 <= depart) OR (arrive <= 15 AND 15 <= arrive);