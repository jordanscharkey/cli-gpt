import sys

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

class StyleLog:

    def prompt(role: str):
        
    
    def show_ellipsis():
        loop = True
        while loop:
            for i in range(0, 4):
                if api_call_done.is_set():
                    loop = False
                    sys.stdout.write('\r' + ' ' * 4 + '\r')
                    break
                time.sleep(1)
                sys.stdout.write('.')
                sys.stdout.flush()
            sys.stdout.write('\r' + ' ' * 4 + '\r')
            sys.stdout.flush()
