import validators


def validate_event(events):

    try:
        if  (events['title']) and (events['description']) and (events['specialty_id']) and (events['featured_for_day']) and (events['featured_for_user']) and (events['ext_weblink']) and (events['ext_name']) and (events['ext_type']) and (events['ext_access']):
            
            # print("Accepted")

            if len(events['title']) > 160 :
                # print("title Accepted")
                return{
                    'statusCode': 429,
                    'message': 'Title word limit exceeded'
                }

            if len(events['description']) > 1000 :
                # print("description Accepted")
                return{
                   'statusCode': 429,
                   'message': 'Description word limit exceeded'
                }

            if not validators.url(events['ext_weblink']) :
            #     print("url Accepted")
            # else:
            #     print("not url")    
                return{
                   'statusCode': 1010,
                   'message': 'This is not a link.'
                }
        return True

    except KeyError as e:
        return{
            'statusCode': 400,
            'message': 'Not valid',
        }  

           
def validate_record(record):

    try:
        # print(record.title , record.description, record.specialty_id, record.featured_for_day, record.featured_for_user)
        if  (record.title) and (record.description) and (record.specialty_id) and ((record.featured_for_day != None) or (record.featured_for_user != None)) and (record.ext_weblink ) and (record.ext_name) and (record.ext_type) and (record.ext_access):
            
            # print("Accepted")

            if len(record.title) > 160 :
                # print("title Accepted")
                return{
                    'statusCode': 429,
                    'message': 'Title word limit exceeded'
                }

            if len(record.description) > 1000 :
                # print("description Accepted")
                return{
                   'statusCode': 429,
                   'message': 'Description word limit exceeded'
                }

            if not validators.url(record.ext_weblink) :
            #     print("url Accepted")
            # else:
            #     print("not url")    
                return{
                   'statusCode': 1010,
                   'message': 'This is not a link.'
                }
            return True        
        # else:
        #         print("not valid")        
        
    except KeyError as e:
        return{
            'statusCode': 400,
            'message': 'Not valid',
        }  

                      