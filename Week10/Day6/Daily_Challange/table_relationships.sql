DROP TABLE IF EXISTS customer_profile;
DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE customer_profile (
    id SERIAL PRIMARY KEY,
    isLoggedIn BOOLEAN DEFAULT false,
    customer_id INTEGER UNIQUE,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

INSERT INTO customer (first_name, last_name)
VALUES
('John', 'Doe'),
('Jerome', 'Lalu'),
('Lea', 'Rive');

INSERT INTO customer_profile (isLoggedIn, customer_id)
VALUES (
    true,
    (SELECT id FROM customer WHERE first_name = 'John')
);

INSERT INTO customer_profile (isLoggedIn, customer_id)
VALUES (
    false,
    (SELECT id FROM customer WHERE first_name = 'Jerome')
);

SELECT customer.first_name
FROM customer
JOIN customer_profile
    ON customer.id = customer_profile.customer_id
WHERE customer_profile.isLoggedIn = true;


DROP TABLE IF EXISTS Book;

CREATE TABLE Book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR (50) NOT NULL,
    author VARCHAR (50) NOT NULL
);

INSERT INTO Book (title, author)
VALUES 
('Alice In Wonderland', 'Lewis Carroll'),
('Harry Potter', 'J.K Rowling'),
('To kill a mockingbird', 'Harper Lee');

SELECT * FROM Book;

CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    age INTEGER CHECK (age <= 15)
);

INSERT INTO Student (name, age)
VALUES 
('John', 12),
('Lera', 11),
('Patrick', 10),
('Bob', 14);

CREATE TABLE Library (
    book_fk_id INTEGER,
    student_fk_id INTEGER,
    borrowed_date DATE,
    FOREIGN KEY (book_fk_id) REFERENCES Book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_fk_id) REFERENCES Student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (book_fk_id, student_fk_id)
);

INSERT INTO Library (book_fk_id, student_fk_id, borrowed_date)
VALUES
(
    (SELECT book_id FROM Book WHERE title = 'Alice In Wonderland'),
    (SELECT student_id FROM Student WHERE name = 'John'),
    '2022-02-15'
),
(
    (SELECT book_id FROM Book WHERE title = 'To kill a mockingbird'),
    (SELECT student_id FROM Student WHERE name = 'Bob'),
    '2021-03-03'
),
(
    (SELECT book_id FROM Book WHERE title = 'Alice In Wonderland'),
    (SELECT student_id FROM Student WHERE name = 'Lera'),
    '2021-05-23'
),
(
    (SELECT book_id FROM Book WHERE title = 'Harry Potter'),
    (SELECT student_id FROM Student WHERE name = 'Bob'),
    '2021-08-12'
);

-- a) Select all columns from the junction table
SELECT * FROM Library;

-- b) Student name and title of borrowed books
SELECT s.name, b.title
FROM Library l
JOIN Student s ON l.student_fk_id = s.student_id
JOIN Book b ON l.book_fk_id = b.book_id;

-- c) Average age of students who borrowed Alice In Wonderland
SELECT AVG(s.age)
FROM Library l
JOIN Student s ON l.student_fk_id = s.student_id
JOIN Book b ON l.book_fk_id = b.book_id
WHERE b.title = 'Alice In Wonderland';

-- d) Delete a student, see what happens in the junction table
DELETE FROM Student WHERE name = 'Bob';
SELECT * FROM Library;-- a) Select all columns from the junction table
SELECT * FROM Library;

-- b) Student name and title of borrowed books
SELECT s.name, b.title
FROM Library l
JOIN Student s ON l.student_fk_id = s.student_id
JOIN Book b ON l.book_fk_id = b.book_id;

-- c) Average age of students who borrowed Alice In Wonderland
SELECT AVG(s.age)
FROM Library l
JOIN Student s ON l.student_fk_id = s.student_id
JOIN Book b ON l.book_fk_id = b.book_id
WHERE b.title = 'Alice In Wonderland';

-- d) Delete a student, see what happens in the junction table
DELETE FROM Student WHERE name = 'Bob';
SELECT * FROM Library;
