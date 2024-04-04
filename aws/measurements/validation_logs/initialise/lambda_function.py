from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class Logger(Base):
    __tablename__ = 'measurement_logger'
    id = Column(Integer, primary_key=True)
    pluginId = Column(Integer)
    invalidValue = Column(Integer)
    timestamp = Column(DateTime)

def initialise_table(engine):
    Base.metadata.create_all(engine)
    

def handler(event, context):
    try:
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        engine = create_engine(db_connection_string)
        initialise_table(engine)
        return {
            'statusCode': 200,
            'body': 'logger table initialized successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error when initializing logger table: {e}'
        }
