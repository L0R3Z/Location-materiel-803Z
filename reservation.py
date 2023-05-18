from flask import Flask, Blueprint, jsonify, session, render_template, redirect, url_for, request, current_app
from datetime import datetime, date
from utility import encrypt_password

reservation = Blueprint("reservation", __name__)

# Main route of reservation blueprint
@reservation.route("/")
def index():
    try:
        materiel_list = get_all_materiel_and_dispo()
        return render_template("pages/reservation.html", materiel_list=materiel_list)
    except Exception as e: # If the query fails, render the template with a user-friendly error message
        return render_template("pages/reservation.html", error=str(e))

@reservation.route("/makereservation", methods=["GET", "POST"])
def makereservation():
    try:
        data = request.json
        if data:
            insert_all_data(data)
            return {"message": "Votre réservation a été enregistrée et va être prise en compte par le staff !"}
        else:
            raise Exception("Erreur lors de l'envoi des données")
    except Exception as e:
        print(e)
        return {"error": str(e)}

@reservation.route("/searchmateriel", methods=["GET", "POST"])
def searchmateriel():
    try:
        print("inside searchmateriel")
        data = request.json
        if data:
            materiel = get_searched_materiel(data)
            return {"materiel": materiel}
            # return {"message": "Votre réservation a été enregistrée et va être prise en compte par le staff !"}
        else:
            raise Exception("Erreur lors de l'envoi des données")
    except Exception as e:
        print(e)
        return {"error": str(e)}

# Get all the materiel contained in the Materiel table
def get_all_materiel():
    try:
        mydb = current_app.config['mydb']
        mycursor = mydb.cursor()
        print("inside get_all_materiel  ")
        # For performance and code maintainability reasons, it's better to specify the fields to SELECT rather than using "SELECT *"
        mycursor.execute('''SELECT id_materiel, type, modele, description, image, remarque FROM Materiel
            ORDER BY type, modele
            ''')
        rows = mycursor.fetchall()
        # Convert the returned tuples into a well-organized dict with named properties
        materiel_list = [dict(zip(mycursor.column_names, row)) for row in rows]
        mycursor.close()
        return materiel_list
    except Exception as e: # Raise an exception if the request fails. This allows us to display the error message to the user.
        print(e)
        raise Exception("Erreur : impossible de récupérer la liste de matériel") from e

# Get all the materiel contained in the Materiel table, with its disponibility and its return date
def get_all_materiel_and_dispo():
    try:
        mydb = current_app.config['mydb']
        mycursor = mydb.cursor()
        # For performance and code maintainability reasons, it's better to specify the fields to SELECT rather than using "SELECT *"
        mycursor.execute('''SELECT m.id_materiel, m.type, m.modele, m.description, m.image, m.remarque,
            CASE
                WHEN (
                SELECT COUNT(*)
                FROM Reservations r
                JOIN Reservations_Materiel rm ON r.id_reservation = rm.id_reservation
                WHERE rm.id_materiel = m.id_materiel
                AND (
                    rm.rendu = 0
                    OR rm.manquant = 1
                )
                ) > 0 THEN 0
                ELSE 1
            END AS disponible,
            (
                SELECT MAX(r2.date_fin)
                FROM Reservations r2
                JOIN Reservations_Materiel rm2 ON r2.id_reservation = rm2.id_reservation
                WHERE rm2.id_materiel = m.id_materiel
                AND disponible = 0
                AND retour_complet = 1
                AND r2.date_fin > NOW()
            ) AS date_retour
            FROM Materiel m;
            ''')
        rows = mycursor.fetchall()
        # Convert the returned tuples into a well-organized dict with named properties
        materiel_list = [dict(zip(mycursor.column_names, row)) for row in rows]
        mycursor.close()
        return materiel_list
    except Exception as e: # Raise an exception if the request fails. This allows us to display the error message to the user.
        print(e)
        raise Exception("Erreur: impossible de récupérer la liste de matériel") from e

# Get all the materiel contained in the Materiel table, with some research precisions
def get_searched_materiel(parameters):
    try:
        if parameters["type"] and (parameters["dispo"] or parameters["dispo"]==0):
            mydb = current_app.config['mydb']
            mycursor = mydb.cursor()
            print("inside get_searched_materiel")
            # For performance and code maintainability reasons, it's better to specify the fields to SELECT rather than using "SELECT *"
            tempQuery = '''
            SELECT id_materiel, type, modele, description, image, remarque, disponible, date_retour
            FROM (
                SELECT m.id_materiel, m.type, m.modele, m.description, m.image, m.remarque,
                    CASE
                        WHEN (
                        SELECT COUNT(*)
                        FROM Reservations r
                        JOIN Reservations_Materiel rm ON r.id_reservation = rm.id_reservation
                        WHERE rm.id_materiel = m.id_materiel
                        AND (
                            rm.rendu = 0
                            OR rm.manquant = 1
                        )
                        ) > 0 THEN 0
                        ELSE 1
                    END AS disponible,
                    (
                        SELECT MAX(r2.date_fin)
                        FROM Reservations r2
                        JOIN Reservations_Materiel rm2 ON r2.id_reservation = rm2.id_reservation
                        WHERE rm2.id_materiel = m.id_materiel
                        AND disponible = 0
                        AND retour_complet = 1
                        AND r2.date_fin > NOW()
                    ) AS date_retour
                    FROM Materiel m
                ) AS sub
                WHERE sub.type = %s AND ((%s = 1 AND disponible = 1) OR %s = 0);
                '''
            mycursor.execute(tempQuery, (str(parameters["type"]), str(parameters["dispo"]), str(parameters["dispo"])))
            print("Recherche effectuée avec succès!")
            rows = mycursor.fetchall()
            # Convert the returned tuples into a well-organized dict with named properties
            materiel_list = [dict(zip(mycursor.column_names, row)) for row in rows]
            mycursor.close()
            return materiel_list
        else:
            raise Exception("Erreur : l'un des paramètres de recherche n'est pas correctement renseigné")
    except Exception as e: # Raise an exception if the request fails. This allows us to display the error message to the user.
        print(e)
        raise Exception(e)

# A FINIR / OPTIMISER / FACTORISER !!!
def insert_all_data(data):
    mydb = current_app.config['mydb']
    mycursor = mydb.cursor()
    # Start the transaction
    mycursor.execute("START TRANSACTION")
    try:
        # We insert all the 
        insert_reservation(mycursor, data["dates"])
        reservation_id = mycursor.lastrowid
        insert_reservation_materiel(mycursor, data["materiel"], reservation_id)
        insert_contacts(mycursor, data["contacts"], reservation_id)
        insert_projet(mycursor, data["projet"], reservation_id)
        mydb.commit()
        mycursor.close()
        return {"message": "Réservation effectuée !"}
    except Exception as e:
        # Revert all the insertions
        mydb.rollback()
        mycursor.close()
        raise Exception(e)

# Check and insert the data into the Reservations table
def insert_reservation(mycursor, dates):
    # Vérifier si dates.debut et dates.fin ont été renseignés
    if dates["debut"] and dates["fin"]:
        # Vérifier si dates.debut est au moins supérieure ou égale à la date du jour
        debut = datetime.strptime(dates["debut"], "%Y-%m-%d").date()
        if debut >= date.today():
            # Vérifier si dates.fin est au moins supérieure ou égale à dates.debut
            fin = datetime.strptime(dates["fin"], "%Y-%m-%d").date()
            if fin >= debut:
                try:
                    tempQuery = '''INSERT INTO Reservations(date_debut, date_fin) VALUES
                        (%s, %s)'''
                    mycursor.execute(tempQuery, (str(dates["debut"]), str(dates["fin"])))
                    print("réservation insérée avec succès!")
                except Exception as e:
                    print(e)
                    raise Exception("Erreur lors de l'insertion de la réservation") from e
            else:
                raise Exception("Erreur : la date de fin doit être égale ou supérieure à la date de début")
        else:
            raise Exception("Erreur : la date de début doit être égale ou supérieure à la date du jour")
    else:
        raise Exception("Erreur : les dates ne sont pas indiquées")
    
# Check and insert the data into the Reservations_Materiel table
def insert_reservation_materiel(mycursor, materiel, reservation_id):
    # Check if at least one piece of materiel is selected
    if len(materiel) > 0:
        # Insert the reservations_materiel for each piece of equipment
        for matos in materiel:
            # CHECK IF MATOS IS AVAILABLE!!!!!!
            # ...
            try:
                tempQuery = '''INSERT INTO Reservations_Materiel(id_reservation, id_materiel)
                VALUES (%s, %s)'''
                mycursor.execute(tempQuery, (reservation_id, matos))
                print("matériel de réservation inséré avec succès!")
            except Exception as e:
                print(e)
                raise Exception("Erreur lors de l'insertion du matériel à réserver") from e
    else:
        raise Exception("Erreur : aucun matériel n'a été sélectionné")
    
# Check and insert the data into the Contacts table
def insert_contacts(mycursor, contacts, reservation_id):
    # Check if there is at least one contact
    if len(contacts) > 0:
        # For each contact, check if all the informations are here
        for contact in contacts:
            # Check if the essential fields are provided
            if contact["nom"] and contact["prenom"] and contact["email"]:
                try:
                    tempQuery = '''INSERT INTO Contacts(id_reservation, nom, prenom, email, discord, telephone, autre)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                    mycursor.execute(tempQuery, (reservation_id, str(contact["nom"]), str(contact["prenom"]), str(contact["email"]), str(contact["discord"]), str(contact["telephone"]), str(contact["autre"])))
                    print("contacts insérés avec succès!")
                except Exception as e:
                    print(e)
                    raise Exception("Erreur lors de l'insertion des contacts") from e
            else:
                raise Exception("Erreur : des informations sont manquantes sur au moins un contact")
    else:
        raise Exception("Erreur : merci de renseigner au minimum un contact")
    

# Check and insert the data into the Projet table
def insert_projet(mycursor, projet, reservation_id):
    # Vérifier si le projet a été renseigné par l'utilisateur
    if projet["nom"] or projet["description"] or projet["participants"]:
        # Vérifier si la description est renseignée
        if projet["description"]:
            try:
                tempQuery = '''INSERT INTO Projets(id_reservation, nom, description, participants)
                    VALUES (%s, %s, %s, %s)'''
                mycursor.execute(tempQuery, (reservation_id, str(projet["nom"]), str(projet["description"]), str(projet["participants"])))
                print("projet inséré avec succès!")
            except Exception as e:
                print(e)
                raise Exception("Erreur lors de l'insertion du projet") from e
        else:
            raise Exception("Erreur : pour indiquer un projet, il faut au minimum renseigner sa description")

# Pertinence/cohérence de la propriété quantité, puisqu'on gère le matériel à l'unité et au cas par cas (pour indiquer s'il a été emprunté, ajouter des remarques...) ?
# Je pense qu'il serait plus judicieux de retirer cette propriété de la table Materiel.