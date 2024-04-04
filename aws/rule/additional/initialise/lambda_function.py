from sqlalchemy import create_engine, Column, Integer, Double, String
from sqlalchemy.ext.declarative import declarative_base
import os
import json

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'conditional_rule'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    measurementUnit = Column(String(100))
    pluginId = Column(Integer)
    value = Column(Double)
    comparisonOperator = Column(String(50))

def initialise_rule_table(engine):
    Base.metadata.create_all(engine)
    

def handler(event, context):
    try:
        initialise_rule_table(engine)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Rule table initialized successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error when initializing rule table: {e}'})
        }
