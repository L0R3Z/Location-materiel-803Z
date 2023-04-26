from utility import encrypt_password
import mysql.connector

# Values to modify according to your configuration!
# Should move this to a .env file
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "name": "803z"
}

# Enable connection to the database
def connect_db():
    return mysql.connector.connect(
        host = db_config["host"],
        user = db_config["user"],
        password = db_config["passwd"],
        database = db_config["name"],
    )

# Close the connection to the database (for when the app shuts down)
# @app.teardown_appcontext
def close_db(db):
    db.close()

# Create database tables
def create_tables(mydb, mycursor):
    # Admin
    mycursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
        id_admin INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        pseudo VARCHAR(50) NOT NULL,
        mdp VARCHAR(64) NOT NULL,
        superuser BIT NOT NULL DEFAULT 0
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

# Insert all sample values
def insert_basic_datas(mydb, mycursor):
    # Insert sample values in Admin
    encrypted_passwd_admin = encrypt_password("admin")
    encrypted_passwd_john = encrypt_password("mypassword")
    # Using Flask placeholders prevents SQL injection attacks by automatically sanitizing and escaping the values
    tempQuery = '''INSERT INTO Admin(pseudo, mdp, superuser) VALUES
        ("admin", %s, 1),
        ("john_doe", %s, 0)
        '''
    mycursor.execute(tempQuery, (encrypted_passwd_admin, encrypted_passwd_john))
    mydb.commit()
    
    # Insert sample values in Materiel
    mycursor.execute('''INSERT INTO Materiel(type, modele, description, quantite, image, remarque) VALUES
        ("camera", "Canon cramptes 13", "contre focale triple 57mm", 1, "", "inutilisable"),
        ("trepied", "Trepied 2000", "18m 4 pieds etc.", 1, "https://www.europe-nature-optik.fr/884-tm_thickbox_default/kite-trepied-ardea-cf-avec-rotule-manfrotto-128rc.jpg", ""),
        ("camera", "Canon apagn 8", "focale double 14mm avec lampe frontale", 2, "", ""),
        ("micro", "micro pro 1234", "il est vrmt bien", 0, "", ""),
        ''')
    mydb.commit()



# mycursor.execute('''select * from Contacts''')
# contacts = mycursor.fetchall()
# print(contacts)

# print('-------------------')
# mycursor.execute('''select * from Contacts''')
# print(mycursor.fetchone())

# for contacts in mycursor:
#     print(contacts)