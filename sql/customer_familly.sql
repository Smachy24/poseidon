/*
Création de la table Custommer_familly 
*/

CREATE TABLE customer_familly  (
    id VARCHAR(255) PRIMARY KEY,
    code VARCHAR(255) UNIQUE,
    description VARCHAR(255)
);