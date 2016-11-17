import uuid
import time
import sys
from threading import Thread

import interface

try:
    from user import Card
    from terminal import TerminalWithHardwareidentifier
except ConnectionRefusedError:
    interface.message(-11)
    raise ConnectionRefusedError

from reader import Reader

reader = Reader()
terminal = TerminalWithHardwareidentifier(str(uuid.getnode()))
terminal_id = terminal.get_terminal_id()
terminal_enabled = terminal.check_terminal_enabled()
terminal_amount = terminal.get_terminal_amount()
terminal_message = terminal.get_terminal_message()

def _update_terminal_config():
    while 1:
        try:
            global terminal_enabled, terminal_amount, terminal_message
            terminal_enabled = terminal.check_terminal_enabled()
            terminal_amount = terminal.get_terminal_amount()
            terminal_message = terminal.get_terminal_message()

            interface.terminal_enabled = terminal_enabled
            interface.terminal_amount = terminal_amount
            interface.terminal_message = terminal_message
        except (KeyboardInterrupt, SystemExit):
            break
        except:
            pass
        time.sleep(5)

t_update_terminal_config = Thread(target=_update_terminal_config, name="t_update_terminal_config", args=())
t_update_terminal_config.daemon = True
t_update_terminal_config.start()

def main():
    while 1:
        try:
            card_id = reader.get_card_id()
            if card_id is not None:
                try:
                    current_user = Card(card_id)
                except RuntimeError:
                    interface.message(-21)
                    time.sleep(2)
                    continue
                if terminal_enabled == 1:
                    credit_balance = current_user.get_credit_balance()
                    if credit_balance + terminal_amount >= 0:
                        current_user.process_transaction(terminal_amount, transaction_terminal_id=terminal_id)
                        credit_balance = current_user.get_credit_balance()
                        interface.message(1, credit_balance)
                    else:
                        interface.message(-22, credit_balance)
                else:
                    if current_user.get_admin_privilege() >= 1:
                        terminal.update_terminal_enabled(1)
                        interface.message(10)
                        time.sleep(5)
                    else:
                        interface.message(-23)
                        time.sleep(0.5)
            time.sleep(0.5)
        except (KeyboardInterrupt, SystemExit):
            interface.clear()
            sys.exit()
        except:
            interface.message(-1)
        time.sleep(5)

main()
