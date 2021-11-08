import sys
import strings

if not sys.platform.startswith('linux'):
        print(strings.please_change_to_linux)
        sys.exit(-1)

import keyboard
import gui
import timing
import communication


if __name__ == '__main__':
    keyboard.start_keyboard_listening()