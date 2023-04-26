from flask import Flask, Blueprint, jsonify, session, render_template, redirect, url_for, request, current_app
from utility import encrypt_password

materiel = Blueprint("materiel", __name__)

# Main route of materiel blueprint
@materiel.route("/")
def index():
    try:
        materiel_list = get_all_materiel()
        return render_template("materiel.html", materiel_list=materiel_list)
    except Exception as e: # If the query fails, render the template with a user-friendly error message
        return render_template("materiel.html", error=str(e)) 

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
        raise Exception("Erreur: impossible de récupérer la liste de matériel") from e

# MAKE A QUERY THAT RETURN ALL THE MATERIEL, WITH ITS DISPONIBILITY STATUS AND ITS DATE OF RETURN