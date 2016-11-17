import atexit
import mysql.connector

from database_config import *

try:
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database=DATABASE_NAME, buffered=False)
    cnx.autocommit = True
except:
    raise ConnectionRefusedError

@atexit.register
def _atexit():
    cnx.close()

#NAMING SCHEME
#get: returns non-boolean
#check: returns boolean
#set and other verbs: write to database

def get_user_id_from_card_id(card_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+USER_ID_COL+' FROM '+USERS_TABLE_NAME+' WHERE '+CARD_ID_COL+' = %(CARD_ID)s', {"CARD_ID": card_id})
    user_id = cursor.fetchone()
    cursor.close()
    if user_id is None:
        return None
    return user_id[0]

def get_user_id_from_user_name(user_name):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+USER_ID_COL+' FROM '+USERS_TABLE_NAME+' WHERE '+USER_NAME_COL+' = %(USER_NAME)s', {"USER_NAME": user_name})
    user_id = cursor.fetchone()
    cursor.close()
    if user_id is None:
        return None
    return user_id[0]

def check_if_user_id_exists(user_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT EXISTS(SELECT * FROM '+USERS_TABLE_NAME+' WHERE '+USER_ID_COL+' = %(USER_ID)s LIMIT 1)', {"USER_ID": user_id})
    user_id_exists = cursor.fetchone()
    cursor.close()
    if user_id_exists[0] == True:
        return True
    else:
        return False

def log_transaction(transaction_user_id, transaction_amount=None, transaction_initializedby_user_id=None, transaction_terminal_id=None):
    cursor = cnx.cursor()
    cursor.execute('INSERT INTO '+TRANSACTION_LOG_TABLE_NAME+' ('+TRANSACTION_USER_ID_COL+', '+TRANSACTION_AMOUNT_COL+', '+TRANSACTION_INITIALIZEDBY_USER_ID_COL+', '+TRANSACTION_TERMINAL_ID_COL+') VALUES (%(TRANSACTION_USER_ID)s, %(TRANSACTION_AMOUNT)s, %(TRANSACTION_INITIALIZEDBY_USER_ID)s, %(TRANSACTION_TERMINAL_ID)s)', {"TRANSACTION_USER_ID": transaction_user_id, "TRANSACTION_AMOUNT": transaction_amount, "TRANSACTION_INITIALIZEDBY_USER_ID": transaction_initializedby_user_id, "TRANSACTION_TERMINAL_ID": transaction_terminal_id})
    cursor.close()
    return

def get_admin_privilege(user_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+ADMIN_PRIVILEGE_COL+' FROM '+USERS_TABLE_NAME+' WHERE '+USER_ID_COL+' = %(USER_ID)s', {"USER_ID": user_id})
    user = cursor.fetchone()
    cursor.close()
    if user is None:
        return
    admin_privilege = user[0]
    return admin_privilege

def get_credit_balance(user_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+CREDIT_BALANCE_COL+' FROM '+USERS_TABLE_NAME+' WHERE '+USER_ID_COL+' = %(USER_ID)s', {"USER_ID": user_id})
    credit_balance = cursor.fetchone()
    cursor.close()
    return credit_balance[0]

def process_transaction(user_id, amount, transaction_initializedby_user_id=None, transaction_terminal_id=None):
    cursor = cnx.cursor()
    cursor.execute('UPDATE '+USERS_TABLE_NAME+' SET '+CREDIT_BALANCE_COL+' = '+CREDIT_BALANCE_COL+' + %(AMOUNT)s WHERE '+USER_ID_COL+' = %(USER_ID)s', {"USER_ID": user_id, "AMOUNT": amount})
    cursor.close()
    if amount != 0:
        log_transaction(user_id, amount, transaction_initializedby_user_id, transaction_terminal_id)
    return

def get_user_info(user_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM '+USERS_TABLE_NAME+' WHERE '+USER_ID_COL+' = %(USER_ID)s', {"USER_ID": user_id})
    user_data = cursor.fetchone()
    cursor.close()
    return user_data

def get_user_info(user_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+USER_NAME_COL+' FROM '+USERS_TABLE_NAME+' WHERE '+USER_ID_COL+' = %(USER_ID)s', {"USER_ID": user_id})
    user_name = cursor.fetchone()
    cursor.close()
    return user_name[0]

def get_terminal_id_from_terminal_hardwareidentifier(terminal_hardwareidentifier):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+TERMINAL_ID_COL+' FROM '+TERMINALS_TABLE_NAME+' WHERE '+TERMINAL_HARDWAREIDENTIFIER_COL+' = %(TERMINAL_HARDWAREIDENTIFIER)s', {"TERMINAL_HARDWAREIDENTIFIER": terminal_hardwareidentifier})
    terminal_id = cursor.fetchone()
    if terminal_id is None:
        return None
    cursor.close()
    return terminal_id[0]

def check_if_terminal_id_exists(terminal_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT EXISTS(SELECT * FROM '+TERMINALS_TABLE_NAME+' WHERE '+TERMINAL_ID_COL+' = %(TERMINAL_ID)s LIMIT 1)', {"TERMINAL_ID": terminal_id})
    terminal_id_exists = cursor.fetchone()
    cursor.close()
    if terminal_id_exists[0] == True:
        return True
    else:
        return False

def get_terminal_config(terminal_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM '+TERMINALS_TABLE_NAME+' WHERE '+TERMINAL_ID_COL+' = %(TERMINAL_ID)s', {"TERMINAL_ID": terminal_id})
    terminal_config = cursor.fetchone()
    cursor.close()
    return terminal_config

def get_terminal_name(terminal_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+TERMINAL_NAME_COL+' FROM '+TERMINALS_TABLE_NAME+' WHERE '+TERMINAL_ID_COL+' = %(TERMINAL_ID)s', {"TERMINAL_ID": terminal_id})
    terminal_name = cursor.fetchone()
    cursor.close()
    return terminal_name[0]

def check_terminal_enabled(terminal_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+TERMINAL_ENABLED_COL+' FROM '+TERMINALS_TABLE_NAME+' WHERE '+TERMINAL_ID_COL+' = %(TERMINAL_ID)s', {"TERMINAL_ID": terminal_id})
    terminal_enabled = cursor.fetchone()
    cursor.close()
    return terminal_enabled[0]

def update_terminal_enabled(terminal_id, terminal_enabled):
    cursor = cnx.cursor()
    cursor.execute('UPDATE '+TERMINALS_TABLE_NAME+' SET '+TERMINAL_ENABLED_COL+' = %(TERMINAL_ENABLED)s WHERE '+TERMINAL_ID_COL+' = %(TERMINAL_ID)s', {"TERMINAL_ID": terminal_id, "TERMINAL_ENABLED": terminal_enabled})
    cursor.close()
    return

def get_terminal_amount(terminal_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+TERMINAL_AMOUNT_COL+' FROM '+TERMINALS_TABLE_NAME+' WHERE '+TERMINAL_ID_COL+' = %(TERMINAL_ID)s', {"TERMINAL_ID": terminal_id})
    terminal_amount = cursor.fetchone()
    cursor.close()
    return terminal_amount[0]

def get_terminal_message(terminal_id):
    cursor = cnx.cursor()
    cursor.execute('SELECT '+TERMINAL_MESSAGE_COL+' FROM '+TERMINALS_TABLE_NAME+' WHERE '+TERMINAL_ID_COL+' = %(TERMINAL_ID)s', {"TERMINAL_ID": terminal_id})
    terminal_message = cursor.fetchone()
    cursor.close()
    return terminal_message[0]
