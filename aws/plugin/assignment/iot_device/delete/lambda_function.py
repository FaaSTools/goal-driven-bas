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

def delete_assignment(session, pluginId):
    assignment_to_delete = session.query(Assignment).filter(Assignment.pluginId == pluginId).first()
    if assignment_to_delete:
        session.delete(assignment_to_delete)
        session.commit()
        return True
    else:
        return False

def handler(event, context):
    try:
        with SessionLocal() as session:
            pluginId = event.get('pluginId')

            response = delete_assignment(session, pluginId)
            if response:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'message': 'Assignment deleted successfully'})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'Assignment not found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': str(e)})
        }
