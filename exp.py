import redis
redis_client = redis.Redis(host='204.48.30.159', port=6379, db=0,password = 'hB9i2REJQsuf+3uJfPMmdjQeU8tGdkMJUM4riZNRy+pGVwJ372DKIAsS9MRdAb5aoshL0EqJp1TQ621')

cache_value = redis_client.hgetall('d9a78230-a3f9-11eb-9b12-71d13f12ff90')
print(cache_value)
