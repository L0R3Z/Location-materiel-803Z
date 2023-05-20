from flask import Flask, Blueprint, jsonify, session, render_template, redirect, url_for, request, current_app
from utility import encrypt_password

admin = Blueprint("admin", __name__)

#########
# admin #
#########

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

##################
# manageMateriel #
##################

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
                    VALUES (%s, %s, %s, %s, %s)'''
                    mycursor.execute(tempQuery, (str(request.form['type']), str(request.form['modele']), str(request.form['description']), str(request.form['image']), str(request.form['remarque'])))
                # Case when no image url is send
                else:
                    tempQuery = '''INSERT INTO Materiel(type, modele, description, remarque) 
                    VALUES (%s, %s, %s, %s)'''
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

@admin.route("/manageMateriel/archiveMateriel", methods=['POST'])
def admin_archiveMateriel():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        try:
            if request.form['id_materiel'] and request.form['archive'] and request.form['start']:
                archive = bool(int(request.form['archive']))
                archive = 1 if archive == False else 0
                mydb = current_app.config['mydb']
                mycursor = mydb.cursor()
                print("inside admin_archiveMateriel   ")
                tempQuery = '''
                    UPDATE Materiel SET archive = %s 
                    WHERE id_materiel = %s
                '''
                mycursor.execute(tempQuery, (archive, str(request.form['id_materiel'])))
                mydb.commit()
                mycursor.close()
                if request.form['start'] == str(0):
                    return redirect(url_for("admin.admin_manageMateriel"))
                else:
                     return redirect(url_for('admin.admin_editMateriel', id_materiel=request.form['id_materiel']))
            else:
                e = "Erreur : pas d'ID de matériel renseigné pour la suprression"
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
                tempQuery = '''
                    DELETE FROM Reservations_Materiel WHERE id_materiel = %s;
                '''
                mycursor.execute(tempQuery, (request.form['id_materiel'],))
                mydb.commit()
                tempQuery = '''
                    DELETE FROM Materiel WHERE id_materiel = %s;
                '''
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

@admin.route("/manageMateriel/editMateriel", methods=['GET'])
def admin_editMateriel():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        try:
            if 'id_materiel' in request.args:
                mydb = current_app.config['mydb']
                mycursor = mydb.cursor()
                print("inside admin_editMateriel")
                tempQuery = '''
                    SELECT
                        m.id_materiel,
                        m.type,
                        m.modele,
                        m.description,
                        m.image,
                        m.remarque,
                        m.archive
                    FROM Materiel m
                    WHERE m.id_materiel = %s;
                '''
                mycursor.execute(tempQuery, (request.args.get('id_materiel'),))
                # mydb.commit()
                materiel_row = mycursor.fetchone()
                # Convert the returned tuples into a well-organized dict with named properties
                if materiel_row:
                    materiel = dict(zip(mycursor.column_names, materiel_row))
                else:
                    materiel = None
                mycursor.close()
                return render_template("pages/admin_editMateriel.html", materiel=materiel)
            else:
                e = "Erreur : pas d'ID de matériel renseigné pour la modification"
                return render_template("pages/admin.html", error=str(e))
        except Exception as e: # If the query fails, render the template with a user-friendly error message
            return render_template("pages/admin.html", error=str(e))
    # If it's empty, it means that the admin isn't connected
    # If so, redirect to the admin connection page
    else:
        return redirect(url_for("admin.admin_connexion"))

@admin.route("/manageMateriel/updateMateriel", methods=['POST'])
def admin_updateMateriel():
    admin_id = session.get("admin_id")
    # If the admin_id isn't empty, it means that the admin is connected
    if admin_id:
        try:
            if request.form['id_materiel']:
                mydb = current_app.config['mydb']
                mycursor = mydb.cursor()
                print("inside admin_updateMateriel")
                if request.form['image']:
                    tempQuery = '''
                        UPDATE Materiel SET type = %s, modele = %s, description = %s, image = %s, remarque = %s 
                        WHERE id_materiel = %s
                    '''
                    mycursor.execute(tempQuery, (str(request.form['type']), str(request.form['modele']), str(request.form['description']), str(request.form['image']), str(request.form['remarque']), str(request.form['id_materiel'])))
                # Case when no image url is send
                else:
                    tempQuery = '''
                        UPDATE Materiel SET type = %s, modele = %s, description = %s, image = NULL, remarque = %s 
                        WHERE id_materiel = %s
                    '''
                    mycursor.execute(tempQuery, (str(request.form['type']), str(request.form['modele']), str(request.form['description']), str(request.form['remarque']), str(request.form['id_materiel'])))
                mydb.commit()
                mycursor.close()
                return redirect(url_for('admin.admin_editMateriel', id_materiel=request.form['id_materiel']))
            else:
                e = "Erreur : pas d'ID de matériel renseigné pour la mise à jour"
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
        mycursor.execute('''
            SELECT
                m.id_materiel,
                m.type,
                m.modele,
                m.description,
                m.image,
                m.remarque,
                m.archive,
                (
                    SELECT 
                        CASE
                            WHEN COUNT(*) > 0 THEN GROUP_CONCAT(DISTINCT CASE rm.defaut WHEN true THEN 1 ELSE 0 END ORDER BY rm.id_reservation)
                            ELSE NULL
                        END
                    FROM Reservations_Materiel rm
                    JOIN Reservations r ON rm.id_reservation = r.id_reservation
                    WHERE rm.id_materiel = m.id_materiel
                    AND ((rm.rendu = 0 OR rm.defaut = 1) AND r.archive = 0)
                ) AS defaut,
                (
                    SELECT 
                        CASE
                            WHEN COUNT(*) > 0 THEN GROUP_CONCAT(DISTINCT CONCAT(r.date_debut) ORDER BY r.id_reservation)
                            ELSE NULL
                        END
                    FROM Reservations r
                    JOIN Reservations_Materiel rm ON r.id_reservation = rm.id_reservation
                    WHERE rm.id_materiel = m.id_materiel
                    AND ((rm.rendu = 0 OR rm.defaut = 1) AND r.archive = 0)
                ) AS dates_debut,
                (
                    SELECT 
                        CASE
                            WHEN COUNT(*) > 0 THEN GROUP_CONCAT(DISTINCT CONCAT(r.date_fin) ORDER BY r.id_reservation)
                            ELSE NULL
                        END
                    FROM Reservations r
                    JOIN Reservations_Materiel rm ON r.id_reservation = rm.id_reservation
                    WHERE rm.id_materiel = m.id_materiel
                    AND ((rm.rendu = 0 OR rm.defaut = 1) AND r.archive = 0)
                ) AS dates_fin,
                (
                    SELECT 
                        CASE
                            WHEN COUNT(*) > 0 THEN GROUP_CONCAT(DISTINCT rm.id_reservation ORDER BY rm.id_reservation)
                            ELSE NULL
                        END
                    FROM Reservations_Materiel rm
                    JOIN Reservations r ON rm.id_reservation = r.id_reservation
                    WHERE rm.id_materiel = m.id_materiel
                    AND ((rm.rendu = 0 OR rm.defaut = 1) AND r.archive = 0)
                ) AS id_reservation
            FROM Materiel m;
            ''')
        rows = mycursor.fetchall()
        # Convert the returned tuples into a well-organized dict with named properties
        materiel_list = [dict(zip(mycursor.column_names, row)) for row in rows]
        mycursor.close()
        return materiel_list
    except Exception as e: # Raise an exception if the request fails. This allows us to display the error message to the user.
        print(e)
        raise Exception("Erreur : impossible de récupérer la liste de matériel") from e


#####################
# manageReservation #
#####################

@admin.route("/managereservations/")
def admin_managereservations():
    admin_id = session.get("admin_id")
    if admin_id:
        try:
            reservation_list = admin_get_all_reservation()
            return render_template("pages/admin_manageReservation.html", reservation_list=reservation_list)
        except Exception as e:
            return render_template("pages/admin.html", error=str(e))
    else:
        return redirect(url_for("admin.admin_connexion"))

@admin.route("/managereservation/")
@admin.route("/managereservation/?id=<int:id_reservation>")
def admin_managereservation(id_reservation=None):
    admin_id = session.get("admin_id")
    if admin_id:
        try:
            reservation_data = admin_get_reservation_by_id(id_reservation)
            print(reservation_data)
            return render_template("pages/admin_editReservation.html", reservation_data=reservation_data)
        except Exception as e:
            return render_template("pages/admin.html", error=str(e))
    else:
        return redirect(url_for("admin.admin_connexion"))
    
@admin.route("/managereservation/deletereservation/<int:id_reservation>", methods=['DELETE'])
def admin_deletereservation(id_reservation=None):
    admin_id = session.get("admin_id")
    if admin_id:
        try:
            print(id_reservation)
            if id_reservation:
                mydb = current_app.config['mydb']
                mycursor = mydb.cursor()
                tempQuery = '''DELETE FROM Reservations_Materiel WHERE id_reservation = %s;'''
                mycursor.execute(tempQuery, (id_reservation,))
                tempQuery = '''DELETE FROM Contacts WHERE id_reservation = %s;'''
                mycursor.execute(tempQuery, (id_reservation,))
                tempQuery = '''DELETE FROM Projets WHERE id_reservation = %s;'''
                mycursor.execute(tempQuery, (id_reservation,))
                mydb.commit()
                tempQuery = '''DELETE FROM Reservations WHERE id_reservation = %s;'''
                mycursor.execute(tempQuery, (id_reservation,))
                mydb.commit()
                mycursor.close()
                return {"message": "Réservation supprimée avec succès !"}
            else:
                return {"error": "Erreur : pas d'ID de matériel renseigné pour la suppression"}
        except Exception as e:
            return {"error": e}
    else:
        return redirect(url_for("admin.admin_connexion"))
    
@admin.route("/managereservation/archivereservation/<int:id_reservation>", methods=['UPDATE'])
def admin_archivereservation(id_reservation=None):
    admin_id = session.get("admin_id")
    if admin_id:
        try:
            if id_reservation:
                # archive = bool(int(request.form['archive']))
                # archive = 1 if archive == False else 0
                mydb = current_app.config['mydb']
                mycursor = mydb.cursor()
                print("inside admin_archiveReservation   ")
                tempQuery = '''UPDATE Reservations SET archive = 1 WHERE id_reservation = %s'''
                mycursor.execute(tempQuery, (id_reservation,))
                mydb.commit()
                mycursor.close()
                return {"message": "Réservation archivée avec succès !"}
            else:
                return {"error": "Erreur : pas d'ID de matériel renseigné pour archiver"}
        except Exception as e:
            return {"error": e}
    else:
        return redirect(url_for("admin.admin_connexion"))

# @admin.route("/managereservation/edit")
# def admin_editreservation():
#     admin_id = session.get("admin_id")
#     if admin_id:
#         try:
#             reservationId = request.args.get('id_reservation')
#             reservation_data = admin_get_reservation_by_id(reservationId)
#             return render_template("pages/admin_editReservation.html", reservation_data=reservation_data)
#         except Exception as e:
#             return render_template("pages/admin.html", error=str(e))
#     else:
#         return redirect(url_for("admin.admin_connexion"))

def admin_get_all_reservation():
    try:
        mydb = current_app.config['mydb']
        mycursor = mydb.cursor()
        mycursor.execute('''
            SELECT
                id_reservation, date_debut, date_fin, sortie, date_restitution, retour_complet, archive
            FROM
                Reservations
            ORDER BY
                date_debut
            ''')
        rows = mycursor.fetchall()
        reservation_list = [dict(zip(mycursor.column_names, row)) for row in rows]
        mycursor.close()
        return reservation_list
    except Exception as e:
        print(e)
        raise Exception("Erreur : impossible de récupérer la liste de réservations") from e

def admin_get_reservation_by_id(id):
    try:
        mydb = current_app.config['mydb']
        mycursor = mydb.cursor()
        tempQuery = '''
            SELECT
                id_reservation, date_debut, date_fin, sortie, date_restitution, retour_complet, archive
            FROM
                Reservations
            WHERE
                id_reservation = %s
            '''
        mycursor.execute(tempQuery, (id, ))
        rows = mycursor.fetchall()
        reservation = [dict(zip(mycursor.column_names, row)) for row in rows]
        mycursor.close()
        return reservation[0]
    except Exception as e:
        print(e)
        raise Exception("Erreur : impossible de récupérer les données actuelles de la réservation") from e
