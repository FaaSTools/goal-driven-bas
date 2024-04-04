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

def get_latest(session):
    log = session.query(Logger).order_by(Logger.id.desc()).first()
    return log

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        with SessionLocal() as session:
            log = get_latest(session)
            if log is not None:
                response = {
                    'id': log.id,
                    'ruleId': log.ruleId,
                    'description': log.description,
                    'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(response)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'No logs found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': str(e)})
        }
