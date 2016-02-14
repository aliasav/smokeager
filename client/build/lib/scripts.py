#! /usr/bin/env python

import sys
import requests

class API:

	SERVER = {
		"s1": "http://locahost:8000/",
		"s2": "http://autobot/",
	}
	URLS = {
		"smoke1": "/increment_smoke/",
		"analytics": "/analytics/",
	}

	def __init__(self):
		pass

	def setup(self):
		print("Setting up smokeager")
		return

	def increment_smoke(self, inc):
		print("Incrementing smoke by: " + str(inc))
		return

	def status(self):
		print("Fetching smoke analytics")
		return

	def clean(self):
		print("Cleaning smokeager counts")	

	def display_manual(self):
		print("\n---------|| SMOKEAGER (v0.0.1) ||---------\n\n")
		print("Avaliable commands:\n\n")
		print("1. smokeager inc [n]: increment smoke by [n].\n")
		print("2. smokeager status: gives smoking analytics.\n")		
		print("3. smokeager man: Displays this manual.\n")
		print("4. smokeager setup: Setup account for smokeager. Only single account support available presently.\n")
		print("5. smokeager clean: destroys current account information.\n\n")

def main(args):
	args = map(lambda x: x.lower().rstrip().lstrip(), args)	
	api = API()

	if (len(args)==1):
		api.display_manual()

	elif (len(args)==3):
		if (args[1]=="inc"):
			try:
				inc = int(args[2])
			except:
				api.display_manual()
			else:
				api.increment_smoke(args[2])
		else:
			api.display_manual()
	
	elif (args[1]=="man"):
		api.display_manual()

	elif (args[1]=="status"):
		api.status()

	elif (args[1]=="setup"):
		api.setup()

	elif (args[1]=="clean"):
		api.clean()

	else:
		api.display_manual()

if __name__ == "__main__":
	print("__main__ in scripts")
	main(sys.argv)

