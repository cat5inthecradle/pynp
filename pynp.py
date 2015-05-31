## pynp.py

# http://docs.python-requests.org/en/latest/
import requests

class NodePingInterface:

	accounts = {}

	def __init__(self, apitoken):
		self.apitoken = apitoken
		self.update_accounts()

	def update_accounts(self):
		payload = {'token':self.apitoken}
		response = requests.get('https://api.nodeping.com/api/1/accounts', json=payload).json()
		for customerid in response:
			self.accounts[customerid] = NPAccount(self.get_account(customerid))

	def get_account(self, customerid):
		payload = {
			'token':self.apitoken,
			'customerid':customerid
		}
		response = requests.get('https://api.nodeping.com/api/1/accounts', json=payload).json()
		return response

	def new_account(self, name, contactname, email, timezone="-5", location="nam", emailme="no"):
		payload = {
			'token':self.apitoken,
			'name':name,
			'contactname':contactname,
			'email':email,
			'timezone':timezone,
			'location':location,
			'emailme':emailme
		}
		response = requests.post('https://api.nodeping.com/api/1/accounts', json=payload).json()
		self.accounts[response['_id']] = NPAccount(self.get_account(response['_id']))
		return response


class NPAccount(object):

	details = {}
	
	def __init__(self, details):
		self.details = details

	def get_details(self):
		return {'name':self.details['customer_name'], '_id':self.details['_id']}