import requests
from menu import userMenu
from login import Login, warning, error, prLightPurple, prGreen
from requisitions import get_device

def run_app():
    token = None
    prLightPurple('*' * 2 * len('Seja Bem Vindo'))
    warning(f'{"Seja Bem vindo":^30}')
    prLightPurple('*' * 2 * len('Seja Bem Vindo'))
    print()

    while True:
        menu = userMenu(['Get API token', 'Get single device', 'Get multiple devices', 'Quit'], key='main_menu')
        menu.show()
        opc = menu.ask_option()
        if opc == 1:
            session = Login()
            token = session.get_token()
            if token is not None:
                prGreen(f'Your token: {token}')
        if opc == 4:
            print('Quitting the programm...')
            exit()

        if token is not None:
            match opc:

                case 2:
                    if token is not None:
                        device_info = session.get_device()
                    else:
                        Login.error('Generate a token first!')
                case 3:
                    if token is not None:
                        devices_info = session.get_multi_devices()
                        session.display_devices(devices_info)
        else:
            warning('You must generate a token first!')
                    



if __name__ == '__main__':
    run_app()
