from flask import Flask, Blueprint, jsonify, session, render_template, redirect, url_for, request, current_app
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
        # Check if at least one piece of materiel is selected
        if len(data["materiel"]) > 0:
            # if 
            return {"message": "Réservation effectuée !"}
        else:
            raise Exception("Erreur : aucun matériel n'a été sélectionné")
    except Exception as e:
        return {"error": str(e)}

# Get all the materiel contained in the Materiel table
def get_all_materiel():
    try:
        mydb = current_app.config['mydb']
        mycursor = mydb.cursor()
        print("inside get_all_materiel  ")
        # For performance and code maintainability reasons, it's better to specify the fields to SELECT rather than using "SELECT *"
        mycursor.execute('''SELECT id_materiel, type, modele, description, quantite, image, remarque FROM Materiel
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
        print("inside get_all_materiel  ")
        # For performance and code maintainability reasons, it's better to specify the fields to SELECT rather than using "SELECT *"
        mycursor.execute('''SELECT m.id_materiel, m.type, m.modele, m.description, m.quantite, m.image, m.remarque,
            CASE
                WHEN (
                SELECT COUNT(*)
                FROM Reservations r
                JOIN Reservations_Materiel rm ON r.id_reservation = rm.id_reservation
                WHERE rm.id_materiel = m.id_materiel
                AND (
                    rm.rendu = 0
                    OR rm.manquant = 1
                    OR m.quantite = 0
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
                AND retour_incomplet = 0
                AND m.quantite > 0
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

# A FINIR!!!!!!!!!!!!
def insert_reservation(dates):
    try:
        # Vérifier si dates.debut et dates.fin ont été renseignés
        if dates.debut and dates.fin:
            # Vérifier si dates.debut est au moins supérieure ou égale à la date du jeu  
            if dates.debut:
                # Vérifier si dates.fin est au moins supérieure ou égale à dates.debut
                if dates.fin:
                    print("réservation insérée avec succès!")
                else:
                    raise Exception("")
            else:
                raise Exception("")
        else:
            raise Exception("Erreur : les dates ne sont pas indiquées")
    except Exception as e:
        print(e)
        raise Exception("Erreur lors de l'insertion de la réservation") from e

# A FINIR!!!!!!!!!!!!
def insert_projet(projet):
    try:
        if projet.description:
            print("projet inséré avec succès!")
        else:
            raise Exception("Erreur : pour indiquer un projet, il faut au minimum renseigner sa description")
    except Exception as e:
        print(e)
        raise Exception("Erreur lors de l'insertion du projet") from e

# A FINIR!!!!!!!!!!!!
def insert_contacts(contacts):
    try:
        # Check if there is at least one contact
        if len(contacts) > 0:
            # For each contact, check if all the informations are here
            for contact in contacts:
                if contact.nom and contact.prenom and contact.email:
                    print("contacts insérés avec succès!")
                else:
                    raise Exception("Erreur : des informations sont manquantes sur au moins un contact")
        else:
            raise Exception("Erreur : merci de renseigner au minimum un contact")
    except Exception as e:
        print(e)
        raise Exception("Erreur lors de l'insertion des contacts") from e

# Pertinence/cohérence de la propriété quantité, puisqu'on gère le matériel à l'unité et au cas par cas (pour indiquer s'il a été emprunté, ajouter des remarques...) ?
# Je pense qu'il serait plus judicieux de retirer cette propriété de la table Materiel.