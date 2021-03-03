from flask import (
    Flask,
    render_template as render
)
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
    rowCount = Sensor.query.count()
    return render('index.html', rowCount=rowCount)

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
        return {
            "twc": RpiStatus.query.get(1).isActive(),
            "aa": RpiStatus.query.get(2).isActive(),
            "knw1": RpiStatus.query.get(3).isActive(),
            "knw2": RpiStatus.query.get(4).isActive(),
        }

api.add_resource(addSensor, '/addsensor')
api.add_resource(statusUpdate, '/update/<id>')
api.add_resource(getStatus, '/getstatus')


if __name__ == '__main__':
    app.run(debug=True)