DROP TABLE IF EXISTS two_sport_medalists;

CREATE TEMP TABLE two_sport_medalists AS
SELECT
    olympics.person.id AS person_id,
    olympics.person.full_name,
    COUNT(DISTINCT olympics.event.sport_id) AS number_of_sports,
    COUNT(*) AS total_medals
FROM olympics.person
INNER JOIN olympics.games_competitor
    ON olympics.person.id = olympics.games_competitor.person_id
INNER JOIN olympics.competitor_event
    ON olympics.games_competitor.id = olympics.competitor_event.competitor_id
INNER JOIN olympics.event
    ON olympics.competitor_event.event_id = olympics.event.id
WHERE olympics.competitor_event.medal_id IN (1, 2, 3)
GROUP BY
    olympics.person.id,
    olympics.person.full_name
HAVING COUNT(DISTINCT olympics.event.sport_id) = 2;

SELECT *
FROM two_sport_medalists
ORDER BY total_medals DESC;

SELECT *
FROM two_sport_medalists
WHERE person_id IN (
    SELECT person_id
    FROM two_sport_medalists
    ORDER BY total_medals DESC, person_id
    LIMIT 3
)
ORDER BY total_medals DESC;


-- Exercise 2 - Task 1

SELECT
    olympics.noc_region.region_name,
    SUM(competitor_best_event.medals_in_event) AS total_medals
FROM (
    SELECT
        ranked_competitor_events.person_id,
        ranked_competitor_events.event_id,
        ranked_competitor_events.medals_in_event
    FROM (
        SELECT
            olympics.games_competitor.person_id,
            olympics.competitor_event.event_id,
            COUNT(*) AS medals_in_event,
            ROW_NUMBER() OVER (
                PARTITION BY olympics.games_competitor.person_id
                ORDER BY
                    COUNT(*) DESC,
                    olympics.competitor_event.event_id
            ) AS event_rank
        FROM olympics.games_competitor
        INNER JOIN olympics.competitor_event
            ON olympics.games_competitor.id =
               olympics.competitor_event.competitor_id
        WHERE olympics.competitor_event.medal_id IN (1, 2, 3)
        GROUP BY
            olympics.games_competitor.person_id,
            olympics.competitor_event.event_id
    ) AS ranked_competitor_events
    WHERE ranked_competitor_events.event_rank = 1
) AS competitor_best_event
INNER JOIN olympics.person_region
    ON competitor_best_event.person_id =
       olympics.person_region.person_id
INNER JOIN olympics.noc_region
    ON olympics.person_region.region_id =
       olympics.noc_region.id
GROUP BY olympics.noc_region.region_name
ORDER BY total_medals DESC
LIMIT 5;


-- Exercise 2 - Task 2

DROP TABLE IF EXISTS frequent_non_medalists;

CREATE TEMP TABLE frequent_non_medalists AS
SELECT
    olympics.person.full_name,
    COUNT(DISTINCT olympics.games_competitor.games_id) AS games_participated
FROM olympics.person
INNER JOIN olympics.games_competitor
    ON olympics.person.id =
       olympics.games_competitor.person_id
WHERE olympics.person.id NOT IN (
    SELECT olympics.games_competitor.person_id
    FROM olympics.games_competitor
    INNER JOIN olympics.competitor_event
        ON olympics.games_competitor.id =
           olympics.competitor_event.competitor_id
    WHERE olympics.competitor_event.medal_id IN (1, 2, 3)
)
GROUP BY
    olympics.person.id,
    olympics.person.full_name
HAVING COUNT(DISTINCT olympics.games_competitor.games_id) > 3;

SELECT *
FROM frequent_non_medalists
ORDER BY games_participated DESC;
