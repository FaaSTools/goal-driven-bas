from sqlalchemy import create_engine, Column, Integer, Double, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    measurementUnit = Column(String(100))
    value = Column(Double)
    timestamp = Column(DateTime)
    pluginId = Column(Integer)

def get_latest_measurement_by_plugin_id(session, pluginId):
    measurement = session.query(Measurement).filter(Measurement.pluginId == pluginId).order_by(Measurement.timestamp.desc()).first()
    return measurement

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }
    try:
        pluginId = None
        if 'body' in event:  
            try:
                body = json.loads(event['body'])  
                pluginId = body.get('pluginId')
            except (TypeError, ValueError): 
                pluginId = None
        else:  
            pluginId = event.get('pluginId')

        with SessionLocal() as session:
            measurement = get_latest_measurement_by_plugin_id(session, pluginId)
            if measurement is not None:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'id': measurement.id,
                        'measurementUnit': measurement.measurementUnit,
                        'value': measurement.value,
                        'timestamp': measurement.timestamp.isoformat(),
                        'pluginId': measurement.pluginId
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'responseMessage': f'No measurement found for plugin ID {pluginId}'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'responseMessage': f'Error when retrieving from database: {str(e)}'})
        }
