CREATE TABLE order(
    id STRING PRIMARY KEY,
    customer STRING FOREIGN KEY REFERENCES customer(id),
    product STRING,
    quantity INT,
);
