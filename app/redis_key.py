import time 

class RedisKey:

    def __init__(self, key, value, expiry):
        self.key = key 
        self.value = value
        if expiry:
            self.expiry = int(time.time()*1000) + expiry
        else: 
            self.expiry = expiry

