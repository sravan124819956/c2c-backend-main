import db
from datetime import timedelta
from datatypes.journal_access import JournalAccess
from datatypes.journal_type import JournalType

def lambda_handler(event, context):
    try:
        
        session = db.generate_session()
        Specialty = db.models.Specialty
        Journal = db.models.Journal
        JournalDoc = db.models.JournalDocuments

        journal_doc_data = session.query(JournalDoc).filter(JournalDoc.journal_id == event['id']) 

        doc_data = [r._asdict() for r in journal_doc_data] 
        for d in doc_data:
            if d['journal_id'] != None:
                d['id'] = str(d['id'])
                d['journal_id'] = str(d['journal_id'])
                d['created_at'] = str(d['created_at']+timedelta(hours=5, minutes=30))
                d['updated_at'] = str(d['updated_at']+timedelta(hours=5, minutes=30))
            else:
                doc_data = None
                  

        journ = session.query(Journal).filter(Journal.id == event['id'])

        journ_data = [r._asdict() for r in journ]
        b = list()
        c = ()
        for d in journ_data: 
            if d['specialty_id'] != None:

                journal_data=session.query(Journal,Specialty).join(Specialty, Journal.specialty_id == Specialty.id)\
                            .filter(Journal.id == event['id'])
    
                data =[ [r._asdict() for r,a in journal_data], [a._asdict() for r,a in journal_data]]  
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
            else:
            
                d['id'] = str(d['id'])
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
                c = {'Journal': d, 'Specialty': None , 'Journal_Document': doc_data}
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