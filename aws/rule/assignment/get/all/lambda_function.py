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
    __tablename__ = 'rules_assignment'
    id = Column(Integer, primary_key=True)
    primaryRuleId = Column(Integer)
    conditionalRuleId = Column(Integer)

def get_all_assignments(session):
    assignments = session.query(Assignment).all()
    return assignments

def handler(event, context):
    try:
        with SessionLocal() as session:
            conditionalRuleId = event.get('conditionRuleId')

            assignments = get_all_assignments(session)
            if assignments:
                assignments_list = []
                for assignment in assignments:
                    assignments_list.append({
                        'id': assignment.id,
                        'primaryRuleId': assignment.primaryRuleId,
                        'conditionalRuleId': assignment.conditionalRuleId
                    })
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'assignments': assignments_list
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
            'body': json.dumps({'message': f'Error when getting assignments: {e}'})
        }
