import json
import sys
sys.path.append("C:\\Users\Jufishan Boksha\Desktop\C2C\medupdates-backend")

from layers.medupdates_utilities.python.db.models.journals import Journals
from layers.medupdates_utilities.python.db.models.base import session 

def  lambda_handler():
    
    record = session.query(Journals).all()
    for r in record :
        print(r.title, r.status, r.created_at) 
        # print(sorted(r.created_at))
        
    print(record.sort())


# events={}

lambda_handler()