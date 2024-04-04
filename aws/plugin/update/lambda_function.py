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

def update_plugin(session, pluginId, name, description, frequency, capacity, connectURL):
    plugin_to_update = session.query(Plugin).filter(Plugin.id == pluginId).first()
    
    if plugin_to_update:
        if name is not None:
            plugin_to_update.name = name
        if description is not None: 
            plugin_to_update.description = description
        if frequency is not None:
            plugin_to_update.frequency = frequency
        if capacity is not None:
            plugin_to_update.capacity = capacity
        if connectURL is not None:
            plugin_to_update.connectURL = connectURL

        session.commit()
        return True
    else:
        return False

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        pluginId = name = description = frequency = capacity = connectURL = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                pluginId = body.get('pluginId')
                name = body.get('name')
                description = body.get('description')
                frequency = body.get('frequency')
                capacity = body.get('capacity')
                connectURL = body.get('connectURL')
            except (TypeError, ValueError) as e:
                pass
        else:
            pluginId = event.get('pluginId')
            name = event.get('name')
            description = event.get('description')
            frequency = event.get('frequency')
            capacity = event.get('capacity')
            connectURL = event.get('connectURL')

        with SessionLocal() as session:
            response = update_plugin(session, pluginId, name, description, frequency, capacity, connectURL)
            if response:
                return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'id': pluginId})
            }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'error': f'Plugin with id {pluginId} not found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
