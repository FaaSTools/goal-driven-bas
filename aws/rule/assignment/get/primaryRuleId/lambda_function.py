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
    __tablename__ = 'rules_assignment'
    id = Column(Integer, primary_key=True)
    primaryRuleId = Column(Integer)
    conditionalRuleId = Column(Integer)

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
        with SessionLocal() as session:
            if 'body' in event: 
                try:
                    body = json.loads(event['body'])
                    primaryRuleId = body.get('primaryRuleId')
                except (TypeError, ValueError):
                    primaryRuleId = None
            else:
                primaryRuleId = event.get('primaryRuleId')

            assignments = get_assignments(session, primaryRuleId)
            if len(assignments) > 0:
                response = []
                for assignment in assignments:
                    response.append({
                        'id': assignment.id,
                        'primaryRuleId': assignment.primaryRuleId,
                        'conditionalRuleId': assignment.conditionalRuleId
                    })
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'assignments': response})
                }
            elif len(assignments) == 0:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'assignments': []})
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
