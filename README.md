# WebTorrent
It is a simple tool, which provides a JSON API for managing [BTPD](https://github.com/btpd/btpd). Useful for those, who desire to have an own server for downloading some torrents.
Speed limits management is not implemented (maybe yet).
To deploy WebTorrent you need a web-server (I use apache2, you can choose any of your wish with WSGI support). sYSTEMD service comes along, but it's not too hard to write a service script for OpenRC and other init systems.
