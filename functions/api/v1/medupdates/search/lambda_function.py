# import db
import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
from layers.medupdates_utilities.python.db.base import Base
from layers.medupdates_utilities.python.db.base import generate_session
from layers.medupdates_utilities.python.db.base import terminate
from layers.medupdates_utilities.python.db.base import local_engine
from layers.medupdates_utilities.python.db.models.journal import Journal
from sqlalchemy import desc, or_, and_


def lambda_handler(event):
    try:
        session = generate_session()
        e = event['search']
        search = "%{}%".format(e)
        record = session.query(Journal.id,Journal.title,).filter(or_(Journal.title.like(search),Journal.description.like(search))).limit(10)
        data = [r._asdict() for r in record]
        for d in data:
            d['id'] = str(d['id'])
        c = ()
        b = list()
        for i in data:
            c = {'Journal': i}
            b.append(c)
        print(b)
        return{
            'data': b 
        }
    except KeyError as e:
        return{
            'statusCode': 404,
            'message': 'Table not found',
        }
event = {}
event['search'] = "I am a boy."
       
lambda_handler(event)