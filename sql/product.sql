/*
Création de la table Product 
*/

CREATE TABLE product  (
    id VARCHAR(255) PRIMARY KEY,
    code VARCHAR(255) UNIQUE,
    designation VARCHAR(255)
);