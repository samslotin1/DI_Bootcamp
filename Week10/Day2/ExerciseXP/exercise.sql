CREATE DATABASE public;

CREATE TABLE items (
    id INTEGER,
    item_name VARCHAR(100),
    price INTEGER
);

INSERT INTO items (id, item_name, price)
VALUES
(1, 'Small Desk', 100),
(2, 'Large Desk', 300),
(3, 'Fan', 80);

CREATE TABLE customers (
    id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100)
);

INSERT INTO customers (id, first_name, last_name)
VALUES
(1, 'Greg', 'Jones'),
(2, 'Sandra', 'Jones'),
(3, 'Scott', 'Scott'),
(4, 'Trevor', 'Green'),
(5, 'Melanie', 'Johnson');

SELECT * FROM items;

SELECT * FROM items
WHERE price > 80;

SELECT * FROM items
WHERE price <= 300;

SELECT * FROM customers
WHERE last_name = 'Smith';

SELECT * FROM customers
WHERE last_name = 'Jones';

SELECT * FROM customers
WHERE first_name <> 'Scott';
