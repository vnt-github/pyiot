"""redis store."""
import redis
import json
import os
from config import config

redis_config = config["redis"]

class _Redis(object):
	def __init__(self):
		# Note:  use remote
		self.host = redis_config["host"]
		self.port = redis_config["port"]
		self.db = redis_config["db"]
		self.threshold = redis_config["threshold"]
		self.prefix = redis_config["prefix"]
		self._factory = None
		self._redis = None
		self._rpid = None
		self._fpid = None

	@property
	def __redis__(self):
		# different process
		if self._rpid != os.getpid():

			self.__redis__ = redis.StrictRedis(self.host,self.port,self.db)

		# logic to check if connection is alive
		try:

			self._redis.get(None)  # getting None returns None or throws an exception

		except (redis.exceptions.RedisError):

			self.__redis__ = redis.StrictRedis(self.host,self.port,self.db)

		return self._redis

	@__redis__.setter
	def __redis__(self,value):

		self._rpid = os.getpid()

		self._redis = value

	def get(self,key):

		key = self.getKey(key)

		value = self.__redis__.get(key)

		if value:
			value = json.loads(value)
		else:
			value = {}

		return value

	# multi threaded
	def set(self,key,value):

		key = self.getKey(key)

		old_value = self.__redis__.get(key)

		if old_value:

			old_value = json.loads(old_value)

		else:

			old_value = {}

		old_value.update(value)

		new_value = json.dumps(old_value)

		self.__redis__.set(key,new_value)

	'''
		cutom pop function
	'''
	def c_pop(self, key):

		key = self.getKey(key)

		old_value = self.__redis__.get(key)

		if old_value:

			old_value = json.loads(old_value)

		else:

			old_value = {}

		new_value = '{}'

		self.__redis__.set(key, new_value)

		return old_value

	def expire(self, key, time=10):

		key = self.getKey(key)

		self.__redis__.expire(key, time)

	def rpush(self, key, value):

		key = self.getKey(key)

		value = json.dumps(value)

		reply = self.__redis__.rpush(key, value)

		return reply

	def lpush(self, key, value):

		key = self.getKey(key)

		value = json.dumps(value)

		reply = self.__redis__.lpush(key, value)

		return reply

	def lpop(self, key):

		key = self.getKey(key)

		value = self.__redis__.lpop(key)

		value = json.dumps(value)

		return value

	def blpop(self, key, timeout=1):

		key = self.getKey(key)

		value = self.__redis__.blpop(key, timeout=timeout)

		if value:

			value = json.dumps(value)

		return value

	def sadd(self, key, value):

		key = self.getKey(key)

		self.__redis__.sadd(key,value)

	def smembers(self, key):

		key = self.getKey(key)

		values = self.__redis__.smembers(key)

		values = json.dumps(values)

		return values

	def zadd(self, key, score, value):
		print('zadd', key, score, value)
		key = self.getKey(key)
		self.__redis__.zadd(key, score, value)

	def zrange(self, key, start, stop, withscores=True):
		print('zrange', key, start, stop)
		key = self.getKey(key)
		values = self.__redis__.zrange(key, start, stop, withscores)
		return values

	def zrangebyscore(self, key, start, stop, withscore=True):
		print('zrangebyscore', key, start, stop)
		key = self.getKey(key)
		value = self.__redis__.zrangebyscore(key, min=start, max=stop, withscores=withscore)
		return value

	def getKey(self, key):
		# print "Redis.getKey():",key
		return self.prefix + str(key)

	def getExecutionThreshold(self):

		return int(float(self.threshold))

Redis = _Redis()
