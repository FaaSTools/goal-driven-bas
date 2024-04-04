from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Logger(Base):
    __tablename__ = 'logger'
    id = Column(Integer, primary_key=True)
    ruleId = Column(Integer)
    description = Column(String(100))
    timestamp = Column(DateTime)

def create(session, ruleId, description, timestamp):
    new_log = Logger(ruleId=ruleId, description=description, timestamp=timestamp)
    session.add(new_log)
    session.commit()
    return new_log.id

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }
    try:
        ruleId = None
        description = None
        timestamp = None

        if 'body' in event:  
            try:
                body = json.loads(event['body'])
                ruleId = body.get('ruleId')
                description = body.get('description')
                timestamp = body.get('timestamp')
            except (TypeError, ValueError): 
                pluginId = None
        else:  
            ruleId = event.get('ruleId')
            description = event.get('description')
            timestamp = event.get('timestamp')

        with SessionLocal() as session:
            logId = create(session, ruleId, description, timestamp)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'responseMessage': f'Log with ID {logId} created successfully'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'responseMessage': f'Error creating log: {str(e)}'})
        }
