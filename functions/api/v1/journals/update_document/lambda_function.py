import db
from datetime import datetime


def lambda_handler(event,context) :
    session = db.generate_session()
    JournalDoc = db.models.JournalDocuments
    try:
            
        records = session.query(JournalDoc).filter(JournalDoc.journal_id == event['journal_id'])
        for record in records:
            
            record.title = event['title'] if 'title' in event else None
            record.path = event['path'] if 'path' in event else None      
            record.updated_at = datetime.now()
            s3_document_id = str(record.id)
            
        session.commit() 
        session.close()
        db.terminate()
        return{
            's3_document_id': s3_document_id
                }
    except KeyError as e:
            return{
            'statusCode': 400,
            'message': 'no data found' ,
            }