from sqlalchemy import create_engine, Column, Integer, Double, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import os
import json

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

Base = declarative_base()

class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    measurementUnit = Column(String(100))
    value = Column(Double)
    timestamp = Column(DateTime)
    pluginId = Column(Integer)

def initialise_table(engine):
    Base.metadata.create_all(engine)
    

def handler(event, context):
    try:
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')

        engine = create_engine(db_connection_string)
        initialise_table(engine)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Measurement table initialised successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Error initialising measurement table'})
        }
