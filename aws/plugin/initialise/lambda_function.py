from sqlalchemy import create_engine, Column, Integer, Double, String
from sqlalchemy.ext.declarative import declarative_base
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

Base = declarative_base()

class Plugin(Base):
    __tablename__ = 'plugin'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    frequency = Column(Double)
    capacity = Column(Integer)
    connectURL = Column(String(100))

def initialise_plugin_table(engine):
    Base.metadata.create_all(engine)
    

def handler(event, context):
    try:
        initialise_plugin_table(engine)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Plugin table initialised successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Error initialising plugin table'})
        }
