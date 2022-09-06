import db
from datetime import datetime,date
from sqlalchemy import and_
from datatypes.jounrnal_status import JournalStatus

def lambda_handler(event,context) :

    today = date.today() 
    session = db.generate_session()
    Journal = db.models.Journal
    schedule_date = session.query(Journal).filter(and_(Journal._status == JournalStatus.Scheduled.value, Journal.scheduled_at == today))
    
    for d in schedule_date:
        d.publish() 
        d.updated_at = datetime.now()

    session.commit() 
    session.close()
    db.terminate()