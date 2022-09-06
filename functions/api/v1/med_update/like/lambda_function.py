import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
from layers.medupdates_utilities.python.db.base import Base
from layers.medupdates_utilities.python.db.base import generate_session
from layers.medupdates_utilities.python.db.base import terminate
from layers.medupdates_utilities.python.db.base import local_engine
from layers.medupdates_utilities.python.db.models.journal import Journal
from layers.medupdates_utilities.python.db.models.journal_reactions import JournalReactions
from layers.medupdates_utilities.python.db.models.journal_documents import JournalDocuments
from sqlalchemy import desc, or_, and_
from datetime import datetime
from layers.medupdates_utilities.python.datatypes.journal_reaction import JournalReaction 


def lambda_handler(event):
    try:
        session = generate_session()
        re = JournalReactions()
        if event['reaction'] == JournalReaction.Like.value:
            re.journal_id = event['id']
            re.user_id = event['user_id']
            re.reaction = JournalReaction.Like.value
            re.created_at = datetime.now()
            session.add(re)
    
        if event['reaction'] == JournalReaction.Undecided.value:
            res = JournalReactions
            un = session.query(res).filter(and_(res.journal_id == event['id'],res.user_id == event['user_id']))
            print(un)
            print("un")
            res.journal_id = event['id']
            res.user_id = event['user_id']
            res.reaction = JournalReaction.Undecided.value
            res.created_at = datetime.now()
            print("updated")
        session.commit() 
        session.close()
        terminate()

# ------------------------------------------------ Journal table ---------------------------------------------------
        records = session.query(Journal).filter(Journal.id == event['id'])
        data = [r._asdict() for r in records]
        for d in data:
            d['id'] = str(d['id'])
# -------------------------------------------------- Journal document table ---------------------------------------
        j_record = session.query(JournalDocuments).filter(JournalDocuments.journal_id == event['id'])
        data1 = [r._asdict() for r in j_record]
        c = ()
        b = list()
        for jj in data1:
            c = {'journal': d,'journal_document': jj}
            b.append(c)
        print(b)

        return{
            'data': b 
        }
        
    except KeyError as e:
        return{
            'statusCode': 404,
            'message': 'no data found',
        }
    


event = {}
event['id'] = "94cfe834-8f3f-430c-b448-8ff08c186f5d"
event['reaction'] = "Undecided"
event['user_id'] = "94cfe834-8f3f-430c-b448-8ff08c186f12"
lambda_handler(event)        