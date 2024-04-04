from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Assignment(Base):
    __tablename__ = 'plugin_rule_assignment'
    id = Column(Integer, primary_key=True)
    primaryRuleId = Column(Integer)
    pluginId = Column(Integer)
    frequency = Column(Integer)

def get_assignments(session, primaryRuleId):
    assignments = session.query(Assignment).filter(Assignment.primaryRuleId == primaryRuleId).all()
    return assignments

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        
        primaryRuleId = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                primaryRuleId = body.get('primaryRuleId')
            except (TypeError, ValueError) as e:
                pass
        else:
            primaryRuleId = event.get('primaryRuleId')
        
        with SessionLocal() as session:
            assignments = get_assignments(session, primaryRuleId)
            if len(assignments) > 0:
                response = []
                for assignment in assignments:
                    response.append({
                        'id': assignment.id,
                        'primaryRuleId': assignment.primaryRuleId,
                        'pluginId': assignment.pluginId,
                        'frequency': assignment.frequency
                    })
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(response)
                }
            elif len(assignments) == 0:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps([])
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'Rule not found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error: {e}'})
        }
