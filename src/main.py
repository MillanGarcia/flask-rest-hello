"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

TAREAS=[]
@app.route('/todos/listar', methods=['GET'])
def listar_tareas():
    return jsonify(TAREAS)

@app.route('/todos', methods=['POST'])
def crear_tarea():
    body = request.get_json()
    nuevaTarea = {
        "done": body["done"],
        "label": body["label"],
        "id": body["id"]
    }
    TAREAS.append(nuevaTarea)
    return "crear tarea"

@app.route('/todos/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    resultado = None
    for tarea in TAREAS:
        if tarea["id"] == id:
            resultado = tarea
            break
    if resultado != None:
        TAREAS.remove(resultado)
    return jsonify(TAREAS)

# a partir de aqui


@app.route('/user', methods=['POST'])
def crea_usuario():
    body = request.get_json()
    if body == None: # se podría usar en vez de "==", "is", para validar, pero tiene otros usos
        return "Error, envie la información correctamente"
    
    email = body["email"]
    password = body["password"]
    #password = body.get("password"), si uso este método y no esta dentro del body, ???
    if email is None or password is None:
        return "Email o password incorrectos!!"

    user = User(
        email= email,
        password = password,
        is_active = True
    )

    db.session.add(user)#el db, viene de sql alchemy, como se ve en el archivo models.py
    db.session.commit()#mandar la información a la base de datos

    

    return jsonify(user.serialize())# seria la funcion que

@app.route('/user/listar', methods=['GET'])
def listar_usuario():
    users = User.query.all()
    #resultado = [user.serialize()for user in users]
    result=[]
    for user in users:
        result.append(user.serialize())
    return jsonify(result)

@app.route('/user/<id>', methods=['PUT'])
def obtener_usuario():
    user = User.query.get(id)# el .query, viene de user, que viene del archivo __init__.py, ya que user hereda de db.model
    if user is None:
        return "no existe el usuario con id"+str(id)
    return jsonify(user.serialize())

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
