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
                e = Exception("Erreur : identifiant ou mot de passe incorrect")
                return {"error": str(e)}
        else:
            e = Exception("Erreur : valeur manquante")
            return {"error": str(e)}
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