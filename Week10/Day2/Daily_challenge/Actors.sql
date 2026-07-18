CREATE TABLE actor (
    actor_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(100),
    age DATE,
    number_oscars SMALLINT
);

INSERT INTO actor (actor_id, first_name, last_name, age, number_oscars)
VALUES
    (1, 'Matt', 'Damon', '1970-08-10', 5),
    (2, 'George', 'Clooney', '1961-06-05', 2),
    (3, 'Angelina', 'Jolie', '1975-06-04', 1),
    (4, 'Jennifer', 'Aniston', '1969-02-11', 0);

SELECT COUNT(*) FROM actor;

INSERT INTO actor (actor_id, first_name)
VALUES (5, 'Chris');

SELECT * FROM actor;
