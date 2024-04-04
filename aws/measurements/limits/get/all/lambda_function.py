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

def get_all_measurement_limits(session):
    measurements = session.query(MeasurementLimit).all()
    return measurements

def handler(event, context):
    try:
        with SessionLocal() as session:
            measurement_limits = get_all_measurement_limits(session)
            if len(measurement_limits) > 0:
                response = []
                for limit in measurement_limits:
                    response.append({
                        'id': limit.id,
                        'pluginId': limit.pluginId,
                        'valueMax': limit.valueMax,
                        'valueMin': limit.valueMin
                    })
                return {
                    'statusCode': 202,
                    'headers': headers,
                    'body': json.dumps({'limits': response})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'No limits found'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error when retrieving from database: {str(e)}'})
        }
