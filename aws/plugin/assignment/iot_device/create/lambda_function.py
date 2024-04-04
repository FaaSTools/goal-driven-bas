from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

Base = declarative_base()

class Assignment(Base):
    __tablename__ = 'plugin_iot_device_assignment'
    id = Column(Integer, primary_key=True)
    pluginId = Column(Integer)
    deviceId = Column(Integer)
    deviceConnectUrl = Column(String(100))

def add_assignment(session, pluginId, deviceId, deviceConnectUrl):
    new_assignment = Assignment(pluginId=pluginId, deviceId=deviceId, deviceConnectUrl=deviceConnectUrl)
    session.add(new_assignment)
    session.commit()
    return new_assignment.id

def handler(event, context):
    try:
        with SessionLocal() as session:
            pluginId = event.get('pluginId')
            deviceId = event.get('deviceId')
            deviceConnectUrl = event.get('deviceConnectUrl')

            assignment_id = add_assignment(session, pluginId, deviceId, deviceConnectUrl)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'id': assignment_id})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': str(e)})
        }
