from collections.abc import Optional

import evdev
from evdev.events import InputEvent
import pyautogui


eventcode_hotkey_map = {
    257: ("ctrl", "shift", "alt", "/"),
    256: ("ctrl", "shift", "alt", "home"),
    258: ("ctrl", "shift", "alt", "end")
}


def detect_footpedal() -> Optional[evdev.InputDevice]:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    footpedal = None
    for device in devices:
        if 'VEC USB Footpedal' in device.name:
            footpedal = device
            break
    if footpedal is None:
        print("VEC Footpedal not detected!")
        return None
    else:
        return footpedal


def is_keydown(event: InputEvent) -> bool:
    return True if event.value == 1 else False


def listen_to_footpedal(footpedal: evdev.InputDevice):
    footpedal.grab()
    for event in footpedal.read_loop():
        if is_keydown(event):
            pyautogui.hotkey(*eventcode_hotkey_map[event.code])
    footpedal.close()

