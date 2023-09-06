from typing import List, Union, NoReturn
from messages import Colors

class userMenu:
    messages = Colors()
    """
    Generates a user menu.
        Parameters:
            options (Union[List[str], None]): a list of options, or simply None
            key (str): unique identify the menu
    """

    def __init__(self, options: Union[List[str], None] = None, key:str = None) -> None:
        self.menu_options = options if options is not None else []
        self.__convert_types
        self.menu_type = key

    def _str_(self) -> str:
        print(f"Menu about {self.menu_type}. Options available > {[f'{opc}, ' for opc in self.menu_options]}")
    
    def _repr_(self) -> str:
        print("userMenu(['a', 'b', 'c'], key='random')")

    def _add_(self, menu2):
        return self.menu_options + menu2.menu_options
    
    @property
    def __get_max_option_length(self) -> int:
        max_size_option = max(self.menu_options, key=lambda x: len(x))
        return max_size_option.__len__()
    
    @property
    def __convert_types(self) -> NoReturn:
        for idx in range(self.menu_options.__len__()):
            self.menu_options[idx] = str(self.menu_options[idx])

    def add_options(self, options:List[str]) -> NoReturn:
        [self.menu_options.append(option) for option in options]

    def del_option(self, options:List[str]) -> NoReturn:
        for opc in options:

            self.menu_options.remove(opc) if opc in self.menu_options \
            else print(f'{opc} is not previous registred!\n')
        
    def show(self):
        bar_size_to_display = self.__get_max_option_length
        self.messages.prPurple('=' * 3 * bar_size_to_display)
        for idx, option in enumerate(self.menu_options):
            if option.lower().__contains__('get'):
                print(f'\033[1;30;46m{f"{idx + 1})":<3}\033[00m\033[1;30;46m{option:<28}|\033[000m ')
            elif option.lower().__contains__('edit'):
                print(f'\033[1;30;43m{f"{idx + 1})":<3}\033[00m\033[1;30;43m{option:<28}|\033[000m ')
            elif option.lower().__contains__('create'):
                print(f'\033[1;30;42m{f"{idx + 1})":<3}\033[00m\033[1;30;42m{option:<28}|\033[000m ')
            elif option.lower().__contains__('delete') or option.lower().__contains__('quit'):
                print(f'\033[1;30;41m{f"{idx + 1})":<3}\033[00m\033[1;30;41m{option:<28}|\033[000m ')
            else:
                self.messages.error(f'{idx + 1})', endline=True)
                print(f'\033[1;37m{option}\033[m')
        self.messages.prPurple('=' * 3 * bar_size_to_display)
    
    
    def validate_option(self, error):
        if isinstance(error, ValueError):
            self.messages.error('Type a valid integer!')

    def ask_option(self):
        while True:
            try:
                opc = int(input('Digite uma opção > '))
                if 1 <= opc <= len(self.menu_options):
                    return opc
                else:
                    self.messages.error(f'{opc} is not a valid option!')
            
            except Exception as error:
                self.validate_option(error)
                
            except KeyboardInterrupt:
                self.messages.prLightPurple('\nThank you for use!\nQuitting the program...')
                exit()
    
