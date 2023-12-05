import sys
import time

from prompt_toolkit import PromptSession, print_formatted_text, prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers import PythonLexer
from pygments.styles.native import NativeStyle
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter

class StyleLog:

    styler = None

    style = Style.from_dict({
        'input': 'bg:#000000 #00ff00',
        'assistant': 'bg:#000000 #7777ff',
        'system': 'bg:#000000 #ff00ff',
    })

    def __init__(self):
        self.styler = PromptSession(lexer=PygmentsLexer(PythonLexer), auto_suggest=AutoSuggestFromHistory(), history=FileHistory('history.txt'))

    def prompt(self, role: str, message: str):
        if role == 'assistant':
            print_formatted_text(HTML(f"<assistant>Assistant: </assistant>%s") % (message, ), style = self.style)
        elif role == 'user':
            user_input = prompt(
                [
                    ('class:input', "\nInput: "),
                    ('', '')
                ],
                style = self.style
            )
            return user_input
        elif role == 'system':
            print_formatted_text(HTML(f'<system>System:</system> {message}'), style = self.style)
        elif role == 'none':
            print_formatted_text(HTML(f'{message}'), style = self.style)
        return

    def show_ellipsis(self, api_call_done):
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
