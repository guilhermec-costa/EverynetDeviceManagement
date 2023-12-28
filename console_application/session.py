import requests
from getpass import getpass
import json
from messages import Colors
from typing import Union

# implementar classe de tratamento de exceção

class Session:
    base_url = 'https://ns.atc.everynet.io/api/v1.0'
    token = ""
    messages = Colors()
    header = {'Cookie': f'session_token={token}'}

    def __init__(self):
        self.messages.prLightPurple('-' * 30)
        self.email = "alberto.alexandre@nepen.org.br" #input('\nYour email > ')
        self.pwd = "9dW5jW74qWfpiuQ" #getpass('Password > ')
        self.token = None
        return
    
    def generate_empty_device(self) -> dict:
        return {}

    def get_token(self) -> str | None:
        dynamic_url = '/auth'
        q_url = self.base_url + dynamic_url
        payload = json.dumps({'email': self.email, 'password': self.pwd})
        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", q_url, headers=headers, data=payload)
        if response.status_code == 200:
            Session.token = response.json()['access_token']
            self.token = Session.token
            self.header['Cookie'] = f'session_token={self.token}'
            return Session.token
        
        self.messages.error(f'Email or password incorret!')
        return None
    
    def parse_request_return(self, request:requests.request):
        request_structure = {
            204:"The request has succeeded, but the client did not return any content"
        }
        self.messages.prGreen(request_structure[request.status_code])
        return
        
    def _check_request_status(self, request:requests.request, code:int = 200):
        if request.status_code == code:
            try:
                return request.json()
            except Exception as error:
                self.messages.warning('Requesition return is empty!')
                self.messages.warning('Requisition status code: ', endline=True)
                self.messages.prGreen(request.status_code)
                self.parse_request_return(request)              
        else:
            self.messages.error(f'Requisition failed! ERROR >\n\n{request.text}\n')
        return None
        
