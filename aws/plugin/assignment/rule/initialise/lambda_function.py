from sqlalchemy import create_engine, Column, Integer
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

class Assignment(Base):
    __tablename__ = 'plugin_rule_assignment'
    id = Column(Integer, primary_key=True)
    primaryRuleId = Column(Integer)
    pluginId = Column(Integer)
    frequency = Column(Integer)

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
            'body': json.dumps({'message': 'Rule table initialised successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Error initialising rule table'})
        }
