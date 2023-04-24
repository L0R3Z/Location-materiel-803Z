from flask import Flask,request,render_template,jsonify,abort
from flask_cors import CORS
import mysql.connector
from database import create_tables

#######################
# CONNECT TO DATABASE #
#######################

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="803z"
)

mycursor = mydb.cursor()

create_tables(mydb, mycursor)

mycursor.execute('''select * from Contacts''')
contacts = mycursor.fetchall()
print(contacts)

print('-------------------')
mycursor.execute('''select * from Contacts''')
print(mycursor.fetchone())

for contacts in mycursor:
    print(contacts)

mycursor.close()

app = Flask(__name__)
CORS(app)

print("hello world!")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
