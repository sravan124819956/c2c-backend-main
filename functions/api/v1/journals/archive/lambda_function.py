from datetime import datetime
import db

def lambda_handler(event,context) :
        session = db.generate_session()
        Journal = db.models.Journal
        
        try:
            
            records = session.query(Journal).filter(Journal.id == event['id'])
            for record in records:
                record.archive()
                record.updated_at = datetime.now()
            session.commit() 
            session.close()
            db.terminate()
            return{
                'statusCode': 200,
                'message': 'Successful',
                }
        except KeyError as e:
                return{
                'statusCode': 400,
                'message': 'no data found' ,
                }                