from flask_restful import Resource, reqparse
from flask import jsonify
from src.models.entities.missions import Missions  
from models.enum.missionStatus import MissionStatus
from datetime import datetime

# Definindo argumentos para criar uma missão
argumentos = reqparse.RequestParser()
argumentos.add_argument('missionName', type=str, required=True)
argumentos.add_argument('releaseDate', type=str, required=True)  # Formato: "YYYY-MM-DD"
argumentos.add_argument('destination', type=str, required=True)
argumentos.add_argument('missionStatus', type=str, required=True)  # Espera o nome do enum
argumentos.add_argument('tripulation', type=str)
argumentos.add_argument('payload', type=str)
argumentos.add_argument('missionDuration', type=str)
argumentos.add_argument('missionCost', type=float, required=True) 
argumentos.add_argument('missionInfoStatus', type=str)

# Definindo argumentos para atualizar uma missão
argumentos_update = reqparse.RequestParser()
argumentos_update.add_argument('id', type=int, required=True)
argumentos_update.add_argument('missionName', type=str)
argumentos_update.add_argument('releaseDate', type=str)  # Formato: "YYYY-MM-DD"
argumentos_update.add_argument('destination', type=str)
argumentos_update.add_argument('missionStatus', type=str)  # Espera o nome do enum
argumentos_update.add_argument('tripulation', type=str)
argumentos_update.add_argument('payload', type=str)
argumentos_update.add_argument('missionDuration', type=str)
argumentos_update.add_argument('missionCost', type=float) 
argumentos_update.add_argument('missionInfoStatus', type=str)

# Definindo argumentos para deletar uma missão
argumentos_delete = reqparse.RequestParser()
argumentos_delete.add_argument('id', type=int, required=True)

# Definindo argumentos para pesquisar missões por intervalo de datas
argumentos_search = reqparse.RequestParser()
argumentos_search.add_argument('startDate', type=str, required=True)  # Formato: "YYYY-MM-DD"
argumentos_search.add_argument('endDate', type=str, required=True)    # Formato: "YYYY-MM-DD"


class MissionList(Resource):
    def get(self):
        try:
            args = argumentos_search.parse_args()
            start_date = datetime.strptime(args['startDate'], "%Y-%m-%d")
            end_date = datetime.strptime(args['endDate'], "%Y-%m-%d")
            missions = Missions.search_missions_by_date(start_date, end_date)  # Usar o método de pesquisa

            # Ordenar missões por data de lançamento em ordem decrescente
            missions.sort(key=lambda x: x['releaseDate'], reverse=True)
            return jsonify(missions)
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class MissionInsert(Resource):
    def post(self):
        try:
            datas = argumentos.parse_args()
            missionStatus = MissionStatus[datas['missionStatus']]  
            new_mission = Missions.create_mission(
                missionName=datas['missionName'],
                releaseDate=datas['releaseDate'],
                destination=datas['destination'],
                missionStatus=missionStatus,
                tripulation=datas.get('tripulation'),
                payload=datas.get('payload'),
                missionDuration=datas.get('missionDuration'),
                missionCost=datas['missionCost'],  
                missionInfoStatus=datas.get('missionInfoStatus')
            )
            return jsonify({'message': 'Mission created successfully!', 'id': new_mission.id}), 201
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class MissionById(Resource):
    def get(self):
        try:
            args = reqparse.RequestParser()
            args.add_argument('id', type=int, required=True)
            datas = args.parse_args()
            mission = Missions.get_mission(datas['id'])
            if mission:
                return jsonify(mission)
            return jsonify({'message': 'Mission not found'}), 404
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class MissionUpdate(Resource):
    def put(self):
        try:
            datas = argumentos_update.parse_args()
            missionStatus = MissionStatus[datas['missionStatus']] if datas.get('missionStatus') else None
            Missions.update_mission(
                mission_id=datas['id'],
                missionName=datas.get('missionName'),
                releaseDate=datas.get('releaseDate'),
                destination=datas.get('destination'),
                missionStatus=missionStatus,
                tripulation=datas.get('tripulation'),
                payload=datas.get('payload'),
                missionDuration=datas.get('missionDuration'),
                missionCost=datas.get('missionCost'), 
                missionInfoStatus=datas.get('missionInfoStatus')
            )
            return jsonify({'message': 'Mission updated successfully!'}), 200
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class MissionDelete(Resource):
    def delete(self):
        try:
            datas = argumentos_delete.parse_args()
            Missions.delete_mission(datas['id'])
            return jsonify({'message': 'Mission deleted successfully!'}), 200
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500
