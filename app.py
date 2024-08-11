# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify
import mysql.connector

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

print(mydb)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE todos")
# mycursor.execute("CREATE TABLE todo (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description VARCHAR(255), completed BOOLEAN)")

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/api/v1/todo/create', methods=['POST'])
def createTodo():
    input_json = request.get_json()
    print(input_json)
    sql = "INSERT INTO todo (title, description, completed) VALUES (%s, %s, %s)"
    val = (input_json["Title"], input_json["Description"], input_json["Completed"])
    mycursor.execute(sql, val)

    mydb.commit()
    successMessage = {
        "success": "True",
        "id": mycursor.lastrowid
    }
    return jsonify(successMessage)

@app.route('/api/v1/todo/get', methods=['GET'])
def getTodo():
    query_params = request.args
    print(query_params['id'])
    sql = "SELECT id, title, description, completed from todo where id = %s "
    # adr = (query_params.get('roll'),)
    #         OR
    val = (query_params['id'],)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    print(myresult)
    todo = {'todo_id': myresult[0],
                    'title': myresult[1],
                    'description': myresult[2],
                    'completed': myresult[3]}

    response = {'success': True,
                'data': todo }
    return jsonify(response)



# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', port=5002)

