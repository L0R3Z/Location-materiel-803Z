from flask import Flask, Blueprint, jsonify, session, render_template, redirect, url_for, request, current_app
from utility import encrypt_password

admin = Blueprint("admin", __name__)

@admin.route("/")
def index():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        return render_template("pages/admin.html")
    # If it's empty, it means that the admin isn't connected
    # If so, redirect to the admin connection page
    else:
        return redirect(url_for("admin.admin_connexion"))
        

@admin.route("/connexion/")
def admin_connexion():
    return render_template("pages/admin_connexion.html")

@admin.route("/tryconnection/", methods=["GET", "POST"])
def admin_tryconnection():
    try:
        data = request.json
        username = data["username"]
        passwd = encrypt_password(data["passwd"])
        # Check if the values of username and passwd are empty
        if username != "" and passwd != "":
            adminId = check_admin_username_passwd(username, passwd)
            if adminId:
                # Set the admin_id inside the session, to prove that the admin is connected
                # A session is valid as long as the user doesn't close his browser
                session["admin_id"] = adminId
                return {"value": 1}
            else:
                raise Exception("Erreur : identifiant ou mot de passe incorrect")
        else:
            raise Exception("Erreur : valeur manquante")
    except Exception as e:
        print(e)
        return {"error": str(e)}

@admin.route("/logout/")
def admin_logout():
    session.pop("admin_id", None)
    return redirect(url_for("admin.admin_connexion"))

def check_admin_username_passwd(username, passwd):
    try:
        mydb = current_app.config['mydb']
        mycursor = mydb.cursor()
        mycursor.execute('''SELECT * FROM Admin
            WHERE pseudo = %s AND mdp = %s
            LIMIT 1
            ''', (username, passwd))
        datas = mycursor.fetchone()
        if datas:
            return datas[0]
    except Exception as e:
        print(e)
        raise Exception("Erreur lors de la tentative de connexion") from e

@admin.route("/manageMateriel/")
def admin_manageMateriel():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        try:
            materiel_list = admin_get_all_materiel()
            return render_template("pages/admin_manageMateriel.html", materiel_list=materiel_list)
        except Exception as e: # If the query fails, render the template with a user-friendly error message
            return render_template("pages/admin.html", error=str(e))
    # If it's empty, it means that the admin isn't connected
    # If so, redirect to the admin connection page
    else:
        return redirect(url_for("admin.admin_connexion"))

@admin.route("/manageMateriel/addMateriel", methods=['POST'])
def admin_addMateriel():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        try:
            if request.form['type'] and request.form['modele'] and request.form['description']:
                mydb = current_app.config['mydb']
                mycursor = mydb.cursor()
                print("inside admin_addMateriel  ")
                if request.form['image']:
                    tempQuery = '''INSERT INTO Materiel(type, modele, description, image, remarque) 
                    VALUES (%s, %s, %s, %s, %s, %s)'''
                    mycursor.execute(tempQuery, (str(request.form['type']), str(request.form['modele']), str(request.form['description']), str(request.form['image']), str(request.form['remarque'])))
                # Case when no image url is send
                else:
                    tempQuery = '''INSERT INTO Materiel(type, modele, description, remarque) 
                    VALUES (%s, %s, %s, %s, %s)'''
                    mycursor.execute(tempQuery, (str(request.form['type']), str(request.form['modele']), str(request.form['description']), str(request.form['remarque'])))
                mydb.commit()
                mycursor.close()
                return redirect(url_for("admin.admin_manageMateriel"))
            else:
                e = "Erreur : données manquantes pour insérer ce matériel"
                return render_template("pages/admin.html", error=str(e))
        except Exception as e: # If the query fails, render the template with a user-friendly error message
            return render_template("pages/admin.html", error=str(e))
    # If it's empty, it means that the admin isn't connected
    # If so, redirect to the admin connection page
    else:
        return redirect(url_for("admin.admin_connexion"))

@admin.route("/manageMateriel/deleteMateriel", methods=['POST'])
def admin_deleteMateriel():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        try:
            if request.form['id_materiel']:
                mydb = current_app.config['mydb']
                mycursor = mydb.cursor()
                print("inside admin_deleteMateriel   ")
                tempQuery = '''DELETE FROM Materiel WHERE id_materiel = %s;'''
                mycursor.execute(tempQuery, (request.form['id_materiel'],))
                mydb.commit()
                mycursor.close()
                return redirect(url_for("admin.admin_manageMateriel"))
            else:
                e = "Erreur : pas d'ID de matériel renseigné pour la suprression"
                return render_template("pages/admin.html", error=str(e))
        except Exception as e: # If the query fails, render the template with a user-friendly error message
            return render_template("pages/admin.html", error=str(e))
    # If it's empty, it means that the admin isn't connected
    # If so, redirect to the admin connection page
    else:
        return redirect(url_for("admin.admin_connexion"))

# Get all the materiel contained in the Materiel table
def admin_get_all_materiel():
    try:
        mydb = current_app.config['mydb']
        mycursor = mydb.cursor()
        print("inside admin_get_all_materiel  ")
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