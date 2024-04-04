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

def add_assignment(session, primaryRuleId, conditionalRuleId):
    new_assignment = Assignment(primaryRuleId=primaryRuleId, conditionalRuleId=conditionalRuleId)
    session.add(new_assignment)
    session.commit()
    return new_assignment.id

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        primaryRuleId = conditionalRuleId = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                primaryRuleId = body.get('primaryRuleId')
                conditionalRuleId = body.get('conditionalRuleId')
            except (TypeError, ValueError) as e:
                pass
        else:
            primaryRuleId = event.get('primaryRuleId')
            conditionalRuleId = event.get('conditionalRuleId')

        with SessionLocal() as session:

            assignmentId = add_assignment(session, primaryRuleId, conditionalRuleId)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'id': assignmentId
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e)
            })
        }
