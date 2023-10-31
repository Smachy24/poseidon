INSERT INTO customer_familly (id, code, description) VALUES
('158c9998-18da-4bef-a8db-4891b1736574', 'ABC123', 'abcdef'),
('158c9998-18da-4bef-a8db-4891b1736575', 'DEF456', 'abcdef'),
('158c9998-18da-4bef-a8db-4891b1736576', 'GHI789', 'abcdef');


INSERT INTO customer (id, code, nom, familly) VALUES
('258c9998-18da-4bef-a8db-4891b1736574', 'ABC124', 'Mathis', 'famille01'),
('258c9998-18da-4bef-a8db-4891b1736575', 'DEF457', 'Diego', 'famille02'),
('258c9998-18da-4bef-a8db-4891b1736576', 'GHI7810', 'Ben Youcef', 'famille03');


INSERT INTO order (id, customer, product, quantity) VALUES
('258c9998-18da-4bef-a8db-5891b1736574', '258c9998-18da-4bef-a8db-4891b1736574', 'ordinateur', 3),
('258c9998-18da-4bef-a8db-5891b1736575', '258c9998-18da-4bef-a8db-4891b1736575', 'vélo', 1),
('258c9998-18da-4bef-a8db-5891b1736576', '258c9998-18da-4bef-a8db-4891b1736576', 'voiture', 1);


INSERT INTO product (id, code, designation) VALUES
('258c9998-18da-4bef-a8db-5899b1736574', 'ABC124897', 'vetement'),
('258c9998-18da-4bef-a8db-5801b1736575', 'ABC1248YI', 'informatique'),
('258c9998-18da-4bef-a8db-4591b1736576', 'ABC12IUI', 'véhicule');
