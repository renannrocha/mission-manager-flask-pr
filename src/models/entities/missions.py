from src.database import db
from src.models.enum.missionStatus import MissionStatus
from decimal import Decimal

class Missions(db.Model):

    __tablename__ = 'missions'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    missionName = db.Column(db.String(255))
    releaseDate = db.Column(db.Date)
    destination = db.Column(db.String(255))
    missionStatus = db.Column(db.Enum(MissionStatus))
    tripulation = db.Column(db.String(255))
    payload = db.Column(db.String(255))
    missionDuration = db.Column(db.Date)
    missionCost = db.Column(db.Numeric(10, 2))  
    missionInfoStatus = db.Column(db.String(255))

    def __init__(self, missionName, releaseDate, destination, missionStatus, tripulation, payload, missionDuration, missionCost, missionInfoStatus):
        self.missionName = missionName
        self.releaseDate = releaseDate
        self.destination = destination
        self.missionStatus = missionStatus
        self.tripulation = tripulation
        self.payload = payload
        self.missionDuration = missionDuration
        self.missionCost = missionCost  
        self.missionInfoStatus = missionInfoStatus

    @classmethod
    def create_mission(cls, missionName, releaseDate, destination, missionStatus, tripulation, payload, missionDuration, missionCost, missionInfoStatus):
        try:
            new_mission = cls(
                missionName,
                releaseDate,
                destination,
                missionStatus,
                tripulation,
                payload,
                missionDuration,
                missionCost,  
                missionInfoStatus
            )
            db.session.add(new_mission)
            db.session.commit()
            return new_mission
        except Exception as e:
            print("Erro ao criar missão:", e)

    @classmethod
    def get_missions(cls):
        try:
            missions = db.session.query(cls).order_by(cls.releaseDate.desc()).all()
            return [{
                'id': mission.id,
                'missionName': mission.missionName,
                'releaseDate': mission.releaseDate,
                'destination': mission.destination,
                'missionStatus': mission.missionStatus.name,
                'tripulation': mission.tripulation,
                'payload': mission.payload,
                'missionDuration': mission.missionDuration,
                'missionCost': str(mission.missionCost), 
                'missionInfoStatus': mission.missionInfoStatus
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
                    'missionName': mission.missionName,
                    'releaseDate': mission.releaseDate,
                    'destination': mission.destination,
                    'missionStatus': mission.missionStatus.name,
                    'tripulation': mission.tripulation,
                    'payload': mission.payload,
                    'missionDuration': mission.missionDuration,
                    'missionCost': str(mission.missionCost),  
                    'missionInfoStatus': mission.missionInfoStatus
                }
            return None
        except Exception as e:
            print("Erro ao obter missão:", e)

    @classmethod
    def search_missions_by_date(cls, start_date, end_date):
        try:
            missions = db.session.query(cls).filter(cls.releaseDate.between(start_date, end_date)).all()
            return [{
                'id': mission.id,
                'missionName': mission.missionName,
                'releaseDate': mission.releaseDate,
                'destination': mission.destination,
                'missionStatus': mission.missionStatus.name,
                'tripulation': mission.tripulation,
                'payload': mission.payload,
                'missionDuration': mission.missionDuration,
                'missionCost': str(mission.missionCost), 
                'missionInfoStatus': mission.missionInfoStatus
            } for mission in missions]
        except Exception as e:
            print("Erro ao pesquisar missões por data:", e)

    """@classmethod
    def update_mission(cls, mission_id, missionName=None, releaseDate=None, destination=None, missionStatus=None, tripulation=None, payload=None, missionDuration=None, missionCost=None, missionInfoStatus=None):
        try:
            mission = db.session.query(cls).filter(cls.id == mission_id).first()
            if not mission:
                return None

            if missionName is not None:
                mission.missionName = missionName
            if releaseDate is not None:
                mission.releaseDate = releaseDate
            if destination is not None:
                mission.destination = destination
            if missionStatus is not None:
                mission.missionStatus = missionStatus
            if tripulation is not None:
                mission.tripulation = tripulation
            if payload is not None:
                mission.payload = payload
            if missionDuration is not None:
                mission.missionDuration = missionDuration
            if missionCost is not None:
                mission.missionCost = missionCost 
            if missionInfoStatus is not None:
                mission.missionInfoStatus = missionInfoStatus

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
                'missionName': kwargs.get('missionName'),
                'releaseDate': kwargs.get('releaseDate'),
                'destination': kwargs.get('destination'),
                'missionStatus': kwargs.get('missionStatus'),
                'tripulation': kwargs.get('tripulation'),
                'payload': kwargs.get('payload'),
                'missionDuration': kwargs.get('missionDuration'),
                'missionCost': kwargs.get('missionCost'),
                'missionInfoStatus': kwargs.get('missionInfoStatus')
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
