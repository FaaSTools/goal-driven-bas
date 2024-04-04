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

def delete_rule(session, ruleId):
    rule_to_delete = session.query(Rule).filter(Rule.id == ruleId).first()
    if rule_to_delete:
        session.delete(rule_to_delete)
        session.commit()
        return True
    else:
        return False

def handler(event, context):
    try:
        with SessionLocal() as session:
            ruleId = event.get('ruleId')

            response = delete_rule(session, ruleId)
            if response:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'message': 'Rule deleted successfully'})
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
            'body': json.dumps({'message': f'Error when deleting rule: {e}'})
        }
