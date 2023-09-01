import requests
from getpass import getpass
import json
from messages import Colors

# implementar classe de tratamento de exceção

class Session:
    base_url = 'https://ns.atc.everynet.io/api/v1.0'
    token = ""
    messages = Colors()

    def __init__(self):
        self.messages.prLightPurple('-' * 30)
        self.email = 'alberto.alexandre@nepen.org.br' #input('\nYour email > ')
        self.pwd = '9dW5jW74qWfpiuQ' #getpass('Password > ')
        self.token = None
        return
    
    def generate_empty_device(self):
        return {}

    def get_token(self):
        dynamic_url = '/auth'
        q_url = self.base_url + dynamic_url
        payload = json.dumps({'email': self.email, 'password': self.pwd})
        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", q_url, headers=headers, data=payload)
        if response.status_code == 200:
            Session.token = response.json()['access_token']
            return Session.token
        
        self.messages.error(f'Email or password incorret!')
        return None
    
    def _check_request_status(self, request, code=200):
        if request.status_code == code:
            return request.json()
        else:
            self.messages.error(f'Requisition failed! ERROR >\n\n{request.text}\n')
        return None
        