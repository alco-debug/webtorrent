import json
from enum import Enum

class Torrent:
	"""
Describes a torrent

name: the name (alias) given to this torrent
number: the sequentional number of torrent in list
status: current status of torrent
have: currently available size of original data in percent
size: full size of original data in KBytes
ratio: WHAT IS THAT? DON'T KNOW ACTUALLY
	"""
	props_list = ("name", "number", "status", "have", "size", "ratio")

	def __init__(self,name="",number=-1,status="",have=0.0,size=0.0,ratio=0.0):
		self.name = name
		self.number = number
		self.status = status
		self.have = have
		self.size = size
		self.ratio = ratio

	def from_json(self,json_string:str):
		ok = False
		# Is correct JSON?
		try:
			props = json.loads(json_string)
		except JSONDecodeError:
			pass

		# If it is, does it contain all necessary properties to build a class?
		necessary_set = set(props_list);
		current_set = set(props.keys());
		if current_set.issuperset(necessary_set):
			ok = True
		# If all OK, use regular constructor with info we parsed
		if ok:
			self = Torrent(name=props["name"],number=props["number"],status=props["status"],have=props["have"],size=props["size"],ratio=props["ratio"])
			return self
		else:
			self = Torrent()
			return self

	def to_dict(self) -> dict:
		return {"name": self.name, "number": self.number, "status": self.status, "have": self.have, "size": self.size, "ratio": self.ratio}

	def to_json(self) -> str:
		return json.dumps(self.to_dict())


class TorrentStats:
	"""
Describes the torrent daemon statistics output

have: currently available size of original data in percent
download: amount of data, downloaded during current session, KBytes
downrate: download speed, KByte/sec
upload: amount of data, shared during current session, KBytes
uprate: sharing speed , KByte/sec
ratio: download/sharing ratio
connections: the number of currently established active connections
available: amount of downloaded data, available currently 
trackers: the number of trackers, we connected currently
	"""

	props_list = ("have", "download", "downrate", "upload", "uprate", "ratio", "connections", "available", "trackers")

	def __init__(self,have=0.0,download=0.0,downrate=0.0,upload=0.0,uprate=0.0,ratio=0.0, connections=0, available=0.0, trackers=0):
		self.have = have
		self.download = download
		self.downrate = downrate
		self.upload = upload
		self.uprate = uprate
		self.ratio = ratio
		self.connections = connections
		self.available = available
		self.trackers = trackers

	def from_json(self,json_string:str):
		ok = False
		# Is correct JSON?
		try:
			props = json.loads(json_string)
		except JSONDecodeError:
			pass

		# If it is, does it contain all necessary properties to build a class?
		necessary_set = set(props_list);
		current_set = set(props.keys());
		if current_set.issuperset(necessary_set):
			ok = True
		# If all OK, use regular constructor with info we parsed
		if ok:
			self = TorrentStats(have=props["have"],download=props["download"],downrate=props["downrate"],upload=props["upload"],uprate=props["uprate"],ratio=props["ratio"], connections=props["connections"], available=props["available"], trackers=props["trackers"])
			return self
		else:
			self = TorrentStats()
			return self

	def to_dict(self) -> dict:
		return {"have": self.have, "download": self.download, "downrate": self.downrate, "upload": self.upload, "uprate": self.uprate, "ratio": self.ratio, "connections": self.connections, "available": self.available, "trackers": self.trackers}

	def to_json(self) -> str:
		return json.dumps(self.to_dict())

class TorrentState(Enum):
	"""
Describes the state of a torrent
	"""
	INACTIVE = 1
	LAUNCHED = 2

