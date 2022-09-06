from datetime import datetime
import db 
from datatypes.jounrnal_status import JournalStatus
from datatypes.journal_type import JournalType
from datatypes.journal_access import JournalAccess


def lambda_handler(event,context) :
        try:        
                session = db.generate_session()
                Journal = db.models.Journal() 
                print("=======>1",event)
                if ((event['title']) and (event['description'])) :
                        if len(event['title']) <= 160 and len(event['description']) <= 1000 :
                                print("=======>2",event['title'])
                                Journal.title = event['title']
                                Journal.description = event['description']
                                print("=======>3",event['description'])
                                Journal.specialty_id = event['specialty_id'] if event['specialty_id'] != "" else None
                                print("=======>4",event['specialty_id'])
                                Journal.featured_for_day = event['featured_for_day'] 
                                print("=======>5",event['featured_for_day'])
                                Journal.featured_for_user = event['featured_for_user'] 
                                print("=======>6",event['featured_for_user'] )
                                Journal.ext_weblink = event['ext_weblink'] if event['ext_weblink'] != "" else None
                                print("=======>7",event['ext_weblink'])
                                Journal.ext_name = event['ext_name'] if event['ext_name'] != "" else None
                                print("=======>8",event['ext_name'])
                                if (event['ext_type'] if event['ext_type'] != "" else None) == JournalType.Paid.value:
                                        Journal.ext_type = JournalType.Paid.value
                                elif (event['ext_type'] if event['ext_type'] != "" else None) == JournalType.Premium.value:
                                        Journal.ext_type = JournalType.Premium.value 
                                print("=======>9",event['ext_type'])
                                if (event['ext_access'] if event['ext_access'] != "" else None) == JournalAccess.Public.value:
                                        Journal.ext_access = JournalAccess.Public.value
                                elif (event['ext_access'] if event['ext_access'] != "" else None) == JournalAccess.Private.value:
                                        Journal.ext_access = JournalAccess.Private.value  
                                print("=======>10",event['ext_access'])
                                Journal.status = JournalStatus.Draft  
                                Journal.created_at = datetime.now()
                                Journal.updated_at = datetime.now()
                                session.add(Journal)
                                session.flush() 
                                print("=======>11",Journal)
                                journal_id = str(Journal.id)
                        else:   
                                return{
                                        'statusCode': 429,
                                        'message': 'word limit exceeded'
                                } 
                session.commit() 
                session.close()
                db.terminate()
                print("=======>12")
                return{
                        'journal_id': journal_id
                }     
        except KeyError as e:
                return{
                'statusCode': 400,
                'message': 'no data found' ,
                }                