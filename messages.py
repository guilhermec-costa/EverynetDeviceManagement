
class Colors:
    
    def error(self, message, endline=False):
        print(f"\033[1;91m{message}\033[00m") if endline is False \
        else print(f"\033[1;91m{message}\033[00m", end=' ')
        
    def warning(self, message, endline=False):
        print(f"\033[1;93m{message}\033[00m") if endline is False \
        else print(f"\033[1;93m{message}\033[00m", end=' ')
        
    def prLightPurple(self, message, endline=False):
        print(f"\033[1;96m{message}\033[00m") if endline is False \
        else print(f"\033[1;96m{message}\033[00m", end=' ')

    def prGreen(self, message, endline=False):
        print(f"\033[1;92m{message}\033[00m") if endline is False \
        else print(f"\033[1;92m{message}\033[00m", end=' ')

    def prPurple(self, message, endline=False):
        print(f"\033[95m{message}\033[00m") if endline is False \
        else print(f"\033[95m{message}\033[00m", end=' ')