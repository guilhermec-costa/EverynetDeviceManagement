from menu import userMenu
from session import Session, Device
from messages import Colors

def run_app():
    messages = Colors()
    token = None
    messages.prLightPurple('*' * 2 * len('Seja Bem Vindo'))
    messages.warning(f'{"Your welcome!":^30}')
    messages.prLightPurple('*' * 2 * len('Seja Bem Vindo'))
    print()

    while True:
        menu = userMenu(['Get API token', 'Get single device', 'Get multiple devices', 'Create single device', 'Create multiple devices', 'Quit'], key='main_menu')
        menu.show()
        opc = menu.ask_option()
        if opc == 1:
            session = Session()
            token = session.get_token()
            if token is not None:
                messages.prGreen(f'Your token: {token}')
        if opc == 6:
            print('Quitting the programm...')
            exit()

        if token is not None:
            device = Device()
            match opc:
                case 2:
                    device_info = device.get_device()
                    Device.display_devices(device_info)
                case 3:
                    devices_info = device.get_multi_devices()
                    Device.display_devices(devices_info)
                case 4:
                    device.build_device()
                    device_created = device.create_single_device()
                    if device_created is not None:
                        messages.prGreen(f'{device.device_prototype["dev_eui"]} has been created!')
                    
                    
                case 5:
                    device.create_multiple_devices()

        else:
            messages.warning('You must generate a token first!')
                    
if __name__ == '__main__':
    run_app()
