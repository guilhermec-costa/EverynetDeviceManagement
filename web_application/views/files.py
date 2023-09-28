import pandas as pd
from .messages import Colors
import os

class File:
    messages = Colors()
    def __init__(self, path):
        self.path = path
        self.extension = self._check_extension()
        self.content = self.read_file()
    
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
        except (FileNotFoundError, UnboundLocalError):
            self.messages.error('File does not exist in your operational system!')
        
    def adjust_content(self):
        self.content['app_eui'] = self.content['app_eui'].astype(str)
        self.content['dev_eui'] = self.content['dev_eui'].astype(str)
        self.content['dev_addr'] = self.content['dev_addr'].astype(str)
        
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
        
        for column in self.content.columns:
            if column in mandatory_columns.keys():
                mandatory_columns[column] += 1
        
        self.messages.prLightPurple('-' * 30)
        print('Checking existing columns...')
        for column, value in mandatory_columns.items():
            print(f'"{column}" is ', end='')
            if value == 1:
                self.messages.prGreen('OK')
            else:
                self.messages.error('MISSING')
        self.messages.prLightPurple('-' * 30)
        self.ok_columns = False if 0 in mandatory_columns.values() else True


    def _check_size(self):
        self.ok_size = True if self.content.shape[0] >= 1 \
        else False
        
    @property
    def is_able_to_use(self):
        return True if self.ok_size and self.ok_columns \
            else False