from s3_services.s3_services import create_presigned_post
import os
import math
import time as tm

def lambda_handler(event,context) :
    try:
        bucket =  os.environ.get('DOCUMENTS_BUCKET')
        doc_title = event['doc_title']
        doc_title = doc_title.strip(' ')
        doc_title = doc_title.replace(' ','_')
        s3_file_key = 'journals/covers/'+ str(math.floor(tm.time())) + '-' + doc_title
        resp =  create_presigned_post(bucket,s3_file_key) 
        return {
            'data': resp
        }
    except KeyError as e:
                return{
                'statusCode': 400,
                'message': 'no data found' ,
                }                    
