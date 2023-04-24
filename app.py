from flask import Flask,request,render_template,jsonify,abort
from flask_cors import CORS
import mysql.connector

#######################
# CONNECT TO DATABASE #
#######################

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="803z"
)

mycursor = mydb.cursor()

##########################
# CREATE DATABASE TABLES #
##########################

# Admin
mycursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
    id_admin INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    pseudo VARCHAR(50) NOT NULL,
    mdp VARCHAR(255) NOT NULL
    )''')
mydb.commit()

# Materiel
mycursor.execute('''CREATE TABLE IF NOT EXISTS Materiel (
    id_materiel INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    type VARCHAR(50) NOT NULL,
    modele VARCHAR(255) NOT NULL,
    description TEXT,
    quantite INT NOT NULL DEFAULT 1,
    image VARCHAR(500),
    remarque TEXT
    )''')
mydb.commit()

# Reservations
mycursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
    id_reservation INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    sortie BIT NOT NULL DEFAULT 0,  
    date_restitution DATE,
    retour_complet BIT NOT NULL DEFAULT 0,
    retour_incomplet BIT NOT NULL DEFAULT 0
    )''')
mydb.commit()

# Contacts
mycursor.execute('''CREATE TABLE IF NOT EXISTS Contacts (
    id_contact INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_reservation INT NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(320) NOT NULL,
    discord varchar(50),
    telephone VARCHAR(10),
    autre TEXT,
    FOREIGN KEY (id_reservation) REFERENCES Reservations(id_reservation)
    )''')
mydb.commit()

# Projets
mycursor.execute('''CREATE TABLE IF NOT EXISTS Projets (
    id_projet INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_reservation INT NOT NULL,
    nom VARCHAR(100),
    description TEXT NOT NULL,
    participants VARCHAR(500),
    FOREIGN KEY (id_reservation) REFERENCES Reservations(id_reservation)
    )''')
mydb.commit()

# Reservations_Material
mycursor.execute('''CREATE TABLE IF NOT EXISTS Reservations_Materiel (
    id_reservation INT NOT NULL,
    id_materiel INT NOT NULL,
    rendu BIT NOT NULL DEFAULT 0,
    manquant BIT NOT NULL DEFAULT 0,
    defaut BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_reservation) REFERENCES Reservations(id_reservation),
    FOREIGN KEY (id_materiel) REFERENCES Materiel(id_materiel)
    )''')
mydb.commit()

mycursor.execute('''select * from Contacts''')
contacts = mycursor.fetchall()
print(contacts)

print('-------------------')
mycursor.execute('''select * from Contacts''')
print(mycursor.fetchone())

for contacts in mycursor:
    print(contacts)

mycursor.close()

app = Flask(__name__)
CORS(app)

print("hello world!")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
