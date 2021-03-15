from flask import (
    Flask,
    render_template as render,
)
from flask_restful import reqparse, Api, Resource
from models import db, Sensor, RpiStatus
from datetime import date, time
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ubu-temp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('rpiId')
parser.add_argument('temp')
parser.add_argument('date')
parser.add_argument('time')

@app.errorhandler(404)
def page_not_found(e):
    return render('404.html'), 404

@app.route('/')
def home():
    rowCount = Sensor.query.count()
    months = list(map(
        lambda dtt : str(dtt[0].month),
        Sensor.query.group_by(func.strftime('%m', Sensor.date)).with_entities(Sensor.date).all()
    ))
    return render('index.html', rowCount=rowCount, months=months)

class addSensor(Resource):
    def post(self):
        args = parser.parse_args()
        rpiId = int(args.rpiId)
        temp = float(args.temp)
        d = list(map(int, args.date.split('-')))
        d = date(d[0], d[1], d[2])
        t = list(map(int, args.time.split(':')))
        t = time(t[0], t[1])
        sensor = Sensor(rpiId=rpiId, temp=temp, date=d, time=t)
        db.session.add(sensor)
        db.session.commit()
        return {
            'status': 'OK'
        }

class statusUpdate(Resource):
    def get(self, id):
        id = int(id)
        status = RpiStatus.query.get(id)
        status.updateStatus()
        db.session.add(status)
        db.session.commit()
        return {
            'status':'OK'
        }

class getStatus(Resource):
    def get(self):
        lastTemp = {
            'twc' : Sensor.query.filter(Sensor.rpiId == 1).order_by(Sensor.id.desc()).first(),
            'aa' : Sensor.query.filter(Sensor.rpiId == 2).order_by(Sensor.id.desc()).first(),
            'knw1' : Sensor.query.filter(Sensor.rpiId == 3).order_by(Sensor.id.desc()).first(),
            'knw2' : Sensor.query.filter(Sensor.rpiId == 4).order_by(Sensor.id.desc()).first()
        }
        return {
            "twc": [RpiStatus.query.get(1).isActive(), f'{lastTemp["twc"].temp}℃'],
            "aa": [RpiStatus.query.get(2).isActive(), f'{lastTemp["aa"].temp}℃'],
            "knw1": [RpiStatus.query.get(3).isActive(), f'{lastTemp["knw1"].temp}℃'],
            "knw2": [RpiStatus.query.get(4).isActive(), f'{lastTemp["knw2"].temp}℃'],
        }

class getSensorData(Resource):
    def get(self):
        sensor = Sensor.query.all()
        sensorjson = []
        
        for i in sensor:
            sensorjson.append({
                'rpiId': i.rpiId,
                'temp': i.temp,
                'date': int(i.date.strftime("%m")),
                'hour': int(i.time.strftime("%H")),
                'minute': int(i.time.strftime("%M"))
            })
        return { "sensors": sensorjson}
        

api.add_resource(addSensor, '/addsensor')
api.add_resource(statusUpdate, '/update/<id>')
api.add_resource(getStatus, '/getstatus')
api.add_resource(getSensorData, '/getdata')


if __name__ == '__main__':
    app.run(debug=True)