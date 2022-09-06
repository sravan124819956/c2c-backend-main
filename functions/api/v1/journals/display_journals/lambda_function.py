import db
from datetime import timedelta
from sqlalchemy import desc, or_, and_
from datatypes.journal_access import JournalAccess
from datatypes.jounrnal_status import JournalStatus
from datatypes.journal_type import JournalType


def lambda_handler(event,context) :

    try:
        
        session = db.generate_session()
        Specialty = db.models.Specialty
        Journal = db.models.Journal
        if event['section'] == "active" :
            journal_status = [1,2]
            query= session.query(Journal, Specialty).join(Specialty, Journal.specialty_id == Specialty.id)
            
        if event['section'] == "draft" :
            journal_status = [0]
            query= session.query(Journal)
           
        if event['section'] == "archived" :
            journal_status = [3] 
            query= session.query(Journal)  
       
        query = query.filter(Journal.deleted_at.is_(None))

        if event['section'] == "active" :
            if (event['journal_access'] if 'journal_access' in event else False) :
                if event['journal_access'] == JournalAccess.Public.value:
                    query = query.filter(Journal.ext_access == JournalAccess.Public.value)
                elif event['journal_access'] == JournalAccess.Private.value : 
                    query = query.filter(Journal.ext_access == JournalAccess.Private.value) 
                elif event['journal_access'] == "All":
                    print("======>1")
                    query = query.filter(Journal.ext_access.in_([JournalAccess.Private.value,JournalAccess.Public.value]))  

            if (event['journal_status'] if 'journal_status' in event else False) : 
                if event['journal_status'] == "published":
                    query = query.filter(Journal._status.in_([JournalStatus.Published.value]))
                elif event['journal_status'] == "scheduled" : 
                    query = query.filter(Journal._status.in_([JournalStatus.Scheduled.value])) 
                elif event['journal_status'] == "All" :
                    print("======>2")
                    query = query.filter(Journal._status.in_(journal_status))
        
            if (event['start_date'] if 'start_date' in event else False) and (event['end_date'] if 'end_date' in event else False) :
                query = query.filter(and_(Journal.updated_at >= event['start_date'], Journal.updated_at <= event['end_date']))
                
        if event['section'] == "archived" :
            query = query.filter(Journal._status.in_(journal_status))
            if (event['journal_access'] if 'journal_access' in event else False)  :
                if event['journal_access'] == JournalAccess.Public.value:
                    query = query.filter(Journal.ext_access == JournalAccess.Public.value)
                elif event['journal_access'] == JournalAccess.Private.value : 
                    query = query.filter(Journal.ext_access == JournalAccess.Private.value) 
                elif event['journal_access'] == "All" :
                    print("======>3")
                    query = query.filter(or_((Journal.ext_access.in_([JournalAccess.Public.value, JournalAccess.Private.value])), (Journal.ext_access.is_(None))))
                     

            records = query.order_by(desc(Journal.updated_at)).limit(event['page_size'])\
                .offset((event['page_index']-1)*event['page_size'])
            print(records)    
            record = query.count() 
            print(record)  
            data = [r._asdict() for r in records]
            print("=======>data",data)
            
            b = list()
            c = ()
            Specialty = db.models.Specialty
            specialties_names=session.query(Specialty.id,Specialty.name)
            sp_data = [r._asdict() for r in specialties_names]
            for d in data:
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
                if d['specialty_id'] != "None" :
                    for sp in sp_data:
                        sp['id'] = str(sp['id'])  
                        if d['specialty_id'] == sp['id']:
                            c = {'Journal': d, 'Specialty': sp }
                            b.append(c) 
                else :
                    c = {'Journal': d, 'Specialty': None }
                    print("====>5",c)
                    b.append(c) 
                    print("======>6",b)            
                       
            print("======>7",b)            
            return{
                'data': b,
                'total_count': record
            }


        if event['section'] == "draft" : 
            query = query.filter(Journal._status.in_(journal_status))
            if (event['journal_access'] if 'journal_access' in event else False)  :
                if event['journal_access'] == JournalAccess.Public.value:
                    query = query.filter(Journal.ext_access == JournalAccess.Public.value)
                elif event['journal_access'] == JournalAccess.Private.value : 
                    query = query.filter(Journal.ext_access == JournalAccess.Private.value) 
                elif event['journal_access'] == "All" :
                    print("======>4")
                    query = query.filter(or_((Journal.ext_access.in_([JournalAccess.Public.value, JournalAccess.Private.value])), (Journal.ext_access.is_(None))))

            records = query.order_by(desc(Journal.updated_at)).limit(event['page_size'])\
                .offset((event['page_index']-1)*event['page_size'])
            print(records)    
            record = query.count() 
            print(record)  
            data = [r._asdict() for r in records]
            print("=======>data",data)
            
            b = list()
            c = ()
            Specialty = db.models.Specialty
            specialties_names=session.query(Specialty.id,Specialty.name)
            sp_data = [r._asdict() for r in specialties_names]
            for d in data:
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
                if d['specialty_id'] != "None" :
                    for sp in sp_data:
                        sp['id'] = str(sp['id'])  
                        if d['specialty_id'] == sp['id']:
                            c = {'Journal': d, 'Specialty': sp }
                            b.append(c) 
                else :
                    c = {'Journal': d, 'Specialty': None }
                    print("====>5",c)
                    b.append(c) 
                    print("======>6",b)            
                       
            print("======>7",b)            
            return{
                'data': b,
                'total_count': record
            }


        records = query.order_by(desc(Journal.updated_at)).limit(event['page_size'])\
                    .offset((event['page_index']-1)*event['page_size'])

        print(records)    

        record = query.count() 
        
        print(record)    

        data =[ [r._asdict() for r,a in records], [a._asdict() for r,a in records]  ]
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
                    c = {'Journal': data[i-1][j], 'Specialty': data[i][j]}
                    b.append(c)
                    
        print(b) 
        
        return{
            'data': b,
            'total_count': record
        }
    except KeyError as e:
            return{
            'statusCode': 400,
            'message': 'no data found',
            }  
    finally:
        session.close()
        db.terminate()            