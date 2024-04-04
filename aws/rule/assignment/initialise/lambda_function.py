from sqlalchemy import create_engine, Column, Integer
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

class Assignment(Base):
    __tablename__ = 'rules_assignment'
    id = Column(Integer, primary_key=True)
    primaryRuleId = Column(Integer)
    conditionalRuleId = Column(Integer)

def initialise_table(engine):
    Base.metadata.create_all(engine)
    

def handler(event, context):
    try:
        initialise_table(engine)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Assignment table initialized successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error when initializing assignment table: {e}'})
        }
