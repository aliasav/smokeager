#! /usr/bin/env python

import sys
import os
import requests
import json
import ConfigParser
import ast

class SmokeagerCLI:

	def __init__(self):
		# server domain
		self.SERVER = {
			"s2": "http://localhost:8000/api", # for testing
			"s1": "http://autobot/api",
		}
		# all api urls
		self.APIS = {
			"increment": "/increment_smoke",
			"status": "/get_stats",
			"signup": "/signup",
		}
		self.SETTINGS = {
			"sections": [{
				"account": ["name", "email", "token"],
			}],
			"file_name": "settings.ini",
		}		

	# sets up smokeager cli for user
	# stores account information in ~/.smkoeager-cli/account.txt
	# stores api key, username, email-id
	def setup(self):	

		# creates ~/.smokeager-cli
		def create_smokeager_dir():
			home_dir=""
			try:
				from os.path import expanduser
				home_dir = expanduser("~")
			except:
				home_dir = str(raw_input("Couldn't fetch home directory! Please enter absolute home directory path: "))
			
			smokeager_cli_path = home_dir+"/.smokeager-cli"
			if not os.path.exists(smokeager_cli_path):
				os.makedirs(smokeager_cli_path)

			if (os.path.exists(home_dir+"/.smokeager-cli")):
				print(".smokeager-cli folder created successfully!")
			else:
				print("Error in creating .smokeager-cli folder, please contact maintainers of project or raise a github issue!")
				sys.exit()

			return home_dir
		
		# takes input: name, email-id, password
		def get_user_info():		
			import getpass	
			name = str(raw_input("Please enter your name: "))
			email = str(raw_input("Please enter your email-id: "))
			while True:
				p1 = getpass.getpass("Enter password (input will be hidden): ")
				p2 = getpass.getpass("Confirm password: ")
				if(p1==p2 and (len(p1)>5)):
					break
			data = {
				"name": name,
				"email": email,
				"password": p1,
				}
			return data
		
		# makes api call to server
		# if successful, returns token key for user
		def signup(data):
			signup_api = self.SERVER["s1"] + self.APIS["signup"]
			try:
				print("Contacting server ...")
				r = requests.post(signup_api, data=json.dumps(data), timeout=5)
			except:
				print("Please check your connection!")
				sys.exit()
			else:
				if (r.status_code==200):
					print("Account created successfully!")
					token = r.text
					return token
				else:
					print("Server returned: " + str(r.status_code))
					sys.exit()

		# creates settings file
		def create_settings(data):			
			file_path = data["home_dir"] + "/.smokeager-cli/settings.ini"			
			settings_file = open(file_path, "w")
			config = ConfigParser.ConfigParser()
			config.add_section("account")
			config.set("account", "name", data["name"])
			config.set("account", "email", data["email"])
			config.set("account", "token", data["token"])
			config.write(settings_file)
			settings_file.close()


		home_dir = create_smokeager_dir()
		data = get_user_info()
		token = signup(data)
		data["token"] = token
		data["home_dir"] = home_dir
		if (token):
			create_settings(data)
			print("Settings file created successfully!")
			return
		else:
			print("Error in creating settings file, please contact maintainers of project or raise a Github issue!")
			sys.exit()


	# get settings file information
	def get_settings(self):
		#check for settings file	
		smokeager_cli_settings_file = self.get_smokeager_dir() + "/" + self.SETTINGS["file_name"]
		if os.path.isfile(smokeager_cli_settings_file):
			config = ConfigParser.ConfigParser()
			try:
				config.read(smokeager_cli_settings_file)
			except:
				print("Error in fetching settings file!")
				sys.exit()
			settings_data = {}
			# get data
			for section in self.SETTINGS["sections"]:
				for option in section[section.keys()[0]]:
					settings_data[option] = config.get(section.keys()[0], option)
			#print(settings_data)
			return settings_data



	def get_smokeager_dir(self):
		#check for settings file	
		home_dir=""
		try:
			from os.path import expanduser
			home_dir = expanduser("~")
		except:
			print("Unable to fetch home dir, please contact maintainers of project!")
			sys.exit()
		
		smokeager_cli_path = home_dir+"/.smokeager-cli"
		if not os.path.exists(smokeager_cli_path):
			print("smokeager-cli files do not exits! Please run smokeager setup!")
			sys.exit()
		else:		
			return smokeager_cli_path


	# makes api call to increment smoke count
	def increment_smoke(self, inc):
		settings_data = self.get_settings()
		if settings_data["token"]:
			token = ast.literal_eval((settings_data["token"]))
			token = token["key"]
		else:
			print("Token missing in settings file!")
			sys.exit()

		increment_api = self.SERVER["s1"] + self.APIS["increment"]
		data  = {
			"token_list": [token,],
			"count": inc,
		}
		try:
			print("Contacting server ...")
			r = requests.post(increment_api, data=json.dumps(data), timeout=5)
		except:
			print("Please check your connection!")
			sys.exit()
		else:
			if (r.status_code==200):
				print("Count incremented successfully!")
				response = r.text
				return response
			else:
				print("Server returned: " + str(r.status_code))
				sys.exit()


	# displays smoke analytics information
	def status(self):
		settings_data = self.get_settings()
		if settings_data["token"]:
			token = ast.literal_eval(settings_data["token"])
			token = token["key"]
		else:
			print("Token missing in settings file!")
			sys.exit()		
		status_api = self.SERVER["s1"] + self.APIS["status"]
		data = {
			"token": token,
		}

		try:
			#print("Contacting server ...")
			r = requests.post(status_api, data=json.dumps(data), timeout=5)
		except:
			print("Please check your connection!")
			sys.exit()
		else:
			if (r.status_code==200):
				response = json.loads(r.text)
				print("Smoking stats for " + str(settings_data["name"]) + ":\n")
				self.print_dict(response)
				return
			else:
				print("Error in fetching status!")
				sys.exit()

	# prints a dict object
	def print_dict(self, d):
		for key, value in d.iteritems():
			print(str(key) + ":\t" + str(value))
		print ""
	# cleans ~/.smokeager-cli/
	def clean(self):
		print("Cleaning smokeager counts")	

	# displays cli command manual
	def display_manual(self):
		print("\n---------|| SMOKEAGER (v0.0.1) ||---------\n\n")
		print("Avaliable commands:\n\n")
		print("1. smokeager inc [n]: increment smoke by [n].\n")
		print("2. smokeager status: gives smoking analytics.\n")		
		print("3. smokeager man: Displays this manual.\n")
		print("4. smokeager setup: Setup account for smokeager. Only single account support available presently.\n")
		print("5. smokeager clean: destroys current account information.\n\n")

# main entry for cli
def main(args):
	args = map(lambda x: x.lower().rstrip().lstrip(), args)	
	scli = SmokeagerCLI()

	if (len(args)==1):
		scli.display_manual()

	elif (len(args)==3):
		if (args[1]=="inc"):
			try:
				inc = int(args[2])
			except:
				scli.display_manual()
			else:
				scli.increment_smoke(args[2])
		else:
			scli.display_manual()
	
	elif (args[1]=="man"):
		scli.display_manual()

	elif (args[1]=="status"):
		scli.status()

	elif (args[1]=="setup"):
		scli.setup()

	elif (args[1]=="clean"):
		scli.clean()

	else:
		scli.display_manual()


if __name__ == "__main__":
	print("__main__ in scripts")
	main(sys.argv)

