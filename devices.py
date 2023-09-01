from session import Session
from messages import Colors
import requests
import json
from files import File
from menu import userMenu

class Device(Session):
    all_devices = []
    messages = Colors()
    
    def __init__(self):
        self.ready_device = None
        self.device_prototype = None
        
    def get_device(self):

        self.messages.prLightPurple('*' * 30)
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
        while True:
            try:
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
            except ValueError:
                self.messages.error('Type a valid integer!')
                self.messages.prPurple('*' * 25)
                continue
            except KeyboardInterrupt:
                self.messages.prLightPurple('\nThank you for use!\nQuitting the program...')
                exit()

    @classmethod
    def display_devices(cls, data):
        counter = 0
        if data is not None:
            if len(data) > 1:
                for devices in data['devices']:
                    counter +=1
                    cls.messages.prLightPurple('=========================')
                    cls.messages.warning(f'Device {counter} ({devices["dev_eui"]})')
                    for key, value in devices.items():
                        cls.messages.prPurple(f'{key} -> ', endline=True)
                        print(value)
            else:
                print('Device ', end='')
                cls.messages.prLightPurple(data['device']['dev_eui'])
                for key, value in data['device'].items():
                        cls.messages.prPurple(f'{key} -> ', endline=True)
                        print(value)

    def build_device(self, row=None, ask_default_values=False):
        self.messages.prPurple('*' * 30)
        device = self.generate_empty_device()

        if not ask_default_values:
            device['tags'] = ['TV_2']
            device['activation'] = 'ABP'
            device['encryption'] = 'NS'
            device['dev_class'] = 'A'
            device['adr'] = {
                # 30dBm
                'tx_power':0,
                'datarate':0,
                'mode':'static'
            }
            device['band'] = 'LA915-928A'
            device['counters_size'] = 4
        else:
            device['tags'] = input('\033[1;96mTags (separate by commas) > \033[00m').split(',')
            device['tags'] = [tags.strip(' ') for tags in device['tags']]
            device['activation'] = input('\033[1;96m Activation > \033[00m')
            device['encryption'] = 'NS'
            device['dev_class'] = 'A'
            device['adr'] = {
                # 30dBm
                'tx_power':0,
                'datarate':0,
                'mode':'static'
            }
            device['band'] = 'LA915-928A'
            device['counters_size'] = 4
        
        # perguntas para o usuário dos valores não constantes, e caso não seja um upload de arquivo
        if row is None:
            device['dev_eui'] = input('\033[1;96mDeveui > \033[00m')
            device['app_eui'] = input('\033[1;96mAppeui > \033[00m')
            device['dev_addr'] = input('\033[1;96mDev address > \033[00m')
            device['nwkskey'] = input('\033[1;96mNetwork secret key > \033[00m')
            device['appskey'] = input('\033[1;96mApp secret key > \033[00m')
            self.messages.prPurple('*' * 30)
        else:
            device['dev_eui'] = row.dev_eui
            device['app_eui'] = row.app_eui
            device['dev_addr'] = row.dev_addr
            device['nwkskey'] = row.nwkskey
            device['appskey'] = row.appskey
            
        # prototype: versão dicionário
        self.device_prototype = device
        
        #ready_device: versão json
        self.ready_device = json.dumps(device)
        
        self.all_devices.append(self.device_prototype)
    
    def create_multiple_devices_mannualy(self):
        print('\033[1;96m====================\033[00m')
        while True:
            keep_creating = ""
            self.build_device()
            device_created = self.create_single_device()
            if device_created is not None:
                self.messages.prGreen(f'{self.device_prototype["dev_eui"]} has been created!')
                
            print('\033[1;96m====================\033[00m')
            while keep_creating not in ('Y', 'y', 'n', 'N'):
                keep_creating = input('Create more devices: Y/n > ')
            if keep_creating in ('Y','y'):
                continue
            else:
                return
    
    def manage_excelfile(self, file):
        file._check_columns()
        file._check_size()
        if file.is_able_to_use:
            file.adjust_content()
            options = ""
            self.messages.prGreen('It is possible to use the sheet!')
            self.messages.prLightPurple('File content previous')
            print(file.content.head(5))
            while options not in ('Y', 'y', 'n', 'N'):
                confirmation = input('\033[1;93mAre you sure you want to create these devices: Y/n > \033[00m')
                if confirmation in ('Y', 'y'):
                    print('Creating devices!')
                    for row in file.content.itertuples():
                        self.build_device(row=row)
                        device_created = self.create_single_device()
                        if device_created is not None:
                            self.messages.prGreen(f'{self.device_prototype["dev_eui"]} has been created!')

                    return
                else:
                    return
        else:
            self.messages.error('It is not possible to use the sheet!')
            return

    def manage_jsonfile(self, file):
        self.messages.warning('This feature is not implemented yet!')
        return

    def create_via_file(self, file_type):
        file_path = input(f'Type the \033[1;92m{file_type}\033[00m absolute path > ')
        file_instancy = File(file_path)
        print()
        match file_instancy.extension:
            case '.xlsx' | '.csv':
                self.manage_excelfile(file_instancy)
            case '.json':
                self.manage_jsonfile(file_instancy)

        
    def create_multiple_devices(self):
        print('To create multiple devices, choose one of the options below ')
        file_menu = userMenu(['Manually', 'JSON file', 'CSV file', 'XLSX file', 'Back main menu'], key='file_menu')
        file_menu.show()
        
        opc = file_menu.ask_option()
        match opc:
            case 1:
                self.create_multiple_devices_mannualy()
            case 2 | 3 | 4:
                self.create_via_file(file_type=file_menu.menu_options[opc-1])
            case 5:
                print('retornando')
                return

    def create_single_device(self, method='POST'):
        dynamic_url = f"/devices"
        q_url = self.base_url + dynamic_url
        
        payload = self.ready_device
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Session.token}',
            'Cookie': f'session_token={Session.token}'
        }
        response = requests.request(method=method, url=q_url, headers=headers, data=payload)
        return self._check_request_status(response, code=201)
    
    def edit_single_device(self):
        self.build_device(ask_default_values=input('Ask default values > '))
        self.create_single_device(method='PATCH')