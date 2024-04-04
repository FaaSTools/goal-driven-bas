from sqlalchemy import create_engine, Column, Integer, Time, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json
from datetime import datetime

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

def add_rule(session, name, description, startTimeFrom, startTimeTo, logicalOperator):
    new_rule = Rule(name=name, description=description, startTimeFrom=startTimeFrom, startTimeTo=startTimeTo, logicalOperator=logicalOperator)
    session.add(new_rule)
    session.commit()
    return new_rule.id

def handler(event, context):
    try:
        name = description = startTimeFrom = startTimeTo = logicalOperator = None

        if 'body' in event:
            try:
                body = json.loads(event['body'])
                name = body.get('name')
                description = body.get('description')
                startTimeFrom = body.get('startTimeFrom')
                startTimeTo = body.get('startTimeTo')
                logicalOperator = body.get('logicalOperator')
            except (TypeError, ValueError) as e:
                pass
        else:
            name = event.get('name')
            description = event.get('description')
            startTimeFrom = event.get('startTimeFrom')
            startTimeTo = event.get('startTimeTo')
            logicalOperator = event.get('logicalOperator')

        with SessionLocal() as session:
            startTimeFromTime = datetime.strptime(startTimeFrom, '%H:%M:%S').time() if startTimeFrom else None
            startTimeToTime = datetime.strptime(startTimeTo, '%H:%M:%S').time() if startTimeTo else None

            ruleId = add_rule(session, name, description, startTimeFromTime, startTimeToTime, logicalOperator)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'id': ruleId})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
