from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Assignment(Base):
    __tablename__ = 'plugin_rule_assignment'
    id = Column(Integer, primary_key=True)
    primaryRuleId = Column(Integer)
    pluginId = Column(Integer)
    frequency = Column(Integer)

def add_assignment(session, primaryRuleId, pluginId, frequency):
    existing_assignment = session.query(Assignment).filter_by(primaryRuleId=primaryRuleId, pluginId=pluginId).first()
    if existing_assignment:
        existing_assignment.frequency = frequency
        session.commit()
        return existing_assignment.id
    else:
        new_assignment = Assignment(primaryRuleId=primaryRuleId, pluginId=pluginId, frequency=frequency)
        session.add(new_assignment)
        session.commit()
        return new_assignment.id

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                primaryRuleId = body.get('primaryRuleId')
                pluginId = body.get('pluginId')
                frequency = body.get('frequency')
            except (TypeError, ValueError) as e:
                pass
        else:
            primaryRuleId = event.get('primaryRuleId')
            pluginId = event.get('pluginId')
            frequency = event.get('frequency')

        with SessionLocal() as session:
            id = add_assignment(session, primaryRuleId, pluginId, frequency)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'id': id
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error: {e}'})
        }
