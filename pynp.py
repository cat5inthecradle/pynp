# pynp.py
# author: Darin Webb @Cat5InTheCradle

import requests

class NodePingInterface:

	def __init__(self, apitoken, update_accounts = False, update_checks = False):
		self.apitoken = apitoken

		# update_checks implies update_accounts for now
		if update_checks:
			self.update_all()
		elif update_accounts:
			self.update_accounts()

	def update_all(self):
		self.update_accounts()
		self.update_checks()

	# Accounts
	# -------------------------

	# Sets the parent_account property and populates subaccounts
	def update_accounts(self):
		self.parent_account = None

		accounts = self.get_accounts()
		subaccounts = {}
		for customerid in accounts:
			if 'parent' in accounts[customerid]:
				self.parent_account = NPAccount(self.get_account(customerid))
			else:
				subaccounts[customerid] = self.get_account(customerid)
		self.parent_account.set_subaccounts(subaccounts)

	def get_accounts(self):
		return self.api_accounts_get()

	def get_account(self, customerid):
		response = self.api_accounts_get({'customerid':customerid})
		return response

	def new_subaccount(self, name, contactname, email, timezone="-5", location="nam", emailme="no"):
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
		return response

	# Checks
	# --------------------------

	def update_checks(self):

		self.parent_account.set_checks(self.get_checks())

		for customer_id in self.parent_account.subaccounts:
			subaccount = self.parent_account.subaccounts[customer_id]
			subaccount.set_checks(self.get_checks(customer_id, True))

	# if no customerid given, returns parent account checks only.
	def get_checks(self, customerid = "", current = False):
		payload = {'current':current}
		if customerid != "":
			payload['customerid'] = customerid
		return self.api_checks_get(payload)

	def get_check(self, check_id, lastresult = False):
		customerid = check_id.split('-')[0]
		return self.api_checks_get({'customerid':customerid, 'id':check_id, 'lastresult':lastresult})

	def check_status(self, check_id):
		return self.get_check(check_id, True)['lastresult']['su']

	# API Requests
	# ---------------------------

	def api_accounts_get(self, payload = {}):
		payload['token'] =  self.apitoken
		return requests.get('https://api.nodeping.com/api/1/accounts', json=payload).json()

	def api_checks_get(self, payload = {}):
		payload['token'] = self.apitoken
		return requests.get('https://api.nodeping.com/api/1/checks', json=payload).json()

	def api_results_current_get(self, payload = {}):
		payload['token'] = self.apitoken
		return requests.get('https://api.nodeping.com/api/1/results/current', json=payload).json()

class NPObject(object):
	def __init__(self, details):
		self.details = details

	def get(self, key):
		try:
			return self.details(key)
		except E as N:
			return None

	def print_details(self):
		output = ""
		for key in sorted(details):
			output += key + ": " + details(key) + "\n"
		return output


class NPAccount(NPObject):

	def __init__(self, details):
		self.checks = {}
		self.subaccounts = {}
		super(NPAccount, self).__init__(details)

	# feed this npi.get_checks(self.details['_id'])
	def set_checks(self, checks):
		for check_id in checks:
			self.checks[check_id] = NPCheck(checks[check_id])


	def set_subaccounts(self, subaccounts):
		for customerid in subaccounts:
			self.subaccounts[customerid] = NPAccount(subaccounts[customerid])

	def pprint(self):
		return self.details['_id'] + ", " + self.details['customer_name']

class NPCheck(NPObject):

	def __init__(self, details):
		super(NPCheck, self).__init__(details)

	def pprint(self):
		return self.details['_id'] + ", " + self.details['label']
