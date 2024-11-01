from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from src.models.entities.missions import Missions
from rest.controller.missionsController import MissionInsert, MissionList, MissionById, MissionDelete, MissionUpdate 

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

api = Api(app)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

# Adiciona os recursos da API
api.add_resource(MissionInsert, "/missions/add")
api.add_resource(MissionList, "/missions/get")
api.add_resource(MissionById, "/missions/getById")
api.add_resource(MissionUpdate, "/missions/update")
api.add_resource(MissionDelete, "/missions/delete")

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
