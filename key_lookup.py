#####################################################################################################################
# SH                                                                                                                #
# This script acts as a command line program                                                                        #
# The script takes in a user-inputted key and returns all the key-part information about that key, which is derived #
# directly from the database in real-time.                                                                          #
# Last updated: July 18, 2022                                                                                       #
# Initial save                                                                                                      #
#####################################################################################################################

from tabulate import tabulate
import os
import pyodbc

os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'

input_key = ''
key_confirm = ''
key_list = []

# Create connection to SQL database
cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};'
                      'SERVER=' # redacted server
                      'DATABASE=' # redacted database
                      'trusted_connection=yes')
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin-1')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')
cnxn.setencoding(encoding='latin-1')


def run_sql():
    global input_key, key_list

    # Run SQL query
    crsr = cnxn.cursor()
    sql_statement = f"select rtrim(ltrim(glk_grp_part01)), rtrim(ltrim(glk_grp_part02)),rtrim(ltrim(glk_grp_part03))," \
                    f"rtrim(ltrim(glk_grp_part04)), rtrim(ltrim(glk_grp_part05)), rtrim(ltrim(glk_grp_part06))," \
                    f"rtrim(ltrim(glk_grp_part07)), rtrim(ltrim(glk_grp_part08)), rtrim(ltrim(glk_title_dl)) from " \
                    f"glk_key_mstr where glk_key = '{input_key}'"
    key_list = list(crsr.execute(sql_statement))


def get_key():
    global input_key
    input_key = ''

    while len(input_key) != 4 or not input_key.isnumeric():
        input_key = input('Give a key to access information about:\n')


def confirm_key():
    global key_confirm
    print('The key you have provided is', input_key)
    key_confirm = ''

    while not (key_confirm.strip().lower() == 'yes' or key_confirm.strip().lower() == 'no'):
        key_confirm = input('Is this correct? (Please reply with "yes" or "no")\n')

    return key_confirm


def affirmative_key():
    global input_key, key_confirm

    while not key_confirm.strip().lower() == 'yes':
        get_key()
        key_confirm = confirm_key()


print('\nThis tool takes a key that the user inputs and returns key-part information about it.\n')

another_key = input('Do you have a key to enter? (please enter yes or no)\n')

while another_key.strip().lower() == 'yes':
    while key_list.__len__() <= 0:
        get_key()
        confirm_key()
        affirmative_key()
        run_sql()

        key_table = tabulate(key_list,
                             headers=['Fund Group', 'Fund', 'Function', 'Activity', 'Department', 'Division', 'Bureau',
                                      'Section', 'Full description'], tablefmt='pretty')

        print(f"Information about key {input_key}:\n", key_table)
    key_list.clear()
    another_key = input('Do you have another key to enter? (please enter yes or no)\n')
