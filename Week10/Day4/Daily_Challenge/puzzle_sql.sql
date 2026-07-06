CREATE TABLE FirstTab (
     id integer, 
     name VARCHAR(10)
);

INSERT INTO FirstTab VALUES
(5,'Pawan'),
(6,'Sharlee'),
(7,'Krish'),
(NULL,'Avtaar');

SELECT * FROM FirstTab;

CREATE TABLE SecondTab (
    id integer 
);

INSERT INTO SecondTab VALUES
(5),
(NULL);

SELECT * FROM SecondTab;

-- Q1
-- Prediction: 0
-- Reason:
-- The inner query returns NULL.
-- So the outer query becomes: id NOT IN (NULL).
-- Since NULL means unknown/missing, no rows pass the WHERE filter.
-- Therefore COUNT(*) returns 0.

SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id NOT IN ( 
    SELECT id 
    FROM SecondTab 
    WHERE id IS NULL 
);

-- Actual output after running: 0

-- Q2
-- Prediction: 2
-- Reason:
-- The inner query returns 5.
-- So the outer query becomes: id NOT IN (5).
-- The rows with id 6 and 7 pass.
-- The NULL id does not pass because NULL is unknown/missing.
-- Therefore COUNT(*) returns 2.

SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id NOT IN ( 
    SELECT id 
    FROM SecondTab 
    WHERE id = 5 
);

-- Actual output after running: 2

-- Q3
-- Prediction: 0
-- Reason:
-- The inner query returns 5 and NULL.
-- So the outer query becomes: id NOT IN (5, NULL).
-- Because the NOT IN list contains NULL, no rows pass the WHERE filter.
-- Therefore COUNT(*) returns 0.

SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id NOT IN ( 
    SELECT id 
    FROM SecondTab 
);

-- Actual output after running: 0

-- Q4
-- Prediction: 2
-- Reason:
-- The inner query returns only 5 because WHERE id IS NOT NULL removes NULL.
-- So the outer query becomes: id NOT IN (5).
-- The rows with id 6 and 7 pass.
-- The NULL id does not pass because NULL is unknown/missing.
-- Therefore COUNT(*) returns 2.

SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id NOT IN ( 
    SELECT id 
    FROM SecondTab 
    WHERE id IS NOT NULL 
);

-- Actual output after running: 2

