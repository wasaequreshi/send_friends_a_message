import requests
import json
import sys

# This class takes in the following params
# access_token - token from PushBullet API
# list_of_phone_numbers - comma separated
# message - a string text to send friends
# This only work for android
class send_friends_a_message():

	def __init__(self, access_token, list_of_phone_numbers, message):
		# Setting up access token for class 
		self.access_token = access_token
		# Setting up list of phone numbers array
		self.list_of_phone_numbers = []

		# Adding all phone numbers (comma separated)
		split_list_of_phone_numbers = list_of_phone_numbers.split(",")
		for number in split_list_of_phone_numbers:
			self.list_of_phone_numbers.append(number.strip())
		
		# Setting message to send to the number
		self.message = message

		# Setting up user and device id to use later for messaging
		self.set_user_iden()
		self.set_device_iden()

	def status_check(self, response):

		# Getting status code from response
		status_code = response.status_code

		if status_code != 200:
			print response
			sys.exit()

	def set_user_iden(self):
		# Getting User Identifier
		# Setting data up to send to api
		url = "https://api.pushbullet.com/v2/users/me"
		headers = {'Access-Token' : self.access_token}
		
		# Error checking for api call
		try:
			response = requests.get(url, headers=headers)
			user_data = response.json()
		except requests.exceptions.RequestException as e:  # This is the correct syntax
			print e
			sys.exit()

		# respond code checking
		self.status_check(response)
		
		self.source_user_iden = user_data['iden']

	def set_device_iden(self):
		# Getting Device Identifier
		# Setting data up to send to api
		url = "https://api.pushbullet.com/v2/devices"
		headers = {'Access-Token' : self.access_token}
		
		# Error checking for api call
		try:
			response = requests.get(url, headers=headers)
		except requests.exceptions.RequestException as e:  # This is the correct syntax
			print e
			sys.exit()

		# respond code checking
		self.status_check(response)

		device_data = response.json()
		devices = device_data['devices']

		# Looking for mobile device with sms
		for device in devices:
			if device['icon'] == "phone" and device['has_sms'] == True:
				self.target_device_iden = device['iden']

	def send_message(self):
		# Now sending the message
		url = "https://api.pushbullet.com/v2/ephemerals"
		package_name = "com.pushbullet.android"
		type_request = "messaging_extension_reply"

		# Sending to each phone number passed in
		for number in self.list_of_phone_numbers:
			# Setting data up to send to api
			data_binary = {"type" : "push", 
				"push" : {"conversation_iden" : number, 
					"message" : self.message, "package_name" : package_name, 
						"source_user_iden" : self.source_user_iden, "target_device_iden" : self.target_device_iden, 
							"type" : type_request}}
			headers = {'Content-Type' : 'application/json', 'Access-Token' : self.access_token}

			# Error checking for api call
			try:
				response = requests.post(url, data=json.dumps(data_binary), headers=headers)
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print e
				sys.exit()

			# response code checking
			self.status_check(response)

# Running the script
def main():

	# Getting params from command line
	access_token = sys.argv[1]
	list_of_phone_numbers = sys.argv[2]
	message = sys.argv[3]

	# Setting up class to send message to friends
	wumffp = send_friends_a_message(access_token, list_of_phone_numbers, message)
	wumffp.send_message()

if __name__ == '__main__':
	main()

