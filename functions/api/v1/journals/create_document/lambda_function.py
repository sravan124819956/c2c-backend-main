from datetime import datetime
import db 


def lambda_handler(event,context):
    try:
        
        session = db.generate_session()
        JournalDoc = db.models.JournalDocuments
        records = session.query(JournalDoc).filter(JournalDoc.journal_id == event['journal_id']).count()
        if records > 0 :
            return {
                'statusCode': 400,
                'message': 'invalid' ,
            }
        else:    
            s3_document= db.models.JournalDocuments()
            s3_document.journal_id = event['journal_id']
            s3_document.title = event['title']
            s3_document.path= event['path']
            s3_document.created_at = datetime.now()
            s3_document.updated_at = datetime.now()
            session.add(s3_document)
            session.flush() 
            s3_document_id = str(s3_document.id)
            session.commit()
            db.terminate()
            return{
                's3_document_id': s3_document_id 
            } 
    except KeyError as e:
                return{
                'statusCode': 404,
                'message': 'no data available',
                }                