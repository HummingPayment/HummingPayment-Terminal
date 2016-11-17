import time
import wiringpi
from threading import Thread, Event, Lock
from gpiozero import RGBLED, Buzzer

from dothat import lcd
from interface_strings import *

lcd.set_display_mode()
lcd.set_contrast(20)

import locale
locale.setlocale(locale.LC_ALL, display_locale)

backlight = RGBLED(5, 6, 13)

buzzer = Buzzer(22)

message_lock = Lock()

terminal_enabled = 0
terminal_message = ""
terminal_amount = 0

lcd.create_animation(7, [[0b00000,0b10001,0b01010,0b00100,0b10001,0b01010,0b00100,0b00000],[0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000]], 1)

def _default():
    while 1:
        if message_lock.locked() == False:
            lcd.clear()
            if terminal_enabled != True:
                backlight.value = (1, 0.125, 0.125)
                lcd.write(terminal_locked_message)
                lcd.set_cursor_position(0,2)
                lcd.write(unlock)
            else:
                backlight.on()
                lcd.write(terminal_message)
                lcd.set_cursor_position(0,2)
                lcd.write(chr(7))
                if terminal_amount > 0:
                    lcd.write(refill)
                else:
                    lcd.write(amount)
                terminal_amount_string = locale.format('%.2f', abs(terminal_amount), True, True)
                lcd.set_cursor_position(lcd.COLS-len(terminal_amount_string)-1,2)
                lcd.write(terminal_amount_string)
                lcd.write(chr(7))
            lcd.update_animations()
            time.sleep(1)
        else:
            time.sleep(0.25)

t_default = Thread(target=_default, name="t_default", args=())
t_default.daemon = True
t_default.start()

def _message_output(code):
    if code == 1:
        buzzer.beep(on_time=0.25, off_time=0.25, n=1)
        backlight.value = (0.125, 1, 0.125)
    elif code >= 0:
        buzzer.beep(on_time=0.1, off_time=0.05, n=2)
        backlight.value = (1, 1, 0.125)
    else:
        buzzer.beep(on_time=0.1, off_time=0.05, n=4)
        backlight.value = (1, 0.125, 0.125)

def _message(code, credit_balance=None):
    message_lock.acquire()
    _message_output(code)
    lcd.clear()
    lcd.write(message_code[code])
    if credit_balance is not None:
        lcd.set_cursor_position(0,2)
        lcd.write(" ")
        lcd.write(balance)
        credit_balance_string = locale.format('%.2f', credit_balance, monetary=True)
        lcd.set_cursor_position(lcd.COLS-len(credit_balance_string)-1,2)
        lcd.write(credit_balance_string)
        lcd.write(" ")
    time.sleep(2.5)
    message_lock.release()

def clear():
    buzzer.off()
    lcd.clear()
    backlight.off()

def message(code, credit_balance=None):
    while message_lock.locked() == True:
        pass
    Thread(target=_message, name="t_message", args=(code, credit_balance)).start()
