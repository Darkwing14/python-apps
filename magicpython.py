import random
import re
import time
import platform
import sys
import shutil
from math import tau, pi, e, sin, cos, radians, degrees
if platform.system() == 'Windows':
    import msvcrt
else:
    import tty
    import termios
    import select

__version__ = '0.1.3'
__author__ = "Darkwing"
__license__ = "MIT License"
__lambdas__ = {}

def run_immediately(func):
    func()  # run right away
    return func  # return the original func so other decorators can still wrap it

def loop(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

class text:
    @staticmethod
    def colortext(text, color):
        return f"\033[3{color}m{text}\033[0m"
    
    @staticmethod
    def colorget(colorname):
        colors = {
            "black": 0, "red": 1, "green": 2, "yellow": 3,
            "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
            "grey": 7, "gray": 7, "purple": 5, "orange": 1
        }
        try:
            return colors[colorname.lower()]
        except KeyError:
            raise ValueError(f"No match for {colorname}!")
    
    @staticmethod
    def modify(text, *modifications):
        style_codes = {
            "bold": 1, "italic": 3, "oblique": 3, "underline": 4,
            "blink": 5, "highlight": 7, "strikethrough": 9
        }
        codes = []
        for m in modifications:
            if m not in style_codes:
                raise ValueError(f"No match for {m}!")
            codes.append(str(style_codes[m]))
        return f"\033[{';'.join(codes)}m{text}\033[0m"

class functions:
    @staticmethod
    def combinelambdas(*funcs):
        return lambda: tuple(f() for f in funcs)

    @staticmethod
    def loop(times, function):
        for _ in range(times):
            function()

    @staticmethod
    def define(function, name):
        __lambdas__[name] = function

    @staticmethod
    def call(name):
        try:
            func = __lambdas__[name]
        except KeyError:
            raise ValueError(f"No lambda defined with name '{name}'")
        func()

class rand:
    @staticmethod
    def chaos(max_val=None, positive=False):
        if max_val is None:
            return random.random()
        return random.randint(1 if positive else 0, max_val)
    
    @staticmethod
    def dice(notation, summed=True):
        try:
            notation = notation.lower().replace(" ", "")
            match = re.fullmatch(r"(\d*)d(\d+)([+-]\d+)?", notation)
            if not match:
                raise ValueError

            count = int(match.group(1)) if match.group(1) else 1
            sides = int(match.group(2))
            modifier = int(match.group(3)) if match.group(3) else 0

            if count <= 0 or sides <= 0:
                raise ValueError("Dice count and sides must be positive integers.")

            rolls = [random.randint(1, sides) for _ in range(count)]
            return sum(rolls) + modifier if summed else rolls

        except Exception:
            raise ValueError("Invalid dice notation. Try '2d6+3', 'd20', or '3d4-1'.")

def fill(opacity):
    match opacity:
        case 0:
            return " "
        case 1:
            return "░"
        case 2:
            return "▒"
        case 3:
            return "▓"
        case 4:
            return "█"
        case _:
            raise ValueError(f"No match for {opacity}!")

def throw(error): # For people used to javascript I guess
    raise error

def wait(seconds):
    time.sleep(seconds)

def waitms(milliseconds):
    time.sleep(milliseconds / 1000)

def clear():
    print("\033[2J\033[H")

_key_map = {
    'a': ord('a'),
    'b': ord('b'),
    'c': ord('c'),
    'd': ord('d'),
    'e': ord('e'),
    'f': ord('f'),
    'g': ord('g'),
    'h': ord('h'),
    'i': ord('i'),
    'j': ord('j'),
    'k': ord('k'),
    'l': ord('l'),
    'm': ord('m'),
    'n': ord('n'),
    'o': ord('o'),
    'p': ord('p'),
    'q': ord('q'),
    'r': ord('r'),
    's': ord('s'),
    't': ord('t'),
    'u': ord('u'),
    'v': ord('v'),
    'w': ord('w'),
    'x': ord('x'),
    'y': ord('y'),
    'z': ord('z'),
    '0': ord('0'),
    '1': ord('1'),
    '2': ord('2'),
    '3': ord('3'),
    '4': ord('4'),
    '5': ord('5'),
    '6': ord('6'),
    '7': ord('7'),
    '8': ord('8'),
    '9': ord('9'),
    'space': ord(' '),
    'enter': 13,
    'backspace': 8,
    'tab': 9,
    'esc': 27,
}

def keypressed(key_name):
    key = _key_map.get(key_name)
    if key is None:
        print(f"Unknown key: {key_name}")
        return False

    if platform.system() == 'Windows':
        if msvcrt.kbhit():
            pressed_key = msvcrt.getch()
            return ord(pressed_key) == key

    elif platform.system() in ['Linux', 'Darwin']:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            if select.select([sys.stdin], [], [], 0.1)[0]:
                pressed_key = sys.stdin.read(1)
                return ord(pressed_key) == key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return False

def timeunit(unit):
    t = time.localtime()
    match unit:
        case "h":
            return t.tm_hour
        case "i":
            return ((t.tm_hour - 1) % 12) + 1
        case "m":
            return t.tm_min
        case "s":
            return t.tm_sec
        case "p":
            return "AM" if t.tm_hour < 12 else "PM"
        case "d":
            return t.tm_mday
        case _:
            raise ValueError(f"Unknown unit: {unit}")

def loadingbar(progress):
    progress = max(0, min(100, progress))
    clear()
    equals = "=" * (progress // 10)
    minus = "-" * (10 - (progress // 10))
    print(f"[{equals}{minus}] Loading...")

def main():
    print("Welcome to the magic python module! This module is meant to be the swiss army knife of modules!")
    roll = rand.dice("d6")
    print(f"Rolling a die... {roll}")
    print(text.colortext("Colorful!", rand.chaos(6, True)))
    print("Now hold A for me!")
    wait(2)
    print("Woo!" if keypressed("a") else "Hey! You didn't press A!")

def ver():
    print(__version__)
    print(__author__)
    print(__license__)

def terminalsize(dim=None):
    """
    Get terminal size in columns or lines (rows).

    Args:
        dim (str): 'c', 'col', 'columns' → returns width
                   'r', 'row', 'rows', 'lines' → returns height
                   None or invalid → returns (columns, lines)

    Returns:
        int or tuple: Width, height, or both.
    """
    size = shutil.get_terminal_size(fallback=(80, 24))
    if dim in ('c', 'col', 'column', 'columns'):
        return size.columns
    elif dim in ('r', 'row', 'rows', 'line', 'lines'):
        return size.lines
    else:
        return size.columns, size.lines

def nibble(nibble_char):
    answers = {
        "0": " ", "1": "▖", "2": "▗", "3": "▄",
        "4": "▘", "5": "▌", "6": "▚", "7": "▙",
        "8": "▝", "9": "▞", "A": "▐", "B": "▟",
        "C": "▀", "D": "▛", "E": "▜", "F": "█"
    }
    nibble_char = nibble_char.upper()
    if nibble_char not in answers:
        raise ValueError(f"Invalid nibble character: {nibble_char}")
    return answers[nibble_char]

def renderpix(nibbles):
    for x in nibbles:
        print(nibble(nibbles[x]), end="")
    print()


__all__ = [
    'combinelambdas', 'colortext', 'colorget', 'loop', 'chaos',
    'define', 'call', 'dice', 'fill', 'throw', 'wait', 'waitms',
    'clear', 'modify', 'keypressed', 'timeunit', 'loadingbar',
    'main', 'ver', 'terminalsize', 'pi', 'e', "tau", "rand", "functions", "text"
]

