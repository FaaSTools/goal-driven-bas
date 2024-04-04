from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Assignment(Base):
    __tablename__ = 'plugin_iot_device_assignment'
    id = Column(Integer, primary_key=True)
    pluginId = Column(Integer)
    deviceId = Column(Integer)
    deviceConnectUrl = Column(String(100))

def get_assignments(session, pluginId):
    assignments = session.query(Assignment).filter(Assignment.pluginId == pluginId).all()
    return assignments

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
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
            pluginId = event.get('pluginId') if pluginId is None else pluginId

        with SessionLocal() as session:
            assignments = get_assignments(session, pluginId)
            if len(assignments) > 0:
                response = []
                for assignment in assignments:
                    response.append({
                        'id': assignment.id,
                        'pluginId': assignment.pluginId,
                        'deviceId': assignment.deviceId,
                        'deviceConnectUrl': assignment.deviceConnectUrl
                    })
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'assignments': response})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'No assignments found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': str(e)})
        }
