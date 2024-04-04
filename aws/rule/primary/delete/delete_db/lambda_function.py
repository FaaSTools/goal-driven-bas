from sqlalchemy import create_engine, Column, Integer, Time, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'primary_rule'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    startTimeFrom = Column(Time)
    startTimeTo = Column(Time) 
    logicalOperator = Column(String(50))

def delete_rule(session, ruleId):
    rule_to_delete = session.query(Rule).filter(Rule.id == ruleId).first()
    if rule_to_delete:
        session.delete(rule_to_delete)
        session.commit()
        return True
    else:
        return False

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        ruleId = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                ruleId = body.get('ruleId')
            except (TypeError, ValueError) as e:
                pass
        else:
            ruleId = event.get('ruleId')

        with SessionLocal() as session:
            response = delete_rule(session, ruleId)
            if response:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'message': 'Rule deleted successfully'})
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
            'body': json.dumps({
                'error': str(e)
            })
        }
