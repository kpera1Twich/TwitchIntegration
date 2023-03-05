"""Handles keyboard commands

Code taken from https://www.dougdoug.com/twitchplays-keycodes-py-3-9-x
"""

import ctypes
from asyncio import sleep

import pynput

from .enums import Keys, MouseButtons


async def hold_key(hex_key_value: Keys | MouseButtons):
    """Holds down a key

    :param hex_key_value: The hex code of the key
    :type hex_key_value: Keys | MouseButtons
    :return:
    :rtype:
    """
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(
        0,
        hex_key_value.value,
        0x0008,
        0,
        ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p),
    )
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


async def release_key(hex_key_value: Keys | MouseButtons):
    """Releases a key

    :param hex_key_value: The hex code of the key to relase
    :type hex_key_value: Keys | MouseButtons
    :return:
    :rtype:
    """
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(
        0,
        hex_key_value.value,
        0x0008 | 0x0002,
        0,
        ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p),
    )
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


async def hold_and_release_key(hex_key_value: Keys | MouseButtons, seconds: float):
    """Holds down a key for a certain amount of time

    :param hex_key_value:
    :type hex_key_value:
    :param seconds:
    :type seconds:
    :return:
    :rtype:
    """
    await hold_key(hex_key_value)
    await sleep(seconds)
    await release_key(hex_key_value)
