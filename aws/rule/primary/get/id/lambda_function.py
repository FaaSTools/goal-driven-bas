from sqlalchemy import create_engine, Column, Integer, Time, String
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

class Rule(Base):
    __tablename__ = 'primary_rule'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    startTimeFrom = Column(Time)
    startTimeTo = Column(Time) 
    logicalOperator = Column(String(50))

def get_rule(session, ruleId):
    rule = session.query(Rule).filter(Rule.id == ruleId).first()
    return rule

def handler(event, context):
    try:
        with SessionLocal() as session:
            ruleId = event.get('ruleId')

            rule = get_rule(session, ruleId)
            if rule is not None:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'id': rule.id,
                        'name': rule.name,
                        'description': rule.description,
                        'startTimeFrom': rule.startTimeFrom.strftime('%H:%M:%S') if rule.startTimeFrom else 'N/A',
                        'startTimeTo': rule.startTimeTo.strftime('%H:%M:%S') if rule.startTimeTo else 'N/A',
                        'logicalOperator': rule.logicalOperator
                    })
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
            'body': json.dumps({'message': 'Internal server error'})
        }
