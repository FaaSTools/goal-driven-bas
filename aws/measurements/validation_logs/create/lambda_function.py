from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Logger(Base):
    __tablename__ = 'measurement_logger'
    id = Column(Integer, primary_key=True)
    pluginId = Column(Integer)
    invalidValue = Column(Integer)
    timestamp = Column(DateTime)

def create(session, pluginId, invalidValue, timestamp):
    new_log = Logger(pluginId=pluginId, invalidValue=invalidValue, timestamp=timestamp)
    session.add(new_log)
    session.commit()
    return new_log.id

def handler(event, context):
    try:
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        engine = create_engine(db_connection_string)

        Session = sessionmaker(bind=engine)
        session = Session()
        with session:
            pluginId = event.get('pluginId')
            invalidValue = event.get('invalidValue')
            timestamp = event.get('timestamp')
            
            logId = create(session, pluginId, invalidValue, timestamp)
            return {
                'statusCode': 200,
                'responseMessage': f'Log with ID {logId} created successfully'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'responseMessage': f'Error when creating log: {e}'
        }
