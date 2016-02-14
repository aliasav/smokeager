#! /usr/bin/env python

import sys
import os
import requests
import json
import ConfigParser

class SmokeagerCLI:

	# server domain
	SERVER = {
		"s1": "http://locahost:8000/api", # for testing
		"s2": "http://autobot/api",
	}
	# all api urls
	APIS = {
		"smoke1": "/increment_smoke",
		"analytics": "/analytics",
		"signup": "/signup",
	}

	def __init__(self):
		# server domain
		self.SERVER = {
			"s1": "http://localhost:8000/api", # for testing
			"s2": "http://autobot/api",
		}
		# all api urls
		self.APIS = {
			"smoke1": "/increment_smoke",
			"analytics": "/analytics",
			"signup": "/signup",
		}
		pass

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



	# makes api call to increment smoke count
	def increment_smoke(self, inc):
		print("Incrementing smoke by: " + str(inc))
		return

	# displays smoke analytics information
	def status(self):
		print("Fetching smoke analytics")
		return

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

