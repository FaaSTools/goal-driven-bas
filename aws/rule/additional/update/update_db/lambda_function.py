from sqlalchemy import create_engine, Column, Integer, Double, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

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

def update_rule(session, ruleId, name, description, measurementUnit, pluginId, value, comparisonOperator):
    rule_to_update = session.query(Rule).filter(Rule.id == ruleId).first()
    
    if rule_to_update:
        if name is not None:
            rule_to_update.name = name
        if description is not None:
            rule_to_update.description = description
        if measurementUnit is not None:
            rule_to_update.measurementUnit = measurementUnit
        if pluginId is not None:
            rule_to_update.pluginId = pluginId
        if value is not None:
            rule_to_update.value = value
        if comparisonOperator is not None:
            rule_to_update.comparisonOperator = comparisonOperator

        session.commit()
        return True
    else:
        return False

def handler(event, context):
    try:
        with SessionLocal() as session:
            ruleId = event.get('ruleId')
            name = event.get('name')
            description = event.get('description')
            measurementUnit = event.get('measurementUnit')
            pluginId = event.get('pluginId')
            value = event.get('value')
            comparisonOperator = event.get('comparisonOperator')

            response = update_rule(session, ruleId, name, description, measurementUnit, pluginId, value, comparisonOperator)
            if response:
                return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Rule updated successfully'})
            }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'Rule not found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e)
            })
        }
