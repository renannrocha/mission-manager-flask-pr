from src.database import db
from src.models.enum.missionStatus import MissionStatus
from decimal import Decimal
from datetime import datetime

class Missions(db.Model):

    __tablename__ = 'missions'
    __table_args__ = {'sqlite_autoincrement': True}

    """
    {
        "name": "Apollo 11",
        "launch_date": "1969-07-16",
        "destination": "Moon",
        "status": "Completed",
        "crew": "Neil Armstrong, Buzz Aldrin",
        "payload": "Lunar Module",
        "duration": "8 days",
        "cost": 1000000.0,
        "mission_status": "Successful"
    }
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    launchDate = db.Column(db.Date)
    destination = db.Column(db.String(255))
    missionStatus = db.Column(db.Enum(MissionStatus))
    crew = db.Column(db.String(255))
    payload = db.Column(db.String(255))
    duration = db.Column(db.String(255))
    cost = db.Column(db.Numeric(10, 2))  
    missionInfo = db.Column(db.String(500))

    def __init__(self, name, launchDate, destination, missionStatus, crew, payload, duration, cost, missionInfo):
        self.name = name
        self.launchDate = launchDate
        self.destination = destination
        self.missionStatus = missionStatus
        self.crew = crew
        self.payload = payload
        self.duration = duration
        self.cost = cost  
        self.missionInfo = missionInfo

    @classmethod
    def create_mission(cls, name, launchDate, destination, missionStatus, crew, payload, duration, cost, missionInfo):
        try:
            # Converte a string de data para um objeto `date`
            launchDate = datetime.strptime(launchDate, '%Y-%m-%d').date()
            
            # Cria a nova missão com o formato correto dos dados
            new_mission = cls(
                name=name,
                launchDate=launchDate,
                destination=destination,
                missionStatus=missionStatus,
                crew=crew,
                payload=payload,
                duration=duration,
                cost=Decimal(cost),  # Converte o custo para Decimal, caso necessário
                missionInfo=missionInfo
            )
            db.session.add(new_mission)
            db.session.commit()
            return new_mission
        except Exception as e:
            print("Erro ao criar missão:", e)
            db.session.rollback()  # Reverte transações em caso de erro
            return None  # Retorna None explicitamente em caso de falha

    @classmethod
    def get_missions(cls):
        try:
            missions = db.session.query(cls).order_by(cls.launchDate.desc()).all()
            return [{
                'id': mission.id,
                'name': mission.name,
                'launchDate': mission.launchDate,
                'destination': mission.destination,
                'missionStatus': mission.missionStatus.name,
                'crew': mission.crew,
                'payload': mission.payload,
                'duration': mission.duration,
                'cost': str(mission.cost), 
                'missionInfo': mission.missionInfo
            } for mission in missions]
        except Exception as e:
            print("Erro ao obter missões:", e)

    @classmethod
    def get_mission(cls, mission_id):
        try:
            mission = db.session.query(cls).filter(cls.id == mission_id).first()
            if mission:
                return {
                    'id': mission.id,
                    'name': mission.name,
                    'launchDate': mission.launchDate,
                    'destination': mission.destination,
                    'missionStatus': mission.missionStatus.name,
                    'crew': mission.crew,
                    'payload': mission.payload,
                    'duration': mission.duration,
                    'cost': str(mission.cost),  
                    'missionInfo': mission.missionInfo
                }
            return None
        except Exception as e:
            print("Erro ao obter missão:", e)

    @classmethod
    def search_missions_by_date(cls, start_date, end_date):
        try:
            missions = db.session.query(cls).filter(cls.launchDate.between(start_date, end_date)).all()
            return [{
                'id': mission.id,
                'name': mission.name,
                'launchDate': mission.launchDate,
                'destination': mission.destination,
                'missionStatus': mission.missionStatus.name,
                'crew': mission.crew,
                'payload': mission.payload,
                'duration': mission.duration,
                'cost': str(mission.cost), 
                'missionInfo': mission.missionInfo
            } for mission in missions]
        except Exception as e:
            print("Erro ao pesquisar missões por data:", e)

    """@classmethod
    def update_mission(cls, mission_id, name=None, launchDate=None, destination=None, missionStatus=None, crew=None, payload=None, duration=None, cost=None, missionInfo=None):
        try:
            mission = db.session.query(cls).filter(cls.id == mission_id).first()
            if not mission:
                return None

            if name is not None:
                mission.name = name
            if launchDate is not None:
                mission.launchDate = launchDate
            if destination is not None:
                mission.destination = destination
            if missionStatus is not None:
                mission.missionStatus = missionStatus
            if crew is not None:
                mission.crew = crew
            if payload is not None:
                mission.payload = payload
            if duration is not None:
                mission.duration = duration
            if cost is not None:
                mission.cost = cost 
            if missionInfo is not None:
                mission.missionInfo = missionInfo

            db.session.commit()
            return mission
        except Exception as e:
            print("Erro ao atualizar missão:", e)"""
    
    @classmethod
    def update_mission(cls, mission_id, **kwargs):
        try:
            mission = db.session.query(cls).filter(cls.id == mission_id).first()
            if not mission:
                return None

            # Mapeia os atributos permitidos
            allowed_updates = {
                'name': kwargs.get('name'),
                'launchDate': kwargs.get('launchDate'),
                'destination': kwargs.get('destination'),
                'missionStatus': kwargs.get('missionStatus'),
                'crew': kwargs.get('crew'),
                'payload': kwargs.get('payload'),
                'duration': kwargs.get('duration'),
                'cost': kwargs.get('cost'),
                'missionInfo': kwargs.get('missionInfo')
            }

            # Atualiza os atributos que não são None
            for key, value in allowed_updates.items():
                if value is not None:
                    setattr(mission, key, value)

            db.session.commit()
            return mission
        except Exception as e:
            print("Erro ao atualizar missão:", e)

    @classmethod
    def delete_mission(cls, mission_id):
        try:
            mission = db.session.query(cls).filter(cls.id == mission_id).first()
            if mission:
                db.session.delete(mission)
                db.session.commit()
            else:
                print("Missão não encontrada para exclusão.")
        except Exception as e:
            print("Não foi possível excluir a missão:", e)
