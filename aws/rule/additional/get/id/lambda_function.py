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

def get_rule(session, ruleId):
    rule = session.query(Rule).filter(Rule.id == ruleId).first()
    return rule

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }
    try:
        ruleId = None

        if 'body' in event:  
            try:
                body = json.loads(event['body'])  
                ruleId = body.get('ruleId')
            except (TypeError, ValueError): 
                ruleId = None
        else:  
            ruleId = event.get('ruleId')
        
        with SessionLocal() as session:
            rule = get_rule(session, ruleId)
            if rule is not None:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'id': rule.id,
                        'name': rule.name,
                        'description': rule.description,
                        'measurementUnit': rule.measurementUnit,
                        'pluginId': rule.pluginId,
                        'value': rule.value,
                        'comparisonOperator': rule.comparisonOperator
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({
                        'message': 'Rule not found'
                    })
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'message': 'Internal server error'
            })
        }
