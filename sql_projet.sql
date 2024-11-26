DROP TABLE IF EXISTS Achat, Pompe, Intervention, Modele, Client;

CREATE TABLE Client(
   id_client INT AUTO_INCREMENT,
   nom_client VARCHAR(50),
   prenom_client VARCHAR(50),
   adresse VARCHAR(50), -- ville/id ville
   telephone VARCHAR(50),
   adresse_mail VARCHAR(50),
   id_client_1 INT,
   PRIMARY KEY(id_client),
   FOREIGN KEY(id_client_1) REFERENCES Client(id_client)
);

CREATE TABLE Modele(
   id_modele INT AUTO_INCREMENT,
   nom_modele VARCHAR(50),
   caracteristique VARCHAR(50),
   PRIMARY KEY(id_modele)
);

CREATE TABLE Pompe(
   numero_pompe INT AUTO_INCREMENT,
   poids INT,
   puissance INT,
   prix INT,
   id_modele INT NOT NULL,
   date_creaton DATE NOT NULL,
   PRIMARY KEY(numero_pompe),
   FOREIGN KEY(id_modele) REFERENCES Modele(id_modele)
);

CREATE TABLE Intervention(
   id_intervention INT AUTO_INCREMENT,
   date_intervention DATE,
   descriptif_intervention VARCHAR(50),
   numero_pompe INT NOT NULL,
   id_client INT NOT NULL,
   duree INT NOT NULL,
   PRIMARY KEY(id_intervention),
   FOREIGN KEY(numero_pompe) REFERENCES Pompe(numero_pompe),
   FOREIGN KEY(id_client) REFERENCES Client(id_client)
);

CREATE TABLE Achat(
   id_achat INT AUTO_INCREMENT,
   date_achat DATE,
   date_installation VARCHAR(50),
   id_client INT NOT NULL, -- prix achat
   numero_pompe INT NOT NULL,
   PRIMARY KEY(id_achat),
   FOREIGN KEY(id_client) REFERENCES Client(id_client),
   FOREIGN KEY(numero_pompe) REFERENCES Pompe(numero_pompe)
);


INSERT INTO Client (id_client, nom_client, prenom_client, adresse, telephone, adresse_mail, id_client_1) VALUES
(1, 'Dupont', 'Jean', '123 Rue Principale', '0601020304', 'jean.dupont@example.com', NULL),
(2, 'Martin', 'Marie', '456 Avenue des Champs', '0605060708', 'marie.martin@example.com', 1),
(3, 'Durand', 'Pierre', '789 Boulevard Central', '0611223344', 'pierre.durand@example.com', NULL),
(4, 'Bernard', 'Sophie', '10 Rue de la Gare', '0622334455', 'sophie.bernard@example.com', 3),
(5, 'Lefevre', 'Luc', '22 Rue des Lilas', '0633445566', 'luc.lefevre@example.com', NULL);

INSERT INTO Modele (id_modele, nom_modele, caracteristique) VALUES
(1, 'Pompe-X1', 'Pompe à haute pression'),
(2, 'Pompe-Y2', 'Pompe à débit rapide'),
(3, 'Pompe-Z3', 'Pompe à faible consommation'),
(4, 'Pompe-A1', 'Pompe industrielle'),
(5, 'Pompe-B2', 'Pompe pour usage domestique');

INSERT INTO Pompe (numero_pompe, poids, puissance, prix, id_modele, date_creaton) VALUES
(1, 200, 300, 2100, 1, '2023-01-01'),
(2, 220, 320, 1600, 2, '2023-02-01'),
(3, 250, 350, 2800, 3, '2023-03-01'),
(4, 230, 340, 2300, 4, '2023-04-01'),
(5, 240, 360, 2400, 5, '2023-05-01');

INSERT INTO Intervention (id_intervention, date_intervention, descriptif_intervention, numero_pompe, id_client, duree) VALUES
(1, '2023-01-15', 'Réparation du moteur', 1, 1, 120),
(2, '2023-02-10', 'Changement de filtre', 2, 2, 60),
(3, '2023-03-05', 'Maintenance générale', 3, 5, 180),
(4, '2023-04-12', 'Réglage de pression', 4, 4, 90),
(5, '2023-05-18', 'Révision annuelle', 5, 5, 240);

INSERT INTO Achat (id_achat, date_achat, date_installation, id_client, numero_pompe) VALUES
(1, '2023-01-01', '2023-01-10', 1, 1),
(2, '2023-02-02', '2023-02-12', 2, 2),
(3, '2023-03-03', '2023-03-13', 3, 3),
(4, '2023-04-04', '2023-04-14', 4, 4),
(5, '2023-05-05', '2023-05-15', 5, 5),
(6, '2023-06-10', '2023-06-15', 1, 2),
(7, '2023-07-05', '2023-07-12', 2, 1),
(8, '2023-08-20', '2023-08-25', 3, 3),
(9, '2023-09-15', '2023-09-18', 4, 2),
(10, '2023-10-10', '2023-10-20', 5, 1);

