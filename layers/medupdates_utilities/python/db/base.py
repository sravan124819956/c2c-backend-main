from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import psycopg2 
import boto3
import os
from .secret import get_secret

try:
    # db_host = os.environ.get('RDS_HOST')
    # db_port = os.environ.get('RDS_PORT')
    # db_name = os.environ.get('RDS_DBNAME')
    # db_username = os.environ.get('RDS_USER')
    # secret_name = os.environ.get('RDS_SECRET_NAME')

    db_host= "localhost"
    db_port="5433"
    db_name="postgres"
    db_username="postgres"
    db_password = "root"

    # db_password = get_secret(secret_name)

    uri=f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    print("URI: ", uri)

    local_engine=create_engine(uri,echo=True)

    _SessionFactory = sessionmaker(bind=local_engine)
except Exception as e:
    print(str(e))
    local_engine=None
    
@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}

def generate_session():
    if local_engine is not None:
        return _SessionFactory()

def terminate():
    if local_engine is not None:
        local_engine.dispose()
    else:
        print("No connection found")
