# Could maybe use Flask-Swagger later to automatically generate the API documentation
from flask import Flask, request, render_template, jsonify, abort, session, redirect, url_for
from flask_cors import CORS
from database import connect_db, create_tables, insert_basic_datas
from admin import admin
from reservation import reservation



# Connect to database
mydb = connect_db()

# Create database cursor
mycursor = mydb.cursor()

# Check if the tables should be created and if the sample data should be inserted by checking if the Admin table exists
# Saves performance by avoiding otherwise unnecessary requests
mycursor.execute('''SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = 'Admin') AS table_exists;''')
isDatabaseCreated = (mycursor.fetchone())[0]
if isDatabaseCreated == 0:
    print("Creation and filling of tables with sample data...")
    create_tables(mydb, mycursor)
    insert_basic_datas(mydb, mycursor)

# In case I want to insert random values into the database...
# mycursor.execute('''INSERT INTO Materiel(type, modele, description, image, remarque) VALUES
#     ("trepied", "Trepied 2000", "18m 4 pieds etc.", 1, "https://www.europe-nature-optik.fr/884-tm_thickbox_default/kite-trepied-ardea-cf-avec-rotule-manfrotto-128rc.jpg", "")''')
# mydb.commit()
    
# Close database cursor
# Keeping the cursor open for an extended period of time can tie up database resources and potentially cause issues for other connections
mycursor.close()



# Start the Flask application
app = Flask(__name__)
app.secret_key = "123456789" # Set a secret key to ensure that the session data is enabled and secure
app.config['mydb'] = mydb
CORS(app)



# Index route
@app.route("/")
def index():
    return render_template("pages/accueil.html")

# Import blueprint routes from another file
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(reservation, url_prefix="/reservation")



# Run app in debug mode
# Useful for development, but to be removed for the production version
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
