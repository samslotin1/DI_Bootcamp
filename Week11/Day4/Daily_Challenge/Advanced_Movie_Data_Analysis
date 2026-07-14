Task 1 — Average budget growth by production company
WITH company_movies AS (
    SELECT
        pc.company_id,
        pc.company_name,
        m.movie_id,
        m.title,
        m.release_date,
        m.budget,
        LAG(m.budget) OVER (
            PARTITION BY pc.company_id
            ORDER BY m.release_date, m.movie_id
        ) AS previous_budget
    FROM movies.movie AS m
    JOIN movies.movie_company AS mc
        ON m.movie_id = mc.movie_id
    JOIN movies.production_company AS pc
        ON mc.company_id = pc.company_id
    WHERE m.budget > 0
      AND m.release_date IS NOT NULL
),
growth_rates AS (
    SELECT
        company_id,
        company_name,
        movie_id,
        title,
        budget,
        previous_budget,
        (budget - previous_budget) * 100.0
            / NULLIF(previous_budget, 0) AS budget_growth_rate
    FROM company_movies
)
SELECT
    company_id,
    company_name,
    ROUND(AVG(budget_growth_rate), 2) AS average_budget_growth_rate_percent
FROM growth_rates
WHERE previous_budget IS NOT NULL
GROUP BY company_id, company_name
ORDER BY average_budget_growth_rate_percent DESC;
Task 2 — Actor with the most above-average-rated movies
WITH rated_movies AS (
    SELECT
        movie_id,
        title,
        vote_average,
        AVG(vote_average) OVER () AS overall_average_rating
    FROM movies.movie
    WHERE vote_average IS NOT NULL
),
actor_counts AS (
    SELECT
        p.person_id,
        p.person_name,
        COUNT(DISTINCT rm.movie_id) AS high_rated_movie_count
    FROM rated_movies AS rm
    JOIN movies.movie_cast AS mc
        ON rm.movie_id = mc.movie_id
    JOIN movies.person AS p
        ON mc.person_id = p.person_id
    WHERE rm.vote_average > rm.overall_average_rating
    GROUP BY p.person_id, p.person_name
),
ranked_actors AS (
    SELECT
        person_id,
        person_name,
        high_rated_movie_count,
        DENSE_RANK() OVER (
            ORDER BY high_rated_movie_count DESC
        ) AS actor_rank
    FROM actor_counts
)
SELECT
    person_id,
    person_name,
    high_rated_movie_count
FROM ranked_actors
WHERE actor_rank = 1;
Task 3 — Rolling three-movie average revenue by genre
SELECT
    g.genre_name,
    m.movie_id,
    m.title,
    m.release_date,
    m.revenue,
    ROUND(
        AVG(m.revenue) OVER (
            PARTITION BY g.genre_id
            ORDER BY m.release_date, m.movie_id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS rolling_average_revenue
FROM movies.movie AS m
JOIN movies.movie_genres AS mg
    ON m.movie_id = mg.movie_id
JOIN movies.genre AS g
    ON mg.genre_id = g.genre_id
WHERE m.revenue IS NOT NULL
  AND m.release_date IS NOT NULL
ORDER BY g.genre_name, m.release_date, m.movie_id;
Task 4 — Highest-grossing keyword-based movie series
WITH keyword_movies AS (
    SELECT
        k.keyword_id,
        k.keyword_name,
        m.movie_id,
        m.title,
        COALESCE(m.revenue, 0) AS revenue
    FROM movies.movie AS m
    JOIN movies.movie_keywords AS mk
        ON m.movie_id = mk.movie_id
    JOIN movies.keyword AS k
        ON mk.keyword_id = k.keyword_id
),
series_totals AS (
    SELECT
        keyword_id,
        keyword_name,
        COUNT(*) OVER (
            PARTITION BY keyword_id
        ) AS movie_count,
        SUM(revenue) OVER (
            PARTITION BY keyword_id
        ) AS total_revenue
    FROM keyword_movies
),
unique_series AS (
    SELECT DISTINCT
        keyword_id,
        keyword_name,
        movie_count,
        total_revenue
    FROM series_totals
    WHERE movie_count >= 2
),
ranked_series AS (
    SELECT
        keyword_id,
        keyword_name,
        movie_count,
        total_revenue,
        DENSE_RANK() OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM unique_series
)
SELECT
    keyword_id,
    keyword_name AS series_keyword,
    movie_count,
    total_revenue
FROM ranked_series
WHERE revenue_rank = 1;
