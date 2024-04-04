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

class Plugin(Base):
    __tablename__ = 'plugin'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    frequency = Column(Double)
    capacity = Column(Integer)
    connectURL = Column(String(100))

def get_plugin(session, pluginId):
    plugin = session.query(Plugin).filter(Plugin.id == pluginId).first()
    return plugin

def handler(event, context):
    try:
        with SessionLocal() as session:
            pluginId = event.get('pluginId')

            plugin = get_plugin(session, pluginId)
            if plugin is not None:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'plugin': {
                        'id': plugin.id,
                        'name': plugin.name,
                        'description': plugin.description,
                        'frequency': plugin.frequency,
                        'capacity': plugin.capacity,
                        'connectURL': plugin.connectURL
                    }})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'Plugin not found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Error getting plugin'})
        }
