import re

validate_date = re.compile(r'\d{4}-\d{2}-\d{2}')
validate_int = re.compile(r'\d+')
validate_float = re.compile(r'\d+\.\d+')
validate_string = re.compile(r'\w+')


def validate_weather(weather):
    if not validate_int.match(weather.get('id')):
        return 'Invalid id', 400
    if not validate_string.match(weather.get('city')):
        return 'Invalid city', 400
    if not validate_date.match(weather.get('date')):
        return 'Invalid date', 400
    if not validate_float.match(weather.get('temperature')):
        return 'Invalid temperature', 400
    if not validate_int.match(weather.get('humidity')):
        return 'Invalid humidity', 400
    if not validate_string.match(weather.get('description')):
        return 'Invalid description', 400
    temperature = float(weather.get('temperature'))
    if temperature < -100 or temperature > 100:
        return 'Invalid temperature', 400
    humidity = float(weather.get('humidity'))
    if humidity < 0 or humidity > 100:
        return 'Invalid humidity', 400
    return None


def validate_event(event):
    if not validate_int.match(event.get('id')):
        return 'Invalid id', 400
    if not validate_string.match(event.get('city')):
        return 'Invalid city', 400
    if not validate_date.match(event.get('date')):
        return 'Invalid date', 400
    if not validate_string.match(event.get('description')):
        return 'Invalid description', 400
    if not validate_string.match(event.get('title')):
        return 'Invalid title', 400
    return None
