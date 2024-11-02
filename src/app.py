import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from src.database import db
from flask_restful import Api
from flask_cors import CORS
from src.models.entities.missions import Missions
from src.rest.controller.missionsController import (
    MissionInsert,
    MissionList,
    MissionDelete,
    MissionUpdate,
)

app = Flask(__name__)
CORS(app)

# Verificação do valor da variável de ambiente
database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
print("Database URI:", database_uri)  # Adicione esta linha para depuração

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri or 'sqlite:///fallback_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'false').lower() == 'true'

db.init_app(app)

# Inicializa o contexto da aplicação para criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Instância da API RESTful
api = Api(app)

# Adiciona os recursos da API
api.add_resource(MissionInsert, "/missions/add")
api.add_resource(MissionList, "/missions/get")
api.add_resource(MissionUpdate, "/missions/update/<int:mission_id>")
api.add_resource(MissionDelete, "/missions/delete/<int:mission_id>")