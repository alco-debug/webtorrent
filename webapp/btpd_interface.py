import os
import json
from torrent_model import Torrent, TorrentStats
from btpd_cache import *


TORRENT_HOME = "/srv/torrent/torrent/"
FILES_HOME = "/srv/torrent/files/"

def size_from_string(raw_size:str) -> float:
	"""Returns size of torrent in KBytes, given from raw btcli output"""
	units = ["K", "M", "G", "T", "P", "Y"]
	power = units.index(raw_size[-1].upper()) # The power to use with 1024. It's the index of last letter in raw_size in units[]
	return float(raw_size[:-1]) * (1024 ** power)

def speed_from_string(raw_speed:str) -> float:
	"""Returns transfer speed in KBytes, given from raw btcli output"""
	return size_from_string(raw_speed[:-3])

def list_torrents() -> list:
	"""Gets nothing, returns list of current torrents in queue"""
	command = "btcli list"
	def _list_torrents(command) -> list:
		torrents = []
		raw_output_lines = os.popen(command).read().split("\n")[1:-1]
		for line in raw_output_lines:
			words = line.split()
			name = ""
			for word in words[:-5]:
				name += word + " "
			number = int(words[-5])
			status = words[-4]
			have = float(words[-3][:-1])
			size = size_from_string(words[-2])
			ratio = float(words[-1])
			torrent = Torrent(name=name,number=number,status=status,have=have,size=size,ratio=ratio)
			torrents.append(torrent)
		return torrents
	if is_response_cached(command):
		return get_cached_response(command)
	else:
		result = _list_torrents(command)
		cache_response(command, result)
		return result


def stat(torrent:Torrent) -> dict:
	"""Gets nothing, returns current torrent daemon stats"""
	torrent_number_str = ""
	if torrent.number >= 0:
		torrent_number_str = str(torrent.number)
	command = "btcli stat " + torrent_number_str
	def _stat(command):
		raw_output = os.popen(command).read()
		raw_lines = raw_output.split("\n")
		words = raw_lines[1].split()
		if words[0] == "-":
			return TorrentStats()
		have = float(words[0][:-1])
		download = size_from_string(words[1])
		downrate = speed_from_string(words[2])
		upload = size_from_string(words[3])
		uprate = speed_from_string(words[4])
		ratio = float(words[5])
		connections = int(words[6])
		available = float(words[7][:-1])
		trackers = int(words[8])
		return TorrentStats(have=have,download=download,downrate=downrate,upload=upload,uprate=uprate,ratio=ratio,connections=connections,available=available,trackers=trackers)
	if is_response_cached(command):
		return get_cached_response(command)
	else:
		result = _stat(command)
		cache_response(command, result)
		return result

def start(torrent_id:int) -> bool:
	exists = False
	for t in list_torrents():
		if t.number == torrent_id:
			exists = True
	if exists:
		os.popen("btcli start " + str(torrent_id))
	return exists

def start_all():
	os.popen("btcli start")



def stop(torrent_id:int) -> bool:
	exists = False
	for t in list_torrents():
		if t.number == torrent_id:
			exists = True
	if exists:
		os.popen("btcli stop " + str(torrent_id))
	return exists

def start_all():
	os.popen("btcli stop")



def delete(torrent_id:int) -> bool:
	exists = False
	for t in list_torrents():
		if t.number == torrent_id:
			exists = True
	if exists:
		os.popen("btcli del " + str(torrent_id))
	return exists

def create(name:str) -> bool:
	full_name = TORRENT_HOME + name + ".torrent"
	dir_name = FILES_HOME + name
	exists = os.path.exists(full_name)
	if exists:
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		os.popen("btcli add -n {0} -d {1} {2}".format(name, dir_name, full_name))
	return exists

def cache_update(cache_expiry):
	from time import sleep
	from threading import Thread
	time_limit = cache_expiry*0.99
	while True:
		thread_pool = []
		for torrent in list_torrents():
			thread_pool.append(Thread(target=stat,args=[torrent]))
		for thread in thread_pool:
			thread.start()
			sleep((time_limit*0.9)/len(thread_pool))
		sleep(time_limit*0.1)
