from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rpiId = db.Column(db.Integer, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'Rpi : {self.rpiId} {self.date} - {self.time}'
        
class RpiStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lastActive = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'{self.name} status'


    def isActive(self):
        now = datetime.now()
        timediff = (now - self.lastActive).total_second()
        if timediff > 60:
            return f'Offline'
        else:
            return f'Online'
    
    def updateStatus(self):
        self.lastActive = datetime.now()
         
