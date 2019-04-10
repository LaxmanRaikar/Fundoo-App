import redis


r = redis.StrictRedis(host='localhost', port=6379, db=0)


"""This class is used to set , get and delete data from Redis cache"""


class redis_methods:
    def set_token(self, key, value):
        r.set(key, value)       # adds the data to redis
        print('token set')

    def get_token(self, key):
        token = r.get(key)       # gets the data out of redis
        return token