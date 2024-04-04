from sqlalchemy import create_engine, Column, Integer, Double, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

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

def get_all_rules(session):
    rules = session.query(Rule).all()
    return rules

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        with SessionLocal() as session:
            rules = get_all_rules(session)
            response = []
            for rule in rules:
                response.append({
                    'id': rule.id,
                    'name': rule.name,
                    'description': rule.description,
                    'measurementUnit': rule.measurementUnit,
                    'pluginId': rule.pluginId,
                    'value': rule.value,
                    'comparisonOperator': rule.comparisonOperator
                })
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'rules': response})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers, 
            'body': json.dumps({'message': str(e)})
        }
