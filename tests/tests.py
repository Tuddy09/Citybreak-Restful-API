import json
import os

import pytest

db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'root'
db_pw = os.environ.get('DB_PASSWORD') or '3039'


@pytest.fixture()
def app():
    from app import app

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_pw}@{db_host}/Citybreak'
    app.config['TESTING'] = True
    with app.app_context():
        from app import db
        db.create_all()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_get_event(client):
    response = client.get('/events?city=London')
    assert response.status_code == 200
    assert response.json[0] == {
        'id': 4,
        'city': 'London',
        'date': '2021-10-10',
        'title': 'London Marathon',
        'description': 'Annual marathon event'
    }


def test_get_event_invalid_city(client):
    response = client.get('/events?city=$$$')
    assert response.status_code == 400
    assert response.json == 'Invalid city'


def test_get_event_without_city(client):
    response = client.get('/events')
    assert response.status_code == 200


def test_post_event(client):
    response = client.post('/events', json={
        'id': '5',
        'city': 'London',
        'date': '2021-10-10',
        'title': 'London Marathon',
        'description': 'Annual marathon event'
    })
    assert response.json == 'OK'
    assert response.status_code == 201


def test_post_event_invalid_city(client):
    response = client.post('/events', json={
        'id': '5',
        'city': '$$$',
        'date': '2021-10-10',
        'title': 'London Marathon',
        'description': 'Annual marathon event'
    })
    assert response.status_code == 400
    assert response.json == 'Invalid city'


def test_put_event(client):
    response = client.put('/events?id=5', json={
        'id': '5',
        'city': 'London',
        'date': '2021-10-10',
        'title': 'London Marathon',
        'description': 'Annual marathon event'
    })
    assert response.status_code == 200


def test_delete_event(client):
    response = client.delete('/events?id=5')
    assert response.status_code == 200


def test_get_weather(client):
    response = client.get('/weather?city=London&date=2021-10-10')
    assert response.status_code == 200
    assert response.json[0] == {
        'id': 1,
        'city': 'London',
        'date': '2021-10-10',
        'temperature': 10.0,
        'humidity': 50,
        'description': 'Cloudy'
    }


def test_post_weather(client):
    response = client.post('/weather', json={
        'id': '4',
        'city': 'London',
        'date': '2021-10-10',
        'temperature': '10.0',
        'humidity': '50',
        'description': 'Cloudy'
    })
    assert response.json == 'OK'
    assert response.status_code == 201


def test_put_weather(client):
    response = client.put('/weather?id=4', json={
        'id': '4',
        'city': 'London',
        'date': '2021-10-10',
        'temperature': '10.0',
        'humidity': '50',
        'description': 'Cloudy'
    })
    assert response.json == 'OK'
    assert response.status_code == 200


def test_delete_weather(client):
    response = client.delete('/weather?id=4')
    assert response.status_code == 200
