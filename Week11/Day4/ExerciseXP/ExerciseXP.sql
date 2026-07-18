-- ==========================================
-- Exercise 1 — Task 1: Rank Movies by Popularity within Each Genre
-- ==========================================

SELECT
    g.genre_name,
    m.title,
    m.popularity,
    RANK() OVER (
        PARTITION BY g.genre_name
        ORDER BY m.popularity DESC
    ) AS popularity_rank
FROM movies.movie m
JOIN movies.movie_genres mg
    ON m.movie_id = mg.movie_id
JOIN movies.genre g
    ON mg.genre_id = g.genre_id
ORDER BY g.genre_name, popularity_rank;


-- ==========================================
-- Exercise 1 — Task 2: Revenue Quartiles by Production Company
-- ==========================================

SELECT
    pc.company_name,
    m.title,
    m.revenue,
    NTILE(4) OVER (
        PARTITION BY pc.company_name
        ORDER BY m.revenue DESC
    ) AS revenue_quartile
FROM movies.movie m
JOIN movies.movie_company mcomp
    ON m.movie_id = mcomp.movie_id
JOIN movies.production_company pc
    ON mcomp.company_id = pc.company_id
ORDER BY pc.company_name, revenue_quartile;


-- ==========================================
-- Exercise 1 — Task 3: Running Total of Budgets by Genre
-- ==========================================

SELECT
    g.genre_name,
    m.title,
    m.budget,
    SUM(m.budget) OVER (
        PARTITION BY g.genre_name
        ORDER BY m.release_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_budget
FROM movies.movie m
JOIN movies.movie_genres mg
    ON m.movie_id = mg.movie_id
JOIN movies.genre g
    ON mg.genre_id = g.genre_id
ORDER BY g.genre_name, m.release_date;


-- ==========================================
-- Exercise 1 — Task 4: Most Recent Movie per Genre
-- ==========================================

SELECT DISTINCT
    g.genre_name,
    FIRST_VALUE(m.title) OVER (
        PARTITION BY g.genre_name
        ORDER BY m.release_date DESC
    ) AS most_recent_movie,
    FIRST_VALUE(m.release_date) OVER (
        PARTITION BY g.genre_name
        ORDER BY m.release_date DESC
    ) AS most_recent_release_date
FROM movies.movie m
JOIN movies.movie_genres mg
    ON m.movie_id = mg.movie_id
JOIN movies.genre g
    ON mg.genre_id = g.genre_id
ORDER BY g.genre_name;


-- ==========================================
-- Exercise 2 — Task 1: Rank Actors by Movie Appearances
-- ==========================================

WITH actor_counts AS (
    SELECT
        p.person_name,
        COUNT(mc.movie_id) AS movie_count
    FROM movies.person p
    JOIN movies.movie_cast mc
        ON p.person_id = mc.person_id
    GROUP BY p.person_name
)

SELECT
    person_name,
    movie_count,
    DENSE_RANK() OVER (
        ORDER BY movie_count DESC
    ) AS actor_rank
FROM actor_counts
ORDER BY actor_rank;


-- ==========================================
-- Exercise 2 — Task 2: Director with Highest Average Rating
-- ==========================================

WITH director_ratings AS (
    SELECT
        p.person_name AS director_name,
        AVG(m.vote_average) AS avg_rating
    FROM movies.person p
    JOIN movies.movie_crew mcr
        ON p.person_id = mcr.person_id
    JOIN movies.movie m
        ON mcr.movie_id = m.movie_id
    WHERE mcr.job = 'Director'
    GROUP BY p.person_name
),
ranked_directors AS (
    SELECT
        director_name,
        avg_rating,
        RANK() OVER (
            ORDER BY avg_rating DESC
        ) AS rating_rank
    FROM director_ratings
)

SELECT
    director_name,
    avg_rating
FROM ranked_directors
WHERE rating_rank = 1;


-- ==========================================
-- Exercise 2 — Task 3: Cumulative Revenue per Actor
-- ==========================================

SELECT
    p.person_name,
    SUM(m.revenue) AS cumulative_revenue
FROM movies.person p
JOIN movies.movie_cast mc
    ON p.person_id = mc.person_id
JOIN movies.movie m
    ON mc.movie_id = m.movie_id
GROUP BY p.person_name
ORDER BY cumulative_revenue DESC;


-- ==========================================
-- Exercise 2 — Task 4: Director with Highest Total Budget
-- ==========================================

WITH director_budgets AS (
    SELECT
        p.person_name AS director_name,
        SUM(m.budget) AS total_budget
    FROM movies.person p
    JOIN movies.movie_crew mcr
        ON p.person_id = mcr.person_id
    JOIN movies.movie m
        ON mcr.movie_id = m.movie_id
    WHERE mcr.job = 'Director'
    GROUP BY p.person_name
),
ranked_budgets AS (
    SELECT
        director_name,
        total_budget,
        RANK() OVER (
            ORDER BY total_budget DESC
        ) AS budget_rank
    FROM director_budgets
)

SELECT
    director_name,
    total_budget
FROM ranked_budgets
WHERE budget_rank = 1;
