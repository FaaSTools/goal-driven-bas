from sqlalchemy import create_engine, Column, Integer
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
    __tablename__ = 'plugin_rule_assignment'
    id = Column(Integer, primary_key=True)
    primaryRuleId = Column(Integer)
    pluginId = Column(Integer)
    frequency = Column(Integer)

def delete_assignments(session, pluginId):
    assignments_to_delete = session.query(Assignment).filter(Assignment.pluginId == pluginId).all()
    if len(assignments_to_delete) > 0:
        for assignment in assignments_to_delete:
            session.delete(assignment)
        session.commit()
        return True
    else:
        return False

def handler(event, context):
    try:
        with SessionLocal() as session:
            pluginId = event.get('pluginId')

            response = delete_assignments(session, pluginId)
            if response:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'responseMessage': f'Assignments for plugin with ID {pluginId} deleted successfully'
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'Assignments not found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Internal server error'})
        }
