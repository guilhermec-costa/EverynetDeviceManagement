import requests
from getpass import getpass
import json
import pandas as pd
from menu import userMenu
from messages import Colors
import os

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
    
    def _check_request_status(self, request):
        if request.status_code == 200:
            return request.json()
        else:
            self.messages.error(f'Error on get device info! ERROR >\n\n{request.text}\n')
        return None


class Device(Session):
    all_devices = []
    
    def __init__(self):
        self.init_device = None
        self.device_prototype = None
        
    def get_device(self):

        deveui = input('Type a deveui > ')
        self.messages.prLightPurple('...................')
        dynamic_url = Session.base_url + f'/devices/{deveui}?access_token={Session.token}'
        headers = {
            'Authorization': f'Bearer {Session.token}',
            'Cookie': f'session_token={Session.token}'
        }

        response = requests.request('GET', dynamic_url, headers=headers, data="")
        return self._check_request_status(response)

    def get_multi_devices(self):
        offset = int(input('Offset (min number to get) > '))
        limit = int(input('Limit (max number to get) > '))
        dynamic_url = f'/devices?offset={offset}&limit={limit}'
        q_url = Session.base_url + dynamic_url
        headers = {
        'Authorization': f'Bearer {Session.token}',
        'Cookie': f'session_token={Session.token}'
        }

        response = requests.request('GET', url=q_url, headers=headers, data="")
        return self._check_request_status(response)

    @classmethod
    def display_devices(cls, data):
        counter = 0
        for devices in data['devices']:
            counter +=1
            cls.messages.prLightPurple('=========================')
            cls.messages.warning(f'Device {counter} ({devices["dev_eui"]})')
            for key, value in devices.items():
                cls.messages.prPurple(f'{key} -> ')
                print(value)

    def build_device(self):
        device = self.generate_empty_device()
        device['dev_eui'] = input('\033[1;96mDeveui > \033[00m')
        device['app_eui'] = input('\033[1;96mAppeui > \033[00m')
        #device['tags'] = input('\033[1;96mTags (separate by commas) > \033[00m').split(',')
        #device['tags'] = [tags.strip(' ') for tags in device['tags']]
        device['tags'] = 'TV_2'
        device['activation'] = 'ABP'
        device['encryption'] = 'NS'
        device['dev_addr'] = input('\033[1;96mDev address > \033[00m')
        device['nwkskey'] = input('\033[1;96mNetwork secret key > \033[00m')
        device['appskey'] = input('\033[1;96mApp secret key > \033[00m')
        device['dev_class'] = 'A'
        device['counter_size'] = 4
        device['adr'] = {
            'tx_power':30,
            'datarate':0,
            'mode':'static'
        }
        device['band'] = 'LA915-918A'
        self.device_prototype = device
        self.init_device = json.dumps(device)
        
        self.all_devices.append(self.device_prototype)
    
    def create_multiple_devices_mannualy(self):
        print('\033[1;96m====================\033[00m')
        while True:
            keep_creating = ""
            self.build_device()
            print('\033[1;96m====================\033[00m')
            while keep_creating not in ('Y', 'y', 'n', 'N'):
                keep_creating = input('Create more devices: Y/n > ')
            if keep_creating in ('Y','y'):
                continue
            else:
                return
    
    def create_via_file(self):
        file_path = input('Type the file absolute path > ')
        file_instancy = File(file_path)
        print()
        print('File content previous')
        print(file_instancy.content)
            
        


    def create_multiple_devices(self):
        print('To create multiple devices, choose one of the options below ')
        file_menu = userMenu(['Manually', 'JSON file', 'CSV file', 'XLSX file', 'Back main menu'], key='file_menu')
        file_menu.show()
        
        opc = file_menu.ask_option()
        self.create_via_file()

    def create_device(self):
        for device in self.all_devices:
            print(f'Device {device["dev_eui"]} has been created!')
            self.all_devices.remove(device)

class File:
    messages = Colors()
    def __init__(self, path):
        self.path = path
        self.extension = self._check_extension()
        self.content = self.read_file()
        self.is_able_to_create = False
        if self.extension in ('.xlsx', '.csv'):
            self._check_columns()
    
    def _check_extension(self):
        extension = os.path.splitext(self.path)[1]
        return extension
    
    def read_file(self):
        try:
            match self.extension:
                case '.json':
                    content = pd.read_json(rf'{self.path}')
                case '.xlsx':
                    content = pd.read_excel(rf'{self.path}')         
                case '.csv':
                    content = pd.read_csv(rf'{self.path}')
            return content
        except FileNotFoundError:
            self.messages.error('File does not exist in your operation system!')
        
        except UnboundLocalError:
            self.messages.warning('Verify the file extension!')
    
    def _check_columns(self):
        self.content.columns = [col.strip().lower().replace(' ', '_')\
                                        for col in self.content.columns]
        mandatory_columns = {
            'dev_eui':0,
            'app_eui':0,
            'dev_addr':0,
            'nwkskey':0,
            'appskey':0
        }
        
        if self.extension in ('.csv', '.xlsx'):
            for column in self.content.columns:
                if column in mandatory_columns.keys():
                    mandatory_columns[column] += 1
        
        print('Checking existing columns...')
        for column, value in mandatory_columns.items():
            print(f'"{column}" is ', end='')
            if value == 0:
                self.messages.prGreen('OK')
            else:
                self.messages.error('MISSING\n')
                self.is_able_to_create = False