import database

class User():
    def __init__(self, user_id):
        user_id_exists = database.check_if_user_id_exists(user_id)
        if user_id_exists != True:
            raise RuntimeError('User ID not found in the database.')
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def get_user_name(self):
        return database.get_user_info(self.user_id)

    def get_user_info(self):
        return database.get_user_info(self.user_id)

    def get_admin_privilege(self):
        admin_privilege = database.get_admin_privilege(self.user_id)
        return admin_privilege

    def get_credit_balance(self):
        return database.get_credit_balance(self.user_id)

    def process_transaction(self, amount, transaction_initializedby_user_id=None, transaction_terminal_id=None):
        database.process_transaction(self.user_id, amount, transaction_initializedby_user_id, transaction_terminal_id)

class Card(User):
    def __init__(self, card_id):
        user_id = database.get_user_id_from_card_id(card_id)
        if user_id is None:
            raise RuntimeError('Card ID not found in the database.')
        self.card_id = card_id
        self.user_id = user_id

    def get_card_id(self):
        return self.card_id
