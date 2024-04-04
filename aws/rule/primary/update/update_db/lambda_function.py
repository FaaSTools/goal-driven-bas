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

def update_rule(session, ruleId, name, description, startTimeFrom=None, startTimeTo=None, logicalOperator=None):
    rule_to_update = session.query(Rule).filter(Rule.id == ruleId).first()
    
    if rule_to_update:
        if name is not None:
            rule_to_update.name = name
        if description is not None:
            rule_to_update.description = description
        if startTimeFrom is not None:
            rule_to_update.startTimeFrom = startTimeFrom
        if startTimeTo is not None:
            rule_to_update.startTimeTo = startTimeTo
        if logicalOperator is not None:
            rule_to_update.logicalOperator = logicalOperator

        session.commit()
        return True
    else:
        return False

def handler(event, context):
    try:
        ruleId = name = description = startTimeFrom = startTimeTo = logicalOperator = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                ruleId = body.get('ruleId')
                name = body.get('name')
                description = body.get('description')
                startTimeFrom = body.get('startTimeFrom')
                startTimeTo = body.get('startTimeTo')
                logicalOperator = body.get('logicalOperator')
            except (TypeError, ValueError) as e:
                pass
        else:
            ruleId = event.get('ruleId')
            name = event.get('name')
            description = event.get('description')
            startTimeFrom = event.get('startTimeFrom')
            startTimeTo = event.get('startTimeTo')
            logicalOperator = event.get('logicalOperator')

        with SessionLocal() as session:
            response = update_rule(session, ruleId, name, description, startTimeFrom, startTimeTo, logicalOperator)
            if response:
                return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': f'Rule with ID {ruleId} updated successfully'})
            }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': f'Rule with ID {ruleId} not found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e)
            })
        }
