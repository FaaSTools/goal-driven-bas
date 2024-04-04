from sqlalchemy import create_engine, Column, Integer, Double, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

Base = declarative_base()

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

class MeasurementLimit(Base):
    __tablename__ = 'measurement_limit'
    id = Column(Integer, primary_key=True)
    pluginId = Column(Integer)
    valueMax = Column(Double)
    valueMin = Column(Double)

def add_limit(session, pluginId, valueMax, valueMin):
    new_limit = MeasurementLimit(pluginId=pluginId, valueMax=valueMax, valueMin=valueMin)
    session.add(new_limit)
    session.commit()
    return new_limit.id

def handler(event, context):
    try:
        with SessionLocal() as session:
            pluginId = event.get('pluginId')
            valueMax = event.get('valueMax')
            valueMin = event.get('valueMin')
            
            limitId = add_limit(session, pluginId, valueMax, valueMin)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'id': limitId})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': str(e)})
        }
