from functools import wraps
from sre_constants import OPCODES
from typing import List, Union, NoReturn
from login import Login, error, warning, prLightPurple
from requisitions import get_device

class userMenu:
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
        prLightPurple('=' * 3 * bar_size_to_display)
        for idx, option in enumerate(self.menu_options):
            error(f'{idx + 1})')
            print(end='')
            print(f'\033[1;37m{option}\033[m')
        prLightPurple('=' * 3 * bar_size_to_display)
    
    def ask_option(self):
        while True:
            try:
                opc = int(input('Digite uma opção > '))
                if 1 <= opc <= len(self.menu_options):
                    return opc
                else:
                    error(f'{opc} is not a valide option!')
            except ValueError:
                error('Type a valid integer!')
