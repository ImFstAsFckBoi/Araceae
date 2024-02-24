

_LEFT = 97
_RIGHT = 100
_UP = 119
_DOWN = 115
_CLEAREOL = '\033[2K'


def _cmdprint(*args, **kwargs):
    print(*args, **kwargs, end='')


def SAVE_CURSOR(): _cmdprint('\033[s')
def RESTORE_CURSOR(): _cmdprint('\033[u')
def CLEAREOL(): _cmdprint(_CLEAREOL)
def RESET(): _cmdprint('\033[0m')
def HIDE_CURSOR(): _cmdprint('\033[?25l')
def SHOW_CURSOR(): _cmdprint('\033[?25h')


def println(*args, **kwargs):
    CLEAREOL()
    print(*args, **kwargs)
