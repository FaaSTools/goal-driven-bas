from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

def get_assignment(session, pluginId, ruleId):
    assignment = session.query(Assignment).filter(Assignment.pluginId == pluginId, Assignment.primaryRuleId == ruleId).first()
    return assignment

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }
    try:
        pluginId = None
        ruleId = None

        if 'body' in event:  
            try:
                body = json.loads(event['body'])  
                pluginId = body.get('pluginId')
                ruleId = body.get('ruleId')
            except (TypeError, ValueError): 
                pluginId = None
        else:  
            pluginId = event.get('pluginId')
            ruleId = event.get('ruleId')

        with SessionLocal() as session:
            assignment = get_assignment(session, pluginId, ruleId)
            if assignment is not None:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'id': assignment.id,
                        'primaryRuleId': assignment.primaryRuleId,
                        'pluginId': assignment.pluginId,
                        'frequency': assignment.frequency
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({
                        'responseMessage': f'Assignment with rule id {ruleId} and plugin id {pluginId} not found'
                    })
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'responseMessage': f'Error when retrieving from database: {str(e)}'})
        }
