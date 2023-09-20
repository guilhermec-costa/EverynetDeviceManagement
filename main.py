from menu import userMenu
from session import Session
from messages import Colors
from devices import Device

def run_app():
    messages = Colors()
    token = None
    messages.prPurple('*' * 32)
    messages.warning(f'\033[1;95;40m*\033[m\033[1;30;47m{"You are welcome!":^30}\033[00m\033[1;95;40m*\033[m')
    messages.prPurple('*' * 32)
    print()

    while True:
        menu = userMenu(['Get API token', 'Get single device', 'Get multiple devices', 'Get uplink messages', 'Create single device', 'Create multiple devices',
                         'Edit single device', 'Edit multiple devices', 'Delete single device', 'Delete multiple devices', 'Quit'], key='main_menu')
        menu.show()
        opc = menu.ask_option()
        if opc == 1:
            session = Session()
            token = session.get_token()
            if token is not None:
                messages.prGreen(f'Your token: {token}')
        if opc == 11:
            messages.prLightPurple('\nThank you for use!\nQuitting the program...')
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
                    device_messages = device.get_uplink_message()
                    device.display_messages(device_messages)
                    base64_payload, hex_payload = Device.get_payload_from_uplinks(device_messages)
                    binary_lats, binary_longs = Device.extract_coord_bits_from_payload(hex_payload, 16)
                    float_latitudes, float_longitudes = Device.extract_coordinates(binary_lats), Device.extract_coordinates(binary_longs)
                    print(float_latitudes, float_longitudes)

                case 5:
                    device.build_device()
                    device_created = device.create_single_device()
                    if device_created is not None:
                        messages.prGreen(f'{device.device_prototype["dev_eui"]} has been created!')
                    
                    
                case 6:
                    device.create_multiple_devices()
                case 7:
                    messages.warning('Editing a single device!')
                case 8:
                    messages.warning('Editing multiple devices!')
                case 9:
                    device.delete_single_device()
                case 10:
                    messages.warning('Deleting multiple devices!')

        else:
            messages.warning('You must generate a token first!')
                    
if __name__ == '__main__':
    run_app()
