import json
from uuid import UUID

class MyConverter:
    def default(o):
        if isinstance(o, UUID):
            return o.hex

def formatter(item):
    
    formatted_data=json.loads(item,cls=MyConverter)

    return formatted_data