-- Exercise 1, Task 1: Average age by medal type using correlated subquery

SELECT
    m.medal_name,
    AVG(gc.age) AS average_age
FROM competitor_event AS ce
JOIN medal AS m
    ON ce.medal_id = m.id
JOIN games_competitor AS gc
    ON ce.competitor_id = gc.id
WHERE m.medal_name != 'NA'
  AND gc.age IS NOT NULL
  AND EXISTS (
      SELECT 1
      FROM competitor_event AS ce2
      JOIN medal AS m2
          ON ce2.medal_id = m2.id
      WHERE ce2.competitor_id = gc.id
        AND m2.medal_name != 'NA'
  )
GROUP BY m.medal_name;


-- Exercise 1, Task 2:
-- Top 5 regions with the highest number of unique competitors
-- who participated in more than 3 different events.

SELECT
    nr.region_name,
    COUNT(DISTINCT pr.person_id) AS unique_competitors
FROM person_region AS pr
JOIN noc_region AS nr
    ON pr.region_id = nr.id
WHERE pr.person_id IN (
    SELECT person_id
    FROM (
        SELECT
            gc.person_id,
            COUNT(DISTINCT ce.event_id) AS event_count
        FROM games_competitor AS gc
        JOIN competitor_event AS ce
            ON gc.id = ce.competitor_id
        GROUP BY gc.person_id
        HAVING COUNT(DISTINCT ce.event_id) > 3
    ) AS event_counts
)
GROUP BY nr.region_name
ORDER BY unique_competitors DESC
LIMIT 5;

-- Exercise 1, Task 3:
-- Create a temporary table that stores total medals per competitor,
-- keeping only competitors with more than 2 medals.

CREATE TEMP TABLE competitor_medals AS
SELECT
    gc.person_id,
    COUNT(*) AS total_medals
FROM games_competitor AS gc
JOIN competitor_event AS ce
    ON gc.id = ce.competitor_id
JOIN medal AS m
    ON ce.medal_id = m.id
WHERE m.medal_name != 'NA'
GROUP BY gc.person_id
HAVING COUNT(*) > 2;

-- Check the temporary table
SELECT *
FROM competitor_medals
LIMIT 10;


-- Exercise 1, Task 4:
-- Create a temporary table for analysis, then delete competitors
-- who have not won any real medal.

DROP TABLE IF EXISTS competitor_analysis;

CREATE TEMP TABLE competitor_analysis AS
SELECT DISTINCT
    p.id AS person_id,
    p.full_name
FROM person AS p;

DELETE FROM competitor_analysis
WHERE NOT EXISTS (
    SELECT 1
    FROM games_competitor AS gc
    JOIN competitor_event AS ce
        ON gc.id = ce.competitor_id
    JOIN medal AS m
        ON ce.medal_id = m.id
    WHERE gc.person_id = competitor_analysis.person_id
      AND m.medal_name != 'NA'
);

-- Check remaining competitors
SELECT *
FROM competitor_analysis
LIMIT 10;

-- Exercise 2, Task 1:
-- Update missing competitor heights using the average height
-- of competitors from the same region.
-- We use a temporary table so we do not edit the original person table.

DROP TABLE IF EXISTS person_height_practice;

CREATE TEMP TABLE person_height_practice AS
SELECT
    p.id,
    p.full_name,
    p.height,
    nr.region_name
FROM person AS p
JOIN person_region AS pr
    ON p.id = pr.person_id
JOIN noc_region AS nr
    ON pr.region_id = nr.id;

UPDATE person_height_practice
SET height = (
    SELECT AVG(inner_table.height)
    FROM person_height_practice AS inner_table
    WHERE inner_table.region_name = person_height_practice.region_name
      AND inner_table.height > 0
)
WHERE height = 0;

-- Check updated rows
SELECT *
FROM person_height_practice
WHERE id IN (3, 4, 10, 15);

-- Exercise 2, Task 2:
-- Insert competitors who participated in more than one event
-- in the same Games into a temporary table.

DROP TABLE IF EXISTS multi_event_competitors;

CREATE TEMP TABLE multi_event_competitors (
    person_id INTEGER,
    full_name TEXT,
    games_name TEXT,
    total_events INTEGER
);

INSERT INTO multi_event_competitors
SELECT
    p.id AS person_id,
    p.full_name,
    event_counts.games_name,
    event_counts.total_events
FROM person AS p
JOIN (
    SELECT
        gc.person_id,
        g.games_name,
        COUNT(DISTINCT ce.event_id) AS total_events
    FROM games_competitor AS gc
    JOIN games AS g
        ON gc.games_id = g.id
    JOIN competitor_event AS ce
        ON gc.id = ce.competitor_id
    GROUP BY gc.person_id, g.games_name
    HAVING COUNT(DISTINCT ce.event_id) > 1
) AS event_counts
    ON p.id = event_counts.person_id;

-- Check result
SELECT *
FROM multi_event_competitors
LIMIT 10;

-- Exercise 2, Task 3:
-- Identify regions where the average number of medals won per competitor
-- is greater than the overall average medals per competitor.

SELECT
    region_name,
    AVG(total_medals) AS avg_medals_per_competitor
FROM (
    SELECT
        nr.region_name,
        p.id AS person_id,
        COUNT(
            CASE
                WHEN m.medal_name != 'NA' THEN 1
            END
        ) AS total_medals
    FROM person AS p
    JOIN person_region AS pr
        ON p.id = pr.person_id
    JOIN noc_region AS nr
        ON pr.region_id = nr.id
    LEFT JOIN games_competitor AS gc
        ON p.id = gc.person_id
    LEFT JOIN competitor_event AS ce
        ON gc.id = ce.competitor_id
    LEFT JOIN medal AS m
        ON ce.medal_id = m.id
    GROUP BY nr.region_name, p.id
) AS regional_medals
GROUP BY region_name
HAVING AVG(total_medals) > (
    SELECT AVG(total_medals)
    FROM (
        SELECT
            p.id AS person_id,
            COUNT(
                CASE
                    WHEN m.medal_name != 'NA' THEN 1
                END
            ) AS total_medals
        FROM person AS p
        LEFT JOIN games_competitor AS gc
            ON p.id = gc.person_id
        LEFT JOIN competitor_event AS ce
            ON gc.id = ce.competitor_id
        LEFT JOIN medal AS m
            ON ce.medal_id = m.id
        GROUP BY p.id
    ) AS overall_medals
)
ORDER BY avg_medals_per_competitor DESC;

-- Exercise 2, Task 4:
-- Create a temporary table to track competitors who participated
-- in both Summer and Winter Games.

DROP TABLE IF EXISTS both_seasons_competitors;

CREATE TEMP TABLE both_seasons_competitors AS
SELECT
    p.id AS person_id,
    p.full_name,
    COUNT(DISTINCT g.season) AS seasons_participated
FROM person AS p
JOIN games_competitor AS gc
    ON p.id = gc.person_id
JOIN games AS g
    ON gc.games_id = g.id
GROUP BY p.id, p.full_name
HAVING COUNT(DISTINCT g.season) = 2;

-- Check result
SELECT *
FROM both_seasons_competitors
LIMIT 10;
