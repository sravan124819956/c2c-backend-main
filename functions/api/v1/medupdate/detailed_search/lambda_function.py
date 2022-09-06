# import db
import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
from layers.medupdates_utilities.python.db.base import Base
from layers.medupdates_utilities.python.db.base import generate_session
from layers.medupdates_utilities.python.db.base import terminate
from layers.medupdates_utilities.python.db.base import local_engine
from layers.medupdates_utilities.python.db.models.journal import Journal
from layers.medupdates_utilities.python.db.models.specialties import Specialty
from layers.medupdates_utilities.python.db.models.journal_documents import JournalDocuments
from sqlalchemy import desc, or_, and_


# def lambda_handler(event):
#     try:
#         session = generate_session()
# # ------------------------------------------ Journal table search ---------------------------------------------
#         e = event['search']
#         search = "%{}%".format(e)
#         # journal_record = session.query(Journal._status,Journal.id,Journal.specialty_id,Journal.title,
#         #                         Journal.description,Journal.featured_for_day,Journal.title,
#         #                        Journal.featured_for_user,Journal.ext_weblink,Journal.ext_name,
#         #                        Journal.ext_type,Journal.ext_access,Journal.scheduled_at,Journal.created_at,
#         #                        Journal.updated_at,Journal.deleted_at).filter(or_(Journal.title.like(search),Journal.description.like(search)))
#         #                        .limit(10)
#         query = session.query(Journal._status,Journal.id,Journal.specialty_id,Journal.title,
#                                 Journal.description,Journal.featured_for_day,
#                                Journal.featured_for_user,Journal.ext_weblink,Journal.ext_name,
#                                Journal.ext_type,Journal.ext_access,Journal.scheduled_at,Journal.created_at,
#                                Journal.updated_at,Journal.deleted_at, JournalDocuments.id.label('document_id'), JournalDocuments.path,
#                                 JournalDocuments.title.label('doc_title'), JournalDocuments.created_at.label('doc_created'),
#                                 JournalDocuments.updated_at.label('doc_updated'), Specialty.id.label('special_id'),
#                                 Specialty.name, Specialty.created_at.label('special_created'),
#                                 Specialty.updated_at.label('special_updated')).join(Specialty,Specialty.id == Journal.specialty_id).join(JournalDocuments, Journal.id ==
#                                 JournalDocuments.journal_id, isouter=True).filter(or_(Journal.title.like(search),Journal.description.like(search)))
#                             # .limit(10)
#         journl_data = [r._asdict() for r in query]
#         for i in journl_data:
#             c = {'_status':str(i['_status']),'id':str(i['id']),'specialty_id':str(i['specialty_id']),'title':str(i['title']),
#                             'description':str(i['description']),'featured_for_day':str(i['featured_for_day']),
#                             'featured_for_user':str(i['featured_for_user']),'ext_weblink':str(i['ext_weblink'])},
#             cc = {'id':str(i['id']),'name':i['name'],'created_at': i['created_at'],'updated_at': i['updated_at']}
#             ccc = {'journal_document':str(i['special_id'])},{'journal_reaction':str(i['special_id'])}
#             b = list()
#             j_data = ()
#             s_data = ()
#             jdoc_data = ()
#             b.append(c)
#         print(b)

        
#     except KeyError as e:
#         return{
#             'statusCode': 404,
#             'message': 'Table not found',
#         }

# event = {}
# event['search'] = "I am a boy."
       
# lambda_handler(event)



def lambda_handler(event):
    try:
        
        session = generate_session()
#--------------------------------------- It will search in journal table with input param --------------------------------
        e = event['search']
        search = "%{}%".format(e)
        journal_record = session.query(Journal._status,Journal.id,Journal.specialty_id,Journal.title,
                                Journal.description,Journal.featured_for_day,Journal.title,
                               Journal.featured_for_user,Journal.ext_weblink,Journal.ext_name,
                               Journal.ext_type,Journal.ext_access,Journal.scheduled_at,Journal.created_at,
                               Journal.updated_at,Journal.deleted_at).filter(or_(Journal.title.like(search),Journal.description.like(search))).limit(10) 

        doc_data = [r._asdict() for r in journal_record] 
        print(doc_data)
        for d in doc_data:
            if d['journal_id'] != None:
                d['id'] = str(d['id'])
                d['journal_id'] = str(d['journal_id'])
                d['created_at'] = str(d['created_at']+timedelta(hours=5, minutes=30))
                d['updated_at'] = str(d['updated_at']+timedelta(hours=5, minutes=30))
            else:
                doc_data = None
#--------------------------------------- It will search in specility table with journal sepID -------------------------
        journal_data=session.query(Journal,Specialty).join(Specialty, Journal.specialty_id == Specialty.id)
        data =[ [r._asdict() for r,a in journal_data], [a._asdict() for r,a in journal_data]]  
        print(data)
        print("data")
        b = list()
        c = ()
        for i in range(len(data)):
            if i == 1:
                for j in range(len(data[i])):
                    d =  data[i-1][j]
                    d['id'] = str(d['id'])
                    d['specialty_id'] = str(d['specialty_id'])
                    d['created_at'] = str(d['created_at']+timedelta(hours=5, minutes=30))
                    d['updated_at'] = str(d['updated_at']+timedelta(hours=5, minutes=30))
                    d['scheduled_at'] = str(d['scheduled_at']+timedelta(hours=5, minutes=30)) if d['scheduled_at'] is not None else None
                    if (d['ext_access'] if d['ext_access'] != "" else None) == JournalAccess.Public:
                        d['ext_access'] = JournalAccess.Public.value
                    elif (d['ext_access'] if d['ext_access'] != "" else None) == JournalAccess.Private:
                        d['ext_access'] = JournalAccess.Private.value 
                    if (d['ext_type'] if d['ext_type'] != "" else None) == JournalType.Paid:
                        d['ext_type'] = JournalType.Paid.value
                    elif (d['ext_type'] if d['ext_type'] != "" else None) == JournalType.Premium:
                        d['ext_type'] = JournalType.Premium.value     
                    e = data[i][j]
                    e['id'] = str(e['id'])
                    e['created_at'] = str(e['created_at']+timedelta(hours=5, minutes=30))
                    e['updated_at'] = str(e['updated_at']+timedelta(hours=5, minutes=30))
                    c = {'Journal': data[i-1][j], 'Specialty': data[i][j], 'Journal_Document': doc_data }
                    b.append(c)

        print(b)    
        session.close()
        db.terminate()
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