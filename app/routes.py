from flask import request, jsonify
from flask_restful import Resource
from .models import Mission, db
from datetime import datetime

class MissionListResource(Resource):
    def get(self):
        """Retorna todas as missões, ordenadas por data de lançamento"""
        missions = Mission.query.order_by(Mission.launch_date.desc()).all()
        return jsonify([mission.to_dict() for mission in missions])

    def post(self):
        """Cria uma nova missão com os dados fornecidos"""
        data = request.get_json()
        new_mission = Mission(
            name=data['name'],
            launch_date=datetime.strptime(data['launch_date'], '%Y-%m-%d'),
            destination=data['destination'],
            status=data['status'],
            crew=data.get('crew', ''),
            payload=data.get('payload', ''),
            duration=data.get('duration', ''),
            cost=data.get('cost', 0.0),
            mission_status=data.get('mission_status', '')
        )
        db.session.add(new_mission)
        db.session.commit()
        return {"message": "Mission created", "id": new_mission.id}, 201

class MissionResource(Resource):
    def get(self, mission_id):
        """Retorna os detalhes de uma missão específica"""
        mission = Mission.query.get_or_404(mission_id)
        return jsonify(mission.to_dict())

    def put(self, mission_id):
        """Atualiza os dados de uma missão existente"""
        mission = Mission.query.get_or_404(mission_id)
        data = request.get_json()
        mission.name = data['name']
        mission.launch_date = datetime.strptime(data['launch_date'], '%Y-%m-%d')
        mission.destination = data['destination']
        mission.status = data['status']
        mission.crew = data.get('crew', '')
        mission.payload = data.get('payload', '')
        mission.duration = data.get('duration', '')
        mission.cost = data.get('cost', 0.0)
        mission.mission_status = data.get('mission_status', '')

        db.session.commit()
        return {"message": "Mission updated"}

    def delete(self, mission_id):
        """Deleta uma missão específica pelo ID"""
        mission = Mission.query.get_or_404(mission_id)
        db.session.delete(mission)
        db.session.commit()
        return {"message": "Mission deleted"}

class MissionSearchResource(Resource):
    def get(self):
        """Pesquisa missões por intervalo de datas"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return {"message": "start_date and end_date are required"}, 400

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        missions = Mission.query.filter(Mission.launch_date.between(start_date, end_date)).all()
        return jsonify([mission.to_dict() for mission in missions])

def initialize_routes(api):
    api.add_resource(MissionListResource, '/missions')  # Endpoint para todas as missões (GET, POST)
    api.add_resource(MissionResource, '/missions/<int:mission_id>')  # Endpoint para uma missão específica (GET, PUT, DELETE)
    api.add_resource(MissionSearchResource, '/missions/search')  # Endpoint de pesquisa por intervalo de datas
