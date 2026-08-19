
-- Exercise 1: DVD Rental
-- ============================================================

-- 1. Get a list of all the languages from the language table.
SELECT
    language_id,
    name
FROM language
ORDER BY language_id;


-- 2. Get a list of all films joined with their languages.
-- Details: film title, description, and language name.
SELECT
    f.title,
    f.description,
    l.name AS language_name
FROM film AS f
INNER JOIN language AS l
    ON f.language_id = l.language_id
ORDER BY f.title;


-- 3. Get all languages, even if there are no films in those languages.
-- Details: film title, description, and language name.
SELECT
    f.title,
    f.description,
    l.name AS language_name
FROM language AS l
LEFT JOIN film AS f
    ON l.language_id = f.language_id
ORDER BY l.name, f.title;


-- 4. Create a new table called new_film with columns id and name.
-- Drop first so this solution file can be run more than once.
DROP TABLE IF EXISTS customer_review;
DROP TABLE IF EXISTS new_film;

CREATE TABLE new_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO new_film (name)
VALUES
    ('The SQL Adventure'),
    ('Database Dreams'),
    ('Postgres Nights');

SELECT *
FROM new_film
ORDER BY id;


-- 5. Create a customer_review table.
-- If a film is deleted from new_film, its reviews are deleted automatically
-- because of ON DELETE CASCADE.
CREATE TABLE customer_review (
    review_id SERIAL PRIMARY KEY,
    film_id INTEGER NOT NULL
        REFERENCES new_film(id)
        ON DELETE CASCADE,
    language_id INTEGER NOT NULL
        REFERENCES language(language_id),
    title VARCHAR(255) NOT NULL,
    score INTEGER NOT NULL
        CHECK (score BETWEEN 1 AND 10),
    review_text TEXT NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT NOW()
);


-- 6. Add 2 movie reviews, linked to valid rows in new_film and language.
INSERT INTO customer_review (
    film_id,
    language_id,
    title,
    score,
    review_text
)
VALUES
    (
        1,
        (SELECT language_id FROM language WHERE name = 'English'),
        'Fun database movie',
        8,
        'A creative film with a clear story and a strong ending.'
    ),
    (
        2,
        (SELECT language_id FROM language WHERE name = 'English'),
        'Very original',
        9,
        'The movie was interesting, well paced, and easy to recommend.'
    );

SELECT *
FROM customer_review
ORDER BY review_id;


-- 7. Delete a film that has a review from new_film.
-- Result: the review for this film is automatically deleted from
-- customer_review because the foreign key uses ON DELETE CASCADE.
DELETE FROM new_film
WHERE id = 1;

SELECT *
FROM customer_review
ORDER BY review_id;


-- ============================================================
-- Exercise 2: DVD Rental
-- ============================================================

-- 1. Use UPDATE to change the language of some films.
-- The language IDs are selected from the language table to guarantee
-- that valid language_id values are used.
UPDATE film
SET language_id = (
    SELECT language_id
    FROM language
    WHERE name = 'Italian'
)
WHERE title IN ('ACADEMY DINOSAUR', 'ACE GOLDFINGER');

UPDATE film
SET language_id = (
    SELECT language_id
    FROM language
    WHERE name = 'French'
)
WHERE title IN ('ADAPTATION HOLES', 'AFFAIR PREJUDICE');

SELECT
    f.title,
    l.name AS language_name
FROM film AS f
INNER JOIN language AS l
    ON f.language_id = l.language_id
WHERE f.title IN (
    'ACADEMY DINOSAUR',
    'ACE GOLDFINGER',
    'ADAPTATION HOLES',
    'AFFAIR PREJUDICE'
)
ORDER BY f.title;


-- 2. Which foreign keys are defined for the customer table?
SELECT
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS referenced_table,
    ccu.column_name AS referenced_column
FROM information_schema.table_constraints AS tc
INNER JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
INNER JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
    AND tc.table_name = 'customer'
ORDER BY tc.constraint_name, kcu.ordinal_position;

-- Answer:
-- The customer table has foreign keys on address_id and store_id.
-- This means that when inserting a customer, the address_id must already
-- exist in the address table, and the store_id must already exist in the
-- store table. PostgreSQL will reject an INSERT that references missing rows.


-- 3. Drop the customer_review table.
-- This is easy here because other tables do not depend on customer_review.
-- It still needs checking in real projects, because another table or view
-- could depend on it. In that case, dependent objects must be handled first.
DROP TABLE customer_review;


-- 4. Find out how many rentals are still outstanding.
SELECT
    COUNT(*) AS outstanding_rentals
FROM rental
WHERE return_date IS NULL;


-- 5. Find the 30 most expensive movies which are outstanding.
-- "Most expensive" is interpreted as highest replacement_cost.
SELECT DISTINCT
    f.film_id,
    f.title,
    f.replacement_cost,
    f.rental_rate
FROM film AS f
INNER JOIN inventory AS i
    ON f.film_id = i.film_id
INNER JOIN rental AS r
    ON i.inventory_id = r.inventory_id
WHERE r.return_date IS NULL
ORDER BY f.replacement_cost DESC, f.rental_rate DESC, f.title
LIMIT 30;


-- 6. Help find the 4 movies your friend wants to rent.

-- 6.1 The film is about a sumo wrestler, and one actor is Penelope Monroe.
SELECT DISTINCT
    f.title,
    f.description
FROM film AS f
INNER JOIN film_actor AS fa
    ON f.film_id = fa.film_id
INNER JOIN actor AS a
    ON fa.actor_id = a.actor_id
WHERE f.description ILIKE '%sumo%'
    AND a.first_name = 'PENELOPE'
    AND a.last_name = 'MONROE'
ORDER BY f.title;


-- 6.2 A short documentary, less than 1 hour long, rated R.
SELECT DISTINCT
    f.title,
    f.description,
    f.length,
    f.rating
FROM film AS f
INNER JOIN film_category AS fc
    ON f.film_id = fc.film_id
INNER JOIN category AS c
    ON fc.category_id = c.category_id
WHERE c.name = 'Documentary'
    AND f.length < 60
    AND f.rating = 'R'
ORDER BY f.length, f.title;


-- 6.3 A film Matthew Mahan rented, paid over $4.00 for, and returned
-- between July 28 and August 1, 2005.
SELECT DISTINCT
    f.title,
    f.description,
    p.amount,
    r.return_date
FROM customer AS c
INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
INNER JOIN payment AS p
    ON r.rental_id = p.rental_id
INNER JOIN inventory AS i
    ON r.inventory_id = i.inventory_id
INNER JOIN film AS f
    ON i.film_id = f.film_id
WHERE c.first_name = 'MATTHEW'
    AND c.last_name = 'MAHAN'
    AND p.amount > 4.00
    AND r.return_date >= DATE '2005-07-28'
    AND r.return_date < DATE '2005-08-02'
ORDER BY r.return_date, f.title;


-- 6.4 Matthew Mahan watched this film too. It had "boat" in the title
-- or description, and it was very expensive to replace.
SELECT DISTINCT
    f.title,
    f.description,
    f.replacement_cost
FROM customer AS c
INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
INNER JOIN inventory AS i
    ON r.inventory_id = i.inventory_id
INNER JOIN film AS f
    ON i.film_id = f.film_id
WHERE c.first_name = 'MATTHEW'
    AND c.last_name = 'MAHAN'
    AND (
        f.title ILIKE '%boat%'
        OR f.description ILIKE '%boat%'
    )
ORDER BY f.replacement_cost DESC, f.title
LIMIT 1;
