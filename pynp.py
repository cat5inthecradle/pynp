# pynp.py
# author: Darin Webb @Cat5InTheCradle

import requests

class NodePingInterface:

	accounts = {}
	checks = {}

	def __init__(self, apitoken, update = False):
		self.apitoken = apitoken
		if update:
			update_all()

	def update_all(self):
		self.update_accounts()
		self.update_checks()

	# Accounts
	# -------------------------

	def update_accounts(self):
		response = self.get_accounts()
		for customerid in response:
			self.accounts[customerid] = NPAccount(self.get_account(customerid))

	def get_accounts(self):
		return self.api_accounts_get()

	def get_account(self, customerid):
		response = self.api_accounts_get({'customerid':customerid})
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

	# Checks
	# --------------------------

	def update_checks(self):
		parent_checks = self.get_checks()
		for check_id in parent_checks:
			self.checks[check_id] = NPCheck(parent_checks[check_id])
		for account in self.accounts:
			account_checks = self.get_checks(self.accounts[account].details['_id'])
			for check_id in account_checks:
				self.checks[check_id] = NPCheck(account_checks[check_id])

	def get_checks(self, customerid = "", lastresult = False):
		payload = {'lastresult':False}
		if subaccount != "":
			payload['customerid'] = customerid
		return self.api_checks_get(payload)

	def get_check(self, check_id, current = False):
		customerid = check_id.split('-')[0]
		return self.api_checks_get({'customerid':customerid, 'id':check_id, 'current':False})

	# API Requests
	# ---------------------------

	def api_accounts_get(self, payload = {}):
		payload['token'] =  self.apitoken
		return requests.get('https://api.nodeping.com/api/1/accounts', json=payload).json()

	def api_checks_get(self, payload = {}):
		payload['token'] = self.apitoken
		return requests.get('https://api.nodeping.com/api/1/checks', json=payload).json()

class NPObject(object):
	details = {}
	def __init__(self, details):
		self.details = details

class NPAccount(NPObject):
	checks = {}
	children = {}

	# feed this npi.get_checks(self.details['_id'])
	def load_checks(self, checks):
		for check_id in checks:
			self.checks[check_id] = NPCheck(checks[check_id])

	def load_children(self, subaccounts):
		for customerid in subaccounts:
			self.children[subaccount] = NPAccount(subaccounts[customerid])

	def pprint(self):
		return "Account ID: " + self.details['_id'] + ", " + self.details['customer_name']

class NPCheck(NPObject):
	def pprint(self):
		return "Check ID: " + self.details['_id'] + ", " + self.details['label']