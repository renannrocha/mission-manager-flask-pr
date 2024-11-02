from flask_restful import Resource, reqparse
from flask import jsonify
from src.models.entities.missions import Missions
from datetime import datetime, date

argumentos = reqparse.RequestParser()
argumentos.add_argument('name', type=str, required=True)
argumentos.add_argument('launchDate', type=str, required=True) 
argumentos.add_argument('destination', type=str, required=True)
argumentos.add_argument('status', type=str, required=True)  
argumentos.add_argument('crew', type=str)
argumentos.add_argument('payload', type=str)
argumentos.add_argument('duration', type=str)
argumentos.add_argument('cost', type=float, required=True)
argumentos.add_argument('missionInfo', type=str)

argumentos_update = reqparse.RequestParser()
argumentos_update.add_argument('name', type=str)
argumentos_update.add_argument('launchDate', type=str) 
argumentos_update.add_argument('destination', type=str)
argumentos_update.add_argument('status', type=str)  
argumentos_update.add_argument('crew', type=str)
argumentos_update.add_argument('payload', type=str)
argumentos_update.add_argument('duration', type=str)
argumentos_update.add_argument('cost', type=float)
argumentos_update.add_argument('missionInfo', type=str)

argumentos_search = reqparse.RequestParser()
argumentos_search.add_argument('startDate', type=str, required=True) 
argumentos_search.add_argument('endDate', type=str, required=True)   

class MissionList(Resource):
    def get(self):
        try:
            args = argumentos_search.parse_args()
            
            try:
                start_date = datetime.strptime(args['startDate'], "%Y-%m-%d").date()
                end_date = datetime.strptime(args['endDate'], "%Y-%m-%d").date()
            except ValueError:
                return {'status': 400, 'msg': "Formato de data inválido. Use 'YYYY-MM-DD'."}, 400
            
            missions = Missions.search_missions_by_date(start_date, end_date)

            if not missions:
                return {'status': 404, 'msg': "Nenhuma missão encontrada para as datas fornecidas."}, 404

            missions.sort(key=lambda x: x['launchDate'], reverse=True)

            for mission in missions:
                mission['launchDate'] = mission['launchDate'].strftime("%Y-%m-%d")

            return missions, 200
        
        except Exception as e:
            return {'status': 500, 'msg': f"Erro interno: {str(e)}"}, 500


class MissionInsert(Resource):
    def post(self):
        try:
            datas = argumentos.parse_args()
            print(f"Received data: {datas}") 

            mission_status = datas['status']
            print(f"Processed status: {mission_status}")

            launch_date = datetime.strptime(datas['launchDate'], '%Y-%m-%d').date()

            new_mission = Missions.create_mission(
                name=datas['name'],
                launchDate=launch_date,
                destination=datas['destination'],
                status=datas.get('status'), 
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
            print(f"Erro: {str(e)}")  
            return {'status': 500, 'msg': str(e)}, 500


class MissionUpdate(Resource):
    def put(self, mission_id):
        try:
            datas = argumentos_update.parse_args() 
            mission_status = datas.get('status')  

            if datas.get('launchDate'):
                launch_date = datetime.strptime(datas['launchDate'], '%Y-%m-%d').date()
            else:
                launch_date = None

            updated_mission = Missions.update_mission(
                mission_id=mission_id, 
                name=datas.get('name'),
                launchDate=launch_date,
                destination=datas.get('destination'),
                status=mission_status,
                crew=datas.get('crew'),
                payload=datas.get('payload'),
                duration=datas.get('duration'),
                cost=datas.get('cost'),
                missionInfo=datas.get('missionInfo')
            )

            if updated_mission:
                return {'message': 'Mission updated successfully!'}, 200
            return {'status': 404, 'msg': 'Mission not found.'}, 404
        except Exception as e:
            return {'status': 500, 'msg': str(e)}, 500


class MissionDelete(Resource):
    def delete(self, mission_id):
        try:
            Missions.delete_mission(mission_id)
            return {'message': 'Mission deleted successfully!'}, 200
        except Exception as e:
            return {'status': 500, 'msg': str(e)}, 500
