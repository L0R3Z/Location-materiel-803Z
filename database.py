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
        image VARCHAR(500),
        remarque TEXT,
        archive BIT NOT NULL DEFAULT 0
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
        archive BIT NOT NULL DEFAULT 0
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
        ("john_doe", %s, 0);
        '''
    mycursor.execute(tempQuery, (encrypted_passwd_admin, encrypted_passwd_john))
    mydb.commit()
    
    # Insert sample values in Materiel
    mycursor.execute('''INSERT INTO Materiel(type, modele, description, image, remarque) VALUES
        ("boitier", "Canon cramptes 13", "contre focale triple 57mm", "", "inutilisable"),
        ("trepied", "Trepied 2000", "18m 4 pieds etc.", "https://www.europe-nature-optik.fr/884-tm_thickbox_default/kite-trepied-ardea-cf-avec-rotule-manfrotto-128rc.jpg", ""),
        ("camera", "Canon apagn 8", "focale double 14mm avec lampe frontale", "", ""),
        ("micro", "micro pro 1234", "il est vrmt bien", "", ""), 
        ("boitier", "Canon 550D", "Monture : Canon EF", "", ""), 
        ("boitier", "Canon 5D Mark II", "Monture : Canon EF", "", ""),
        ("boitier", "Canon 6D Mark II", "Monture : Canon EF", "", ""), 
        ("boitier", "Sony A7SII", "Monture : Sony E", "", ""),
        ("boitier", "Kit GOPRO HERO2", "", "", ""),
        ("boitier", "Black Magic Pocket 4k", "Monture : Micro 4/3", "", ""), 
        ("optique", "CANON 2.8/ 16-35mm", "Monture : EF, diamètre : 82", "", ""),
        ("optique", "CANON 3.5-5.6/ 28-80mm", "Monture : EF, diamètre : 58", "", ""), 
        ("accessoire", "Filtre MIST", "", "", ""),
        ("accessoire", "Pare-Soleil SAMYANG", "", "", ""), 
        ("accessoire", "Filtre N/D 100-400", "taille : 82mm", "", ""),
        ("machinerie", "Stabilisateur Smartphone DJI", "", "", ""),
        ("machinerie", "Steadicam MERLIN", "", "", "Manuel / PT"), 
        ("machinerie", "Cross épaule", "", "", "Contre-poid instable, protection décollée, vise manque (au niveau du poid principale), légere tendance à perdre sa poignée.") ;
        ''')
    mydb.commit()
    
    # Insert sample values in Reservations
    mycursor.execute('''INSERT INTO Reservations(date_debut, date_fin, sortie, date_restitution, retour_complet, archive) VALUES
        ("2022-09-30", "2022-10-05", 1, "2022-10-07", 1, 0),
        ("2023-04-24", "2023-12-04", 1, null, 0, 0),
        ("2023-04-25", "2023-04-27", 1, "2023-04-26", 0, 0),
        ("2023-04-26", "2024-01-04", 0, null, 0, 0), 
        ("2023-04-28", "2023-05-01", 1, "2023-05-01", 0, 0),
        ("2023-04-02", "2023-04-15", 1, "2023-04-15", 1, 0);
        ''')
    mydb.commit()
    
    # Insert sample values in Reservations_Materiel
    mycursor.execute('''INSERT INTO Reservations_Materiel(id_reservation, id_materiel, rendu, manquant, defaut) VALUES
        (1, 2, 1, 0, 0),
        (1, 3, 1, 0, 0),
        (2, 2, 1, 0, 0),
        (3, 1, 0, 1, 0),
        (3, 4, 1, 0, 1),
        (4, 2, 0, 0, 0);
        ''')
    mydb.commit()

    # Insert sample values in Projet
    mycursor.execute('''INSERT INTO Projets (id_reservation, nom, description, participants) VALUES 
        (1, "Gamejam shy visuels", "création de visuels pour un jeu créé pendant une gamejam de 45h (gamejam advance)", "Enzo, Sukai, ER, AD"),
        (2, "Title Sequence", "Title sequence filmé + scènes 3D réalisé en 2eme année", "Sukai");
        ''')
    mydb.commit()
    
    # Insert sample values in Contacts
    mycursor.execute('''INSERT INTO Contacts (id_reservation, nom, prenom, email, discord, telephone, autre) VALUES 
        (1, "Bassot", "Enzo", "enzo.bassot@gmail.com", "Mrzozo#4244", "0782836972", "^^"),
        (2, "Huet", "Quentin", "quentinhuet4500@gmail.com", "", "", "")
        ''')
    mydb.commit()
