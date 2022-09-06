# import db
import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
from layers.medupdates_utilities.python.db.base import Base
from layers.medupdates_utilities.python.db.base import generate_session
from layers.medupdates_utilities.python.db.base import terminate
from layers.medupdates_utilities.python.db.base import local_engine
from layers.medupdates_utilities.python.db.models.specialties import Specialty




def lambda_handler():
    try:
        session = generate_session()
        # Specialty = Specialty
        specialties_names=session.query(Specialty.id, Specialty.name)
        data = [r._asdict() for r in specialties_names]
        for d in data:
            d['id'] = str(d['id'])
        session.close()
        terminate()
        print(data)
        return{
            'data': data 
        }
    except KeyError as e:
        return{
            'statusCode': 404,
            'message': 'Table not found',
        }
lambda_handler()