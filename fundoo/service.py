import redis


r = redis.StrictRedis(host='localhost', port=6379, db=0)

class redis_methods:

    def set_token(self,key,value):
        r.set(key,value)
        print('token set')

    def get_token(self,key):
        token=r.get(key)
        return  token