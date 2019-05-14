import time, hashlib
import uuid

def create_uid():
    return str(uuid.uuid1())

def create_id():
    m = hashlib.md5(str(time.clock()).encode('utf-8'))
    return m.hexdigest()


