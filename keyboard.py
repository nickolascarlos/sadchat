from pynput import keyboard
from pynput.keyboard import Key

from commands import *
import buffer

def on_press(key):
    try:
        buffer.buffer += key.char
    except AttributeError as e:
        if key == Key.space:
            buffer.buffer += " "
        elif key == Key.backspace:
            buffer.buffer = buffer.buffer[:-1] # Apaga
        elif key == Key.enter:
            # Verifica se o que está no buffer se trata de um comando
            # Se for, o processa
            # Do contrário, assume-se ser uma mensagem
            if buffer.buffer.startswith("!"):
                # processa_commando(buffer.buffer)
            else:
                # envia_mensagem(buffer.buffer)
                pass
            # E então limpa o buffer
            buffer.clear_buffer()

def on_release(key):
    buffer.process_buffer() # 'Corrige' o conteúdo do buffer (acentuação)
    # if (key == Key.shift):
    #     print(buffer.buffer)
    ###

def start_keyboard_listening():
    # Registrando e iniciando o Listener para o teclado
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)

    listener.start()