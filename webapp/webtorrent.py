import flask
from flask import request
import os
import json
from werkzeug.utils import secure_filename

from threading import Thread

import btpd_interface as btpd
from torrent_model import Torrent
from web_cache import *
from app_config import *


app=flask.Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

btpd_cache_update_thread = Thread(target=btpd.cache_update, args=[BTPD_CACHE_EXPIRY])
btpd_cache_update_thread.start()


@app.route("/")
def root():
	return list_torrents()

@app.route("/api/list")
def list_torrents():
	if is_response_cached(request.url):
		return get_cached_response(request.url)
	else:
		resp = json.dumps([t.to_dict() for t in btpd.list_torrents()])
		cache_response(request.url, resp)
		return resp

@app.route("/api/stat")
@app.route("/api/stat/<int:id>")
def stat(id=-1):
	def _stat(id=-1):
		result = {"status": -1}
		torrents_list = btpd.list_torrents()
		torrent = Torrent()
		for t in torrents_list:
			if t.number == id or id == -1:
				torrent = t
				result["status"] = 0
				torrent_stat = btpd.stat(torrent).to_dict()
				for prop in torrent_stat.keys():
					result[prop] = torrent_stat[prop]
		return json.dumps(result)
	
	if is_response_cached(request.url):
		return get_cached_response(request.url)
	else:
		resp = _stat(id)
		cache_response(request.url, resp)
		return resp


@app.route("/api/start")
@app.route("/api/start/<int:id>")
def start(id=-1):
	response_dict = {"status": -1}
	if id == -1:
		btpd.start_all()
		response_dict["status"] = 0
	else:
		if btpd.start(id):
			response_dict["status"] = 0
	return json.dumps(response_dict)


@app.route("/api/stop")
@app.route("/api/stop/<int:id>")
def stop(id=-1):
	response_dict = {"status": -1}
	if id == -1:
		btpd.stop_all()
		response_dict["status"] = 0
	else:
		if btpd.stop(id):
			response_dict["status"] = 0
	return json.dumps(response_dict)

@app.route("/api/create/<string:name>")
def create(name="/"):
	response_dict = {"status": -1}
	if name != "/":
		status_ok = btpd.create(name)
		if status_ok:
			response_dict["status"] = 0
	return json.dumps(response_dict)

@app.route("/api/delete/<int:id>")
def delete(id=-1):
	response_dict = {"status": -1}
	if id >= 0:
		status_ok = btpd.delete(id)
		if status_ok:
			response_dict["status"] = 0
	return json.dumps(response_dict)


@app.route("/api/upload", methods=["GET", "POST"])
def upload():
	if request.method == "POST":
		if "file" not in request.files:
			return json.dumps({"status": -1})
		file = request.files["file"]
		if file.filename == "":
			return json.dumps({"status": -1})
		if file and file.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
			filename = secure_filename(file.filename)
			filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(filename)
			if os.path.isfile(filename):
				return json.dumps({"status": 0})
			else:
				return json.dumps({"status": -1})
	else:
		return flask.render_template("upload_torrent.html", page_name="UPLOAD")



if __name__ == "__main__":
	app.run()
