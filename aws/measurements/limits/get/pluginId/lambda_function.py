from sqlalchemy import create_engine, Column, Integer, Double, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

class MeasurementLimit(Base):
    __tablename__ = 'measurement_limit'
    id = Column(Integer, primary_key=True)
    pluginId = Column(Integer)
    valueMax = Column(Double)
    valueMin = Column(Double)

def get_limit_by_plugin_id(session, pluginId):
    limit = session.query(MeasurementLimit).filter(MeasurementLimit.pluginId == pluginId).first()
    return limit

def handler(event, context):
    try:
        pluginId = None
        if 'body' in event:  
            try:
                body = json.loads(event['body'])  
                pluginId = body.get('pluginId')
            except (TypeError, ValueError): 
                pluginId = None
        else:  
            pluginId = event.get('pluginId')

        with SessionLocal() as session:
            limit = get_limit_by_plugin_id(session, pluginId)
            if limit is not None:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'id': limit.id,
                        'pluginId': limit.pluginId,
                        'valueMax': limit.valueMax,
                        'valueMin': limit.valueMin
                    })
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'responseMessage': 'No limits found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'responseMessage': f'Error when retrieving from database: {str(e)}'})
        }
