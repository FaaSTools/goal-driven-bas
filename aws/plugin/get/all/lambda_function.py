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

def get_all(session):
    plugins = session.query(Plugin).all()
    return plugins

def handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    try:
        with SessionLocal() as session:
            plugins = get_all(session)

            if len(plugins) > 0:
                response = []
                for plugin in plugins:
                    response.append({
                        'id': plugin.id,
                        'name': plugin.name,
                        'description': plugin.description,
                        'frequency': plugin.frequency,
                        'capacity': plugin.capacity,
                        'connectURL': plugin.connectURL
                    })
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'plugins': response})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'No plugins found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'header': headers,
            'body': json.dumps({'message': f'Error when retrieving from database: {str(e)}'})
        }
