from sqlalchemy import create_engine, Column, Integer, Double, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import json

db_connection_string = os.environ.get('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Plugin(Base):
    __tablename__ = 'plugin'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    frequency = Column(Double)
    capacity = Column(Integer)
    connectURL = Column(String(100))

def add_plugin(session, name, description, frequency, capacity, connectURL):
    new_plugin = Plugin(name=name, description=description, frequency=frequency, capacity=capacity, connectURL=connectURL)
    session.add(new_plugin)
    session.commit()
    return new_plugin.id

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        name = description = connectURL = frequency = capacity = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                name = body.get('name')
                description = body.get('description')
                frequency = body.get('frequency')
                capacity = body.get('capacity')
                connectURL = body.get('connectURL')
            except (TypeError, ValueError) as e:
                pass
        else:
            name = event.get('name')
            description = event.get('description')
            frequency = event.get('frequency')
            capacity = event.get('capacity')
            connectURL = event.get('connectURL')

        with SessionLocal() as session:
            pluginId = add_plugin(session, name, description, frequency, capacity, connectURL)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'id': pluginId
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e)
            })
        }
