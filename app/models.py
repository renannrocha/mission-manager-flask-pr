from . import db
from datetime import datetime

class Mission(db.Model):
    __tablename__ = 'missions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    crew = db.Column(db.String(200))
    payload = db.Column(db.String(200))
    duration = db.Column(db.String(50))
    cost = db.Column(db.Float)
    mission_status = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'launch_date': self.launch_date.strftime('%Y-%m-%d'),
            'destination': self.destination,
            'status': self.status,
            'crew': self.crew,
            'payload': self.payload,
            'duration': self.duration,
            'cost': self.cost,
            'mission_status': self.mission_status
        }
