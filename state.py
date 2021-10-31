import buffer as _buffer_
from datetime import datetime
import gui


# Arquivo para guardar o estado da aplicação

state = {
    "messages": [],
    "buffer": "",
    "cursor_position": 0,
    "time": "[??:??:??]",
    "username": "",
    "status": "offline",
    "secret": "",
    "main_alert": "Set your user using !setuser"
}

def get(key):
    global state
    return state[key]

def update(key, new_value):
    global state
    state[key] = new_value
    gui.rerender()

def add_message(sender, new_message):
    if (not new_message): return
    now = datetime.now()
    update("messages", [*get("messages"), ["[%02d:%02d:%02d]" % (now.hour, now.minute, now.second), sender, new_message]])

def update_buffer():
    update("buffer", _buffer_.get_buffer())

def set_cursor_position(new):
    update("cursor_position", new)

def inc_cursor_position(q = 1):
    if get("cursor_position") + q <= len(get("buffer")):
        update("cursor_position", get("cursor_position") + q)

def dec_cursor_position(q = 1):
    if get("cursor_position") > 0:
        update("cursor_position", get("cursor_position") - q)

def zero_cursor_position():
    update("cursor_position", 0)

def set_time(hour, minute, second):
    # Caso especial: não rerenderizará toda a interface, apenas a parte relacionada ao horário
    global state

    # update("time", "[%02d:%02d:%02d]" % (hour, minute, second))
    state["time"] = "[%02d:%02d:%02d]" % (hour, minute, second)
    gui.draw_hour()

def set_username(new):
    update("username", new)

def get_username():
    return get("username")

