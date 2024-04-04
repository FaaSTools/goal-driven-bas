from sqlalchemy import create_engine, Column, Integer, String, Double, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json
from datetime import datetime

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

def get_all_measurements(session):
    measurements = session.query(Measurement).order_by(desc(Measurement.id)).limit(100).all()
    return measurements

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        with SessionLocal() as session:
            measurements = get_all_measurements(session)
            if len(measurements) > 0:
                response = []
                for measurement in measurements:
                    timestamp = measurement.timestamp
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
                        except ValueError:
                            continue
                    response.append({
                        'id': measurement.id,
                        'measurementUnit': measurement.measurementUnit,
                        'value': measurement.value,
                        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
                        'pluginId': measurement.pluginId
                    })

                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'measurements': response})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'No measurements found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error when retrieving from database: {str(e)}'})
        }
