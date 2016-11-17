import database

class Terminal():
    def __init__(self, terminal_id):
        terminal_id_exists = database.check_if_terminal_id_exists(terminal_id)
        if terminal_id_exists != True:
            raise RuntimeError('Terminal ID not found in the database.')
        self.terminal_id = terminal_id

    def get_terminal_id(self):
        return self.terminal_id

    def get_terminal_name(self):
        return database.get_terminal_name(self.terminal_id)

    def check_terminal_enabled(self):
        return database.check_terminal_enabled(self.terminal_id)

    def update_terminal_enabled(self, terminal_enabled):
        database.update_terminal_enabled(self.terminal_id, terminal_enabled)

    def enable_terminal(self):
        self.update_terminal_enabled(1)

    def disable_terminal(self):
        self.update_terminal_enabled(0)

    def get_terminal_amount(self):
        return database.get_terminal_amount(self.terminal_id)

    def get_terminal_message(self):
        return database.get_terminal_message(self.terminal_id)


class TerminalWithHardwareidentifier(Terminal):
    def __init__(self, terminal_hardwareidentifier):
        terminal_id = database.get_terminal_id_from_terminal_hardwareidentifier(terminal_hardwareidentifier)
        if terminal_id is None:
            raise RuntimeError('Hardware Identifier not found in the database.')
        self.terminal_hardwareidentifier = terminal_hardwareidentifier
        self.terminal_id = terminal_id

    def get_terminal_hardwareidentifier(self):
        return self.terminal_hardwareidentifier
