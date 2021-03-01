from re import template
from flask import Flask
from flask_restful import reqparse, Api, Resource
from models import db, Sensor, RpiStatus
from datetime import date, time

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

@app.route('/')
def home():
    x = Sensor.query.all()
    return f'{x}'

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

api.add_resource(addSensor, '/addsensor')


if __name__ == '__main__':
    app.run(debug=True)