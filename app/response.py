import time
from app.redis_key import RedisKey
from app.redis_key_database import RedisKeyDatabase

redis_store = RedisKeyDatabase()

def redis_response(decoded_data_list):
    response = None
    num_args = 0
    len_arg = 0
    last_arg = None
    last_key = None
    current_redis_key = RedisKey(None, None, None)

    decoded_data_list = decoded_data_list[:-1]
    while len(decoded_data_list) > 0:
        arg_one = decoded_data_list.pop(0).lower()
        if arg_one.startswith("*"):
            num_args = int(arg_one.strip("*"))
        elif arg_one.startswith("$"):
            len_arg = int(arg_one.strip("$"))
        elif arg_one:
            if last_arg == "echo":
                response = arg_one
            elif last_arg == "set":
                # Create new RedisKey object & set key parameter
                # value & expiry will be None at this point
                if redis_store.len() > 0:
                    current_redis_key = redis_store.find_redis_key(last_key)
                current_redis_key.key = arg_one
                current_redis_key.value = None
                current_redis_key.expiry = None
                redis_store.add_redis_key(current_redis_key)
                last_key = arg_one
            elif last_key:
                # if last key is not None then find RedisKey Object from redis store & update the value. 
                redis_key = redis_store.find_redis_key(last_key)
                redis_store.update_redis_key(redis_key.key, arg_one, redis_key.expiry)
                last_key = None
            elif last_arg == "px":
                redis_store.update_redis_key(current_redis_key.key ,current_redis_key.value ,int(time.time()*1000) + int(arg_one))
                response = "OK"
            elif last_arg == "get":
                redis_key = redis_store.find_redis_key(arg_one)
                if redis_key:
                    response = redis_key.value
                else:
                    response = '$-1\r\n'
            num_args -= 1
            last_arg = arg_one
        if num_args == 0:
            if response is None:
                response = "OK"
            break
    

    return response
