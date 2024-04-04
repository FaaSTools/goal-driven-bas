from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

Base = declarative_base()

class Logger(Base):
    __tablename__ = 'measurement_logger'
    id = Column(Integer, primary_key=True)
    pluginId = Column(Integer)
    invalidValue = Column(Integer)
    timestamp = Column(DateTime)

def get_all_logs(session):
    logs = session.query(Logger).all()
    return logs

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        engine = create_engine(db_connection_string)

        Session = sessionmaker(bind=engine)
        session = Session()
        with session:
            logs = get_all_logs(session)
            if len(logs) > 0:
                response = []
                for log in logs:
                    response.append({
                        'id': log.id,
                        'pluginId': log.pluginId,
                        'invalidValue': log.invalidValue,
                        'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    })
                return {
                    'statusCode': 202,
                    'headers': headers,
                    'body': json.dumps({'logs': response})
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
            'body': json.dumps({'message': f'Error when retrieving from database: {str(e)}'})
        }
