## pynp.py

# http://docs.python-requests.org/en/latest/
import requests

class NodePingInterface:

	accounts = {}

	def __init__(self, apitoken):
		self.apitoken = apitoken
		self.update_accounts()

	# curl -X GET 'https://api.nodeping.com/api/1/accounts'
	def update_accounts(self):
		payload = {'token':self.apitoken}
		response = requests.get('https://api.nodeping.com/api/1/accounts', json=payload).json()
		for customerid in response:
			account = NPAccount(**self.get_account(customerid))
			#response['customerid'] = customerid
			#account = NPAccount(**data)
			self.accounts[account.customerid] = account

	def get_account(self, customerid):
		payload = {
			'token':self.apitoken,
			'customerid':customerid
		}
		response = requests.get('https://api.nodeping.com/api/1/accounts', json=payload).json()
		return response



	# POST - Create a new SubAccount. Note that id and customerid are not supported for POST calls on accounts.
	# 
    # name - required - a name for the subaccount, used primarily as a label for the accounts list.
    # contactname - required - name of the primary contact for the subaccount
    # email - required - email of the primary contact for the subaccount
    # timezone - optional - GMT offset for the account (example: '-7' is US Phoenix)
    # location - optional - The default region for checks for the account. This is a geographical region where our probe servers are located. Currently this can be set to 'nam' for North America, 'eur' for Europe, 'eao' for East Asia/Oceania, or 'wlw' for world wide.
    # emailme - optional - set to 'yes' to opt-in the subaccount for NodePing service and features email notifications. Defaults to 'no' if absent.
	# 
	# curl -X POST 'https://api.nodeping.com/api/1/accounts?timezone=3&name=My+Company+Name&contactname=Joe+Smith&email=joe@example.com&timezone=3&location=eur&emailme=yes' 
	
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
		account = NPAccount(response)
		return response


class NPAccount(object):
	
	def __init__(self, status, sdomain, planId, creation_date, timezone, emailme, _id, type, customer_name, defaultlocations = "", parent = "", customerid = "", reports = "", modified = "", notice = "", trialend = "", promo = "", suref = "", checkcount = 0, statustime = 0, nextBillingDate = 0, billingDayOfMonth = 0, cstatus = ""):
		self.status =  status
		self.sdomain =  sdomain
		self.parent =  parent
		self.planId =  planId
		self.defaultlocations =  defaultlocations
		self.creation_date =  creation_date
		self.timezone =  timezone
		self.emailme =  emailme
		self._id =  _id
		self.type =  type
		self.customerid =  customerid
		self.customer_name = customer_name
		self.reports = reports
		self.modified = modified
		self.notice = notice
		self.trialend = trialend
		self.promo = promo
		self.suref = suref
		self.checkcount = checkcount
		self.statustime = statustime
		self.nextBillingDate = nextBillingDate
		self.billingDayOfMonth = billingDayOfMonth
		self.cstatus = cstatus

	def details(self):
		return {'name':self.customer_name, 'customerid':self.customerid, 'parent':self.parent, 'status':self.status}