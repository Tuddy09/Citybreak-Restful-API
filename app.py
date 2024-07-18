import os
from datetime import datetime
from validations import *
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'root'
db_pw = os.environ.get('DB_PASSWORD') or '3039'
db_url = f'mysql://{db_user}:{db_pw}@{db_host}/Citybreak'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)
api = Api(app)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))

    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if '_state' not in k:
                d[k] = self.__dict__[k] if k != 'date' else self.__dict__[k].strftime('%Y-%m-%d')
        return d


class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def to_dict(self):
        d = {}
        for k in self.__dict__.keys():
            if '_state' not in k:
                d[k] = self.__dict__[k] if k != 'date' else self.__dict__[k].strftime('%Y-%m-%d')
        return d


with app.app_context():
    db.create_all()


class WeatherController(Resource):
    def get(self):
        try:
            city = request.args.get('city')
            date = request.args.get('date')
            if city and date:
                if not validate_date.match(date):
                    return 'Invalid date', 400
                if not validate_string.match(city):
                    return 'Invalid city', 400
                data = db.session.query(Weather).filter_by(city=city, date=datetime.strptime(date, '%Y-%m-%d')).all()
                return [d.to_dict() for d in data]
            else:
                data = db.session.query(Weather).all()
                return [d.to_dict() for d in data]
        except Exception as e:
            return str(e), 500

    def post(self):
        try:
            data = request.get_json()
            id = data.get('id')
            city = data.get('city')
            date = data.get('date')
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            description = data.get('description')
            w = Weather(id=id, city=city, date=date, temperature=temperature, humidity=humidity,
                        description=description)
            if error := validate_weather(data):
                return error
            db.session.add(w)
            db.session.commit()
            return 'OK', 201
        except Exception as e:
            return str(e), 500

    def put(self):
        try:
            weather_id = request.args.get('id')
            if not validate_int.match(weather_id):
                return 'Invalid id', 400
            w = db.session.query(Weather).filter_by(id=weather_id).first()
            data = request.get_json()
            w.city = data.get('city')
            w.date = data.get('date')
            w.temperature = data.get('temperature')
            w.humidity = data.get('humidity')
            w.description = data.get('description')
            if error := validate_weather(data):
                return error
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500

    def delete(self):
        try:
            weather_id = request.args.get('id')
            if not validate_int.match(weather_id):
                return 'Invalid id', 400
            w = db.session.query(Weather).filter_by(id=weather_id).first()
            db.session.delete(w)
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500


class EventController(Resource):
    def get(self):
        try:
            city = request.args.get('city')
            if city:
                if not validate_string.match(city):
                    return 'Invalid city', 400
                data = db.session.query(Event).filter_by(city=city).all()
                return [d.to_dict() for d in data]
            else:
                data = db.session.query(Event).all()
                return [d.to_dict() for d in data]
        except Exception as e:
            return str(e), 500

    def post(self):
        try:
            data = request.get_json()
            id = data.get('id')
            city = data.get('city')
            date = data.get('date')
            title = data.get('title')
            description = data.get('description')
            e = Event(id=id, city=city, date=date, title=title, description=description)
            if error := validate_event(data):
                return error
            db.session.add(e)
            db.session.commit()
            return 'OK', 201
        except Exception as e:
            return str(e), 500

    def put(self):
        try:
            event_id = request.args.get('id')
            if not validate_int.match(event_id):
                return 'Invalid id', 400
            e = db.session.query(Event).filter_by(id=event_id).first()
            data = request.get_json()
            e.city = data.get('city')
            e.date = data.get('date')
            e.title = data.get('title')
            e.description = data.get('description')
            if error := validate_event(data):
                return error
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500

    def delete(self):
        try:
            event_id = request.args.get('id')
            if not validate_int.match(event_id):
                return 'Invalid id', 400
            e = db.session.query(Event).filter_by(id=event_id).first()
            db.session.delete(e)
            db.session.commit()
            return 'OK', 200
        except Exception as e:
            return str(e), 500


api.add_resource(EventController, '/events')
api.add_resource(WeatherController, '/weather')

if __name__ == '__main__':
    app.run()
