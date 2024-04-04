from sqlalchemy import create_engine, Column, Integer, Time, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json
from datetime import datetime

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'primary_rule'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    startTimeFrom = Column(Time)
    startTimeTo = Column(Time) 
    logicalOperator = Column(String(50))

def get_all_rules(session):
    rules = session.query(Rule).order_by(Rule.startTimeFrom.asc()).all()
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
            if len(rules) > 0:
                response = []
                for rule in rules:
                    timestampFrom = 'N/A'
                    timestampTo = 'N/A'

                    if rule.startTimeFrom is not None:
                        if isinstance(rule.startTimeFrom, str):
                            timestampFrom = datetime.strptime(rule.startTimeFrom, '%H:%M:%S')
                        else:
                            timestampFrom = rule.startTimeFrom.strftime('%H:%M:%S')

                    if rule.startTimeTo is not None:
                        if isinstance(rule.startTimeTo, str):
                            timestampTo = datetime.strptime(rule.startTimeTo, '%H:%M:%S')
                        else:
                            timestampTo = rule.startTimeTo.strftime('%H:%M:%S')
                    
                    response.append({
                        'id': rule.id,
                        'name': rule.name,
                        'description': rule.description,
                        'startTimeFrom': timestampFrom,
                        'startTimeTo': timestampTo,
                        'logicalOperator': rule.logicalOperator
                    })
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'rules': response})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'No rules found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': str(e)})
        }
