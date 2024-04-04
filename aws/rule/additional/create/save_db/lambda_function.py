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

def add_rule(session, name, description, pluginId, measurementUnit, value, comparisonOperator):
    new_rule = Rule(name=name, description=description, measurementUnit=measurementUnit, pluginId=pluginId, value=value, comparisonOperator=comparisonOperator)
    session.add(new_rule)
    session.commit()
    return new_rule.id

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        name = description = measurementUnit = pluginId = value = comparisonOperator = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                name = body.get('name')
                description = body.get('description')
                pluginId = body.get('pluginId')
                measurementUnit = body.get('measurementUnit')
                value = body.get('value')
                comparisonOperator = body.get('comparisonOperator')
            except (TypeError, ValueError) as e:
                pass
        else:
            name = event.get('name')
            description = event.get('description')
            pluginId = event.get('pluginId')
            measurementUnit = event.get('measurementUnit')
            value = event.get('value')
            comparisonOperator = event.get('comparisonOperator')

        with SessionLocal() as session:
            
            ruleId = add_rule(session, name, description, pluginId, measurementUnit, value, comparisonOperator)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'id': ruleId
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
