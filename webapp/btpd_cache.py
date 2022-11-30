from app_config import BTPD_CACHE_EXPIRY
from datetime import datetime, timedelta


cache_expiry_timedelta = timedelta(seconds=BTPD_CACHE_EXPIRY)
cache = {}

def is_cache_record_expired(cache_record):
	return datetime.now() - cache_record["timestamp"] > cache_expiry_timedelta

def get_cached_response(command):
	if is_response_cached(command):
		return cache[command]["response"]
	return {}

def cache_response(command, response):
	cache[command] = {"timestamp": datetime.now(), "response": response}

def is_response_cached(command):
	result = False
	cache_record = cache.get(command)
	if cache_record is not None:
		if not is_cache_record_expired(cache_record):
			result = True
	return result
