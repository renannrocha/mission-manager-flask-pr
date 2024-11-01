from flask_restful import Resource, reqparse
from flask import jsonify
from src.models.entities.missions import Missions  
from src.models.enum.missionStatus import MissionStatus
from datetime import datetime

"""
id
name
launchDate
destination
missionStatus
crew
payload
duration
cost
missionInfo
"""

argumentos = reqparse.RequestParser()
argumentos.add_argument('name', type=str, required=True)
argumentos.add_argument('launchDate', type=str, required=True)  # Formato: "YYYY-MM-DD"
argumentos.add_argument('destination', type=str, required=True)
argumentos.add_argument('missionStatus', type=str, required=True)  # Espera o nome do enum
argumentos.add_argument('crew', type=str)
argumentos.add_argument('payload', type=str)
argumentos.add_argument('duration', type=str)
argumentos.add_argument('cost', type=float, required=True) 
argumentos.add_argument('missionInfo', type=str)

argumentos_update = reqparse.RequestParser()
argumentos_update.add_argument('id', type=int, required=True)
argumentos_update.add_argument('name', type=str)
argumentos_update.add_argument('launchDate', type=str)  # Formato: "YYYY-MM-DD"
argumentos_update.add_argument('destination', type=str)
argumentos_update.add_argument('missionStatus', type=str)  # Espera o nome do enum
argumentos_update.add_argument('crew', type=str)
argumentos_update.add_argument('payload', type=str)
argumentos_update.add_argument('duration', type=str)
argumentos_update.add_argument('cost', type=float) 
argumentos_update.add_argument('missionInfo', type=str)

argumentos_delete = reqparse.RequestParser()
argumentos_delete.add_argument('id', type=int, required=True)

argumentos_search = reqparse.RequestParser()
argumentos_search.add_argument('startDate', type=str, required=True)  # Formato: "YYYY-MM-DD"
argumentos_search.add_argument('endDate', type=str, required=True)    # Formato: "YYYY-MM-DD"


class MissionList(Resource):
    def get(self):
        try:
            args = argumentos_search.parse_args()
            start_date = datetime.strptime(args['startDate'], "%Y-%m-%d")
            end_date = datetime.strptime(args['endDate'], "%Y-%m-%d")
            missions = Missions.search_missions_by_date(start_date, end_date)  

            # Ordenar missões por data de lançamento
            missions.sort(key=lambda x: x['launchDate'], reverse=True)
            return missions, 200
        except Exception as e:
            return {'status': 500, 'msg': str(e)}, 500

class MissionInsert(Resource):
    def post(self):
        try:
            datas = argumentos.parse_args()
            missionStatus = MissionStatus[datas['missionStatus']]
            new_mission = Missions.create_mission(
                name=datas['name'],
                launchDate=datas['launchDate'],
                destination=datas['destination'],
                missionStatus=missionStatus,
                crew=datas.get('crew'),
                payload=datas.get('payload'),
                duration=datas.get('duration'),
                cost=datas['cost'],  
                missionInfo=datas.get('missionInfo')
            )

            if new_mission is None:
                return {'status': 500, 'msg': 'Failed to create mission.'}, 500

            return {'message': 'Mission created successfully!', 'id': new_mission.id}, 201
        except Exception as e:
            return {'status': 500, 'msg': str(e)}, 500


class MissionById(Resource):
    def get(self):
        try:
            args = reqparse.RequestParser()
            args.add_argument('id', type=int, required=True)
            datas = args.parse_args()
            mission = Missions.get_mission(datas['id'])
            if mission:
                return mission, 200
            return {'message': 'Mission not found'}, 404
        except Exception as e:
            return {'status': 500, 'msg': str(e)}, 500

class MissionUpdate(Resource):
    def put(self):
        try:
            datas = argumentos_update.parse_args()
            missionStatus = MissionStatus[datas['missionStatus']] if datas.get('missionStatus') else None
            Missions.update_mission(
                mission_id=datas['id'],
                name=datas.get('name'),
                launchDate=datas.get('launchDate'),
                destination=datas.get('destination'),
                missionStatus=missionStatus,
                crew=datas.get('crew'),
                payload=datas.get('payload'),
                duration=datas.get('duration'),
                cost=datas.get('cost'), 
                missionInfo=datas.get('missionInfo')
            )
            return {'message': 'Mission updated successfully!'}, 200
        except Exception as e:
            return {'status': 500, 'msg': str(e)}, 500

class MissionDelete(Resource):
    def delete(self):
        try:
            datas = argumentos_delete.parse_args()
            Missions.delete_mission(datas['id'])
            return {'message': 'Mission deleted successfully!'}, 200
        except Exception as e:
            return {'status': 500, 'msg': str(e)}, 500
