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

def delete_plugin(session, pluginId):
    plugin_to_delete = session.query(Plugin).filter(Plugin.id == pluginId).first()
    if plugin_to_delete:
        session.delete(plugin_to_delete)
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
        pluginId = None
        if 'body' in event:
            try:
                body = json.loads(event['body'])
                pluginId = body.get('pluginId')
            except (TypeError, ValueError) as e:
                pass
        else:
            pluginId = event.get('pluginId')

        with SessionLocal() as session:
            response = delete_plugin(session, pluginId)
            if response:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'responseMessage': f'Plugin with ID {pluginId} deleted successfully'
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({
                        'responseMessage': f'Plugin with ID {pluginId} not found'
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
