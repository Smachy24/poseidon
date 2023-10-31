/*
Création de la table Custommer_familly 
*/
CREATE TABLE customer_familly  (
    id VARCHAR(255) PRIMARY KEY,
    code VARCHAR(255) UNIQUE,
    description VARCHAR(255)
);

/*
Create a table customer
*/
CREATE TABLE customer (
   id VARCHAR(255) PRIMARY KEY,
   code VARCHAR(255) UNIQUE,
   nom STRING,
   familly STRING FOREIGN KEY REFERENCES customer_familly(id),
);

/*
Create a table order
*/
CREATE TABLE order(
    id STRING PRIMARY KEY,
    customer STRING FOREIGN KEY REFERENCES customer(id),
    product STRING,
    quantity INT,
);

/*
Création de la table Product 
*/
CREATE TABLE product  (
    id VARCHAR(255) PRIMARY KEY,
    code VARCHAR(255) UNIQUE,
    designation VARCHAR(255)
);
