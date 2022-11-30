from app_config import WEB_CACHE_EXPIRY
from datetime import datetime, timedelta


cache_expiry_timedelta = timedelta(seconds=WEB_CACHE_EXPIRY)
cache = {}

def is_cache_record_expired(cache_record):
	return datetime.now() - cache_record["timestamp"] > cache_expiry_timedelta

def get_cached_response(url):
	if is_response_cached(url):
		return cache[url]["response"]
	return "{}"

def cache_response(url, response):
	cache[url] = {"timestamp": datetime.now(), "response": response}

def is_response_cached(url):
	result = False
	cache_record = cache.get(url)
	if cache_record is not None:
		if not is_cache_record_expired(cache_record):
			result = True
	return result
