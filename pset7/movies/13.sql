SELECT DISTINCT(name) FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON movies.id = stars.movie_id WHERE movies.title IN
(SELECT DISTINCT(title) FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON movies.id = stars.movie_id WHERE stars.person_id IN
(SELECT id FROM people WHERE name = "Kevin Bacon" AND people.birth = 1958)) AND people.name != "Kevin Bacon";
