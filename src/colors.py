
class Colors:
    BLACK   = '\033[0;30m'
    RED     = '\033[0;31m'
    GREEN   = '\033[0;32m'
    YELLOW  = '\033[0;33m'  
    BLUE    = '\033[0;34m'
    PINK    = '\033[0;34m'
    CYAN    = '\033[0;36m'
    GREY    = '\033[0;37m'
    ENDC    = '\033[0m'

    @staticmethod
    def queryPrintColor(color):
        if (Colors.tempColor != color):
            Colors.tempColor = color
            print(color, end='')

    tempColor = None