import requests
from login import Login

def get_device(token):
    deveui = input('Type a deveui > ')
    base_url = Login.base_url
    dynamic = f'/devices/{deveui}/?access_token={token}'
    return dynamic
    
