from src.database import db
from decimal import Decimal

class Missions(db.Model):

    __tablename__ = 'missions'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    launchDate = db.Column(db.Date)
    destination = db.Column(db.String(255))
    status = db.Column(db.String(255)) 
    crew = db.Column(db.String(255))
    payload = db.Column(db.String(255))
    duration = db.Column(db.String(255))
    cost = db.Column(db.Numeric(10, 2))  
    missionInfo = db.Column(db.String(500))

    def __init__(self, name, launchDate, destination, status, crew, payload, duration, cost, missionInfo):
        self.name = name
        self.launchDate = launchDate
        self.destination = destination
        self.status = status 
        self.crew = crew
        self.payload = payload
        self.duration = duration
        self.cost = cost  
        self.missionInfo = missionInfo

    @classmethod
    def create_mission(cls, name, launchDate, destination, status, crew, payload, duration, cost, missionInfo):
        try:
            new_mission = cls(
                name=name,
                launchDate=launchDate,
                destination=destination,
                status=status, 
                crew=crew,
                payload=payload,
                duration=duration,
                cost=Decimal(cost),
                missionInfo=missionInfo
            )

            db.session.add(new_mission)
            db.session.commit()
            return new_mission
        except ValueError as ve:
            print("Erro de validação:", ve)
            return {"status": 400, "msg": str(ve)} 
        except Exception as e:
            print("Erro ao criar missão:", e)
            db.session.rollback()
            return {"status": 500, "msg": "Erro interno ao criar missão"} 


    @classmethod
    def search_missions_by_date(cls, start_date, end_date):
        try:
            missions = db.session.query(cls).filter(cls.launchDate.between(start_date, end_date)).all()
            return [{
                'id': mission.id,
                'name': mission.name,
                'launchDate': mission.launchDate,
                'destination': mission.destination,
                'status': mission.status, 
                'crew': mission.crew,
                'payload': mission.payload,
                'duration': mission.duration,
                'cost': str(mission.cost), 
                'missionInfo': mission.missionInfo
            } for mission in missions]
        except Exception as e:
            print("Erro ao pesquisar missões por data:", e)
            return {"status": 500, "msg": "Erro interno ao pesquisar missões por data"}
    
    @classmethod
    def update_mission(cls, mission_id, **kwargs):
        try:
            mission = db.session.query(cls).filter(cls.id == mission_id).first()
            if not mission:
                return None

            if 'status' in kwargs and not isinstance(kwargs['status'], str):
                raise ValueError(f"Valor inválido para status: {kwargs['status']}")

            allowed_updates = {
                'name': kwargs.get('name'),
                'launchDate': kwargs.get('launchDate'),
                'destination': kwargs.get('destination'),
                'status': kwargs.get('status') if 'status' in kwargs else mission.status, 
                'crew': kwargs.get('crew'),
                'payload': kwargs.get('payload'),
                'duration': kwargs.get('duration'),
                'cost': kwargs.get('cost'),
                'missionInfo': kwargs.get('missionInfo')
            }

            for key, value in allowed_updates.items():
                if value is not None:
                    setattr(mission, key, value)

            db.session.commit()
            return mission
        except ValueError as ve:
            print("Erro de validação:", ve)
            return {"status": 400, "msg": str(ve)} 
        except Exception as e:
            print("Erro ao atualizar missão:", e)
            db.session.rollback()
            return {"status": 500, "msg": "Erro interno ao atualizar missão"}

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
            db.session.rollback()
