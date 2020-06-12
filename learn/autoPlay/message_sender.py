import os
import ctypes
import win32api
import time
import sys

sys.path.append("./")

from window_helper import WindowMgr

w = WindowMgr()
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def press_key(key):
    code = char_map[key]
    if not code:
        return

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    flags = 0x0008

    ii_.ki = KeyBdInput(0, code, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key):
    code = char_map[key]
    if not code:
        return

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    flags = 0x0008 | 0x0002

    ii_.ki = KeyBdInput(0, code, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def get_game_window():
    w.find_window_wildcard("Minecraft 1*")  # Game window is named 'Minecraft 1.13.1' for example.
    w.set_foreground()


def type_key(key, interval=0.05):
    press_key(key)
    time.sleep(interval)
    release_key(key)
    time.sleep(interval)


# Character map https://gist.github.com/tracend/912308
char_map = {
    'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16, 'i': 0x17, 'o': 0x18, 'p': 0x19,
    'a': 0x1E, 's': 0x1F, 'd': 0x20, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26, 'leftmouse': 0xff,
    'z': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30, 'n': 0x31, 'm': 0x32, 'left': 0xCB + 1024, 'right': 0xCD + 1024, 'up': 0xC8 + 1024, 'down': 0xD0 + 1024, 'leftalt': 0x38, '/': 0x35, 'leftshift': 0x2A, 'leftctrl': 0x1D, 'tab': 0x0F, 'capslock': 0x3A, '1': 0x02, '2': 0x03, '3': 0x04, '4': 0x05, '5': 0x06, '6': 0x07, '7': 0x08, '8': 0x09, '9': 0x0a, '0': 0x0b, 'esc': 0x01, '`': 0x29, 'f1': 0x3b, 'f2': 0x3c, 'f3': 0x3d, 'f4': 0x3e, 'f5': 0x3f, 'f6': 0x40, 'f7': 0x41, 'f8': 0x42, 'f9': 0x43, 'f10': 0x44}

# Sending the message using the character map
# get_game_window()
# press_key(char_map['t'])  # t - opens chat
# release_key(char_map['t'])
#
# press_key(char_map['h']);
# release_key(char_map['h']);  # h
# press_key(char_map['e']);
# release_key(char_map['e']);  # e
# press_key(char_map['l']);
# release_key(char_map['l']);  # l
# press_key(char_map['l']);
# release_key(char_map['l']);  # l
# press_key(char_map['o']);
# release_key(char_map['o']);  # o

# for i in range(3,-1,-1):
#     time.sleep(1)
#     print(i)

# numlock 为 + 1024
# code = 0x3a
# for key in char_map:
#     code = char_map[key]
#     press_key(code)
#     time.sleep(0.05)
#     release_key(code)
#     time.sleep(0.05)

# press_key(code)
# time.sleep(0.05)
# release_key(code)
# time.sleep(0.05)

# press_key(code)
# time.sleep(0.05)
# release_key(code)
# code = 0x39
# press_key(code)
# time.sleep(0.05)
# release_key(code)

# press_key(0x1C);
# release_key(0x1C);  # Submit it (0x1C is ENTER key -> possible char_map extension? ;))
