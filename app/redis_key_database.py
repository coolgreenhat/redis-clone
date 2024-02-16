import time 

class RedisKeyDatabase:
    
    def __init__(self):
        self.redis_keys = []

    def add_redis_key(self, redis_key):
        self.redis_keys.append(redis_key)

    def find_redis_key(self, search_key):
        for redis_key in self.redis_keys:
            if redis_key.key == search_key:
                if redis_key.expiry is None:
                    return redis_key 
                elif int(time.time()*1000) < redis_key.expiry:
                    return redis_key
                else:
                    self.redis_keys.remove(redis_key)
                    break
        return None

    def update_redis_key(self, update_key, update_value, update_expiry):
        for redis_key in self.redis_keys:
            if redis_key.key == update_key:
                if redis_key.expiry is None:
                    redis_key.value = update_value
                    redis_key.expiry = update_expiry
                    break
                elif int(time.time()*1000) > redis_key.expiry:
                    redis_key.value = update_value
                    redis_key.expiry = update_expiry
                    break
                else:
                    self.redis_keys.remove(redis_key)
                    break
    
    def len(self):
        return len(self.redis_keys)

    def get_all(self):
        return self.redis_keys
