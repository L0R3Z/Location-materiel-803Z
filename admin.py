from flask import Flask, Blueprint, jsonify, session, render_template, redirect, url_for, request, current_app
from utility import encrypt_password

admin = Blueprint("admin", __name__)

@admin.route("/")
def index():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        print(admin_id)
        return render_template("admin.html")
    # If it's empty, it means that the admin isn't connected
    # If so, redirect to the admin connection page
    else:
        return redirect(url_for("admin.admin_connexion"))
        

@admin.route("/connexion/")
def admin_connexion():
    return render_template("admin_connexion.html")

@admin.route("/tryconnection/", methods=["GET", "POST"])
def admin_tryconnection():
    data = request.json
    username = data["username"]
    passwd = encrypt_password(data["passwd"])
    isValid = check_admin_username_passwd(username, passwd)
    if isValid:
        # Set the admin_id inside the session, to prove that the admin is connected
        # A session is valid as long as the user doesn't close his browser
        session["admin_id"] = isValid
        # session["admin_id"] = admin.id
        return "1"
    else:
        return "0"

@admin.route("/logout/")
def admin_logout():
    session.pop("admin_id", None)
    return redirect(url_for("admin.admin_connexion"))

def check_admin_username_passwd(username, passwd):
    mydb = current_app.config['mydb']
    mycursor = mydb.cursor()
    mycursor.execute('''SELECT * FROM Admin
        WHERE pseudo = %s AND mdp = %s
        LIMIT 1
        ''', (username, passwd))
    datas = mycursor.fetchone()
    if datas:
        return datas[0]