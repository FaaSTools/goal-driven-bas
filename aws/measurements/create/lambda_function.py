import os
import json
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    measurementUnit = Column(String(100))
    value = Column(Float)
    timestamp = Column(DateTime)
    pluginId = Column(Integer)

def add_measurement(session, measurementUnit, value, timestamp, pluginId):
    resolvedTimestamp = datetime.fromisoformat(timestamp)
    new_measurement = Measurement(
        measurementUnit=measurementUnit, value=value, timestamp=resolvedTimestamp, pluginId=pluginId
    )
    session.add(new_measurement)
    session.commit()
    return new_measurement.id

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }
    try:
        measurementUnit = None
        value = None
        timestamp = None
        pluginId = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                measurementUnit = body.get('measurementUnit')
                value = body.get('value')
                timestamp = body.get('timestamp')
                pluginId = body.get('pluginId')
            except (TypeError, ValueError):
                pass
        else:
            measurementUnit = event.get('measurementUnit')
            value = event.get('value')
            timestamp = event.get('timestamp')
            pluginId = event.get('pluginId')

        with SessionLocal() as session:
            measurementId = add_measurement(session, measurementUnit, value, timestamp, pluginId)
            if measurementId is not None:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'responseMessage': f'Measurement with ID {measurementId} created successfully'
                    })
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'responseMessage': f'Error when creating measurement: {str(e)}'})
        }
