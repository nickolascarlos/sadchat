import sys
import signal
import curses

import strings
import state


if not sys.platform.startswith('linux'):
        print(strings.please_change_to_linux)
        sys.exit(-1)

import keyboard
import gui
import timing
import communication


def hdlr(a, b):
        state.set_threads_exit_flag()
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        sys.exit(0)


signal.signal(signal.SIGINT, hdlr)


if __name__ == '__main__':
    keyboard.start_keyboard_listening()