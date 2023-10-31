CREATE TABLE customer (
   id VARCHAR(255) PRIMARY KEY,
   code VARCHAR(255) UNIQUE,
   nom STRING,
   familly STRING FOREIGN KEY REFERENCES customer_familly(id),
);