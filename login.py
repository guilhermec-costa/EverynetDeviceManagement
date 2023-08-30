import requests
from getpass import getpass
import json

def error(message):
    print(f"\033[1;91m{message}\033[00m", end=' ')
    
def warning(message):
    print(f"\033[1;93m{message}\033[00m")
    
    
def prLightPurple(message):
    print(f"\033[1;96m{message}\033[00m")

def prGreen(message):
    print(f"\033[1;92m{message}\033[00m")

def prPurple(message):
    print(f"\033[95m{message}\033[00m", end=' ')

class Login:
    base_url = 'https://ns.atc.everynet.io/api/v1.0'

    def __init__(self):
        prLightPurple('-' * 30)
        self.email = 'alberto.alexandre@nepen.org.br' #input('\nYour email > ')
        self.pwd = '9dW5jW74qWfpiuQ' #getpass('Password > ')
        self.token = None
        return
    


    def get_token(self):
        dynamic_url = '/auth'
        q_url = self.base_url + dynamic_url

        payload = json.dumps({'email': self.email,
                              'password': self.pwd})

        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", q_url, headers=headers, data=payload)
        if response.status_code == 200:
            self.token = response.json()['access_token']
            return response.json()['access_token']
        print(f'{self.email} is invalid!')
        return None
    
    def check_request_status(self, request):
        if request.status_code == 200:
            return request.json()
        else:
            error(f'Error on get device info! ERROR >\n\n{request.text}\n')
        return None



    def get_device(self):

        deveui = input('Type a deveui > ')
        prLightPurple('...................')
        dynamic_url = self.base_url + f'/devices/{deveui}?access_token={self.token}'

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Cookie': f'session_token={self.token}'
        }

        response = requests.request('GET', dynamic_url, headers=headers, data="")

        return self.check_request_status(response)

    def get_multi_devices(self):
        offset = int(input('Offset (min number to get) > '))
        limit = int(input('Limit (max number to get) > '))
        dynamic_url = f'/devices?offset={offset}&limit={limit}'
        q_url = self.base_url + dynamic_url


        headers = {
        'Authorization': f'Bearer {self.token}',
        'Cookie': f'session_token={self.token}'
        }

        response = requests.request('GET', url=q_url, headers=headers, data="")

        return self.check_request_status(response)

    def display_devices(self, data):
        counter = 0
        for devices in data['devices']:
            counter +=1
            prLightPurple('=========================')
            warning(f'Device {counter} ({devices["dev_eui"]})')
            for key, value in devices.items():
                prPurple(f'{key} -> ')
                print(value)
        






