
class Colors:
    
    def error(self, message):
        print(f"\033[1;91m{message}\033[00m", end=' ')
        
    def warning(self, message):
        print(f"\033[1;93m{message}\033[00m")
        
    def prLightPurple(self, message):
        print(f"\033[1;96m{message}\033[00m")

    def prGreen(self, message):
        print(f"\033[1;92m{message}\033[00m")

    def prPurple(self, message):
        print(f"\033[95m{message}\033[00m", end=' ')