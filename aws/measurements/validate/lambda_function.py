from sqlalchemy import create_engine, Column, Integer, Double, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import os
from datetime import datetime
import pytz
import json

CURR_TIME = datetime.now(pytz.timezone('Europe/Vienna')).time()

Base = declarative_base()

class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    measurementUnit = Column(String(100))
    value = Column(Double)
    timestamp = Column(DateTime)
    pluginId = Column(Integer)

def add_measurement(session, measurementUnit, value, timestamp, pluginId):
    new_measurement = Measurement(measurementUnit=measurementUnit, value=value, timestamp=timestamp, pluginId=pluginId)
    session.add(new_measurement)
    session.commit()
    return new_measurement.id

def validate_measurement_value(value, pluginId):
    url = 'http://measurements_limits_get_plugin_id:8080/2015-03-31/functions/function/invocations' 
    
    payload = {
        'pluginId': pluginId
    }
    headers = {'Content-Type': 'application/json'} 
    response = requests.post(url, json=payload, headers=headers)
    limit = response.json()
    maxVal = limit.get('valueMax')
    minVal = limit.get('valueMin')
    return value >= minVal and value <= maxVal

def log_invalid_measurement(value, pluginId):
    url = 'http://measurements_validation_logs_create:8080/2015-03-31/functions/function/invocations' 
    data = {
        'pluginId': pluginId,
        'invalidValue': value,
        'timestamp': datetime.now(pytz.timezone('Europe/Vienna')).strftime('%Y-%m-%d %H:%M:%S')
    }
    response = requests.post(url, json=data)
    return response.json()

def handler(event, context):
    try:
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        engine = create_engine(db_connection_string)


        Session = sessionmaker(bind=engine)
        session = Session()
        with session:
            measurementUnit = event.get('measurementUnit')
            value = event.get('value')
            timestamp = event.get('timestamp')
            pluginId = event.get('pluginId')
            
            measurementId = add_measurement(session, measurementUnit, value, timestamp, pluginId)

            if not validate_measurement_value(value, pluginId):
                log_invalid_measurement(value, pluginId)
                # notify system admin
                return {
                    'statusCode': 200,
                    'responseMessage': f'Measurement with ID {measurementId} created successfully, but value is invalid'
                }

            return {
                'statusCode': 200,
                'responseMessage': f'Measurement with ID {measurementId} created successfully'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error when creating measurement: {e}'
        }
