from datetime import datetime
import db
from datatypes.journal_access import JournalAccess
from datatypes.journal_type import JournalType


def lambda_handler(event,context) :
        session = db.generate_session()
        Journal = db.models.Journal
        
        try:
                records = session.query(Journal).filter(Journal.id == event['id'])
                for record in records:
                        record.specialty_id = event['specialty_id'] if event['specialty_id'] != "" else None

                        if event['title'] != "" : 
                                if len(event['title']) <= 160 :
                                        record.title = event['title']
                                else : 
                                        return{
                                        'statusCode': 429,
                                        'message': 'Title word limit exceeded'
                                        }      
                                        
                        if event['description'] != "" : 
                                if len(event['description']) <= 1000 :
                                        record.description = event['description'] 
                                else:
                                        return{
                                        'statusCode': 429,
                                        'message': 'Description word limit exceeded'
                                        }
                                        
                        if (event['ext_type'] if event['ext_type'] != "" else None) == JournalType.Paid.value:
                                record.ext_type = JournalType.Paid.value
                        elif (event['ext_type'] if event['ext_type'] != "" else None) == JournalType.Premium.value:
                                record.ext_type = JournalType.Premium.value 
                        
                        if (event['ext_access'] if event['ext_access'] != "" else None) == JournalAccess.Public.value:
                                record.ext_access = JournalAccess.Public.value
                        elif (event['ext_access'] if event['ext_access'] != "" else None) == JournalAccess.Private.value:
                                record.ext_access = JournalAccess.Private.value  

                        record.ext_weblink = event['ext_weblink'] if event['ext_weblink'] != "" else None
                        # if  validators.url(event['ext_weblink'] if 'ext_weblink' in event else None) :
                        #         record.ext_weblink = event['ext_weblink']
                        # else:           
                        #         return{
                        #         'statusCode': 1010,
                        #         'message': 'This is not a link.'
                        #         }
                        record.featured_for_day = event['featured_for_day'] 
                        record.featured_for_user = event['featured_for_user'] 
                        record.ext_name = event['ext_name'] if event['ext_name'] != ""  else None
                        print(event['scheduled_at'])
                        record.scheduled_at = event['scheduled_at'] if event['scheduled_at'] is not None else None
                        record.updated_at = datetime.now()
                        journal_id = str(record.id)

                session.commit() 
                session.close()
                db.terminate()
                return{
                        'journal_id': journal_id
                        }
        except KeyError as e:
                return{
                'statusCode': 400,
                'message': 'no data found' ,
                }