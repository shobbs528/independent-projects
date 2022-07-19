##############################################################################################################
# SH                                                                                                         #
# This script connects to database, runs sql queries, and then outputs the results to an Excel workbook      #
# with sheets for each query that is run. Then, moves the workbook to a shared directory so others can view  #
# Last updated: May 26, 2022                                                                                 #
# Cleaned up code and added prompt at the end for successful transfer                                        #
##############################################################################################################

from string import ascii_uppercase as al
import getpass
import os
import pyodbc
import shutil
import smtplib
import xlsxwriter

os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'

# Gets the current user signed in to the computer (?)
# Requests the password for the user and puts the input into the pwd variable
# If nothing is entered or password is incorrect, script quits
user = getpass.getuser()
pwd = getpass.getpass("Password for %s:\n" % user)

# Attempting a login to the server to validate the password
# If the password is incorrect or empty, then the script will quit
try:
    server = smtplib.SMTP('') # redacted email server
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    server.quit()
except Exception as e:
    print('Invalid password:\n', e)
    quit()

write_log = []
worksheets = []
workbook = xlsxwriter.Workbook('GA_Stats.xlsx')
cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};'
                      'SERVER=' # redacted server
                      'DATABASE=' # redacted database
                      'trusted_connection=yes')
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin-1')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')
cnxn.setencoding(encoding='latin-1')
sql_dir = '' # redacted folder path
ws_row = 0
column = 0
which_sql = ''
alphabet = al

btub_worksheet = workbook.add_worksheet('BTUB')
inin_worksheet = workbook.add_worksheet('ININ')
je_worksheet = workbook.add_worksheet('JE')
pr_worksheet = workbook.add_worksheet('PR')

worksheets.append(btub_worksheet)
worksheets.append(inin_worksheet)
worksheets.append(je_worksheet)
worksheets.append(pr_worksheet)


def get_sql_stnt(stmt):
    return (stmt[stmt.rindex('_'):])[:-(stmt[::-1].index('.') + 1)][1:]


def sql_to_excel(sheet):
    global worksheets, write_log, ws_row, column

    ws_row = 0
    column = 0
    row_num = write_log.__len__() + 1
    col_num = alphabet[len(write_log[0])-1]

    match sheet:
        case 'BTUB':
            btub_worksheet.add_table(f'A1:{col_num}{row_num}',
                                     {'data': write_log,
                                      'columns': [{'header': 'User'},
                                                  {'header': '# of BTUBs processed'}]})
        case 'ININ':
            inin_worksheet.add_table(f'A1:{col_num}{row_num}',
                                     {'data': write_log,
                                      'columns': [{'header': 'User'},
                                                  {'header': '# of ININs reviewed'}]})
        case 'JE':
            je_worksheet.add_table(f'A1:{col_num}{row_num}',
                                   {'data': write_log,
                                    'columns': [{'header': 'User'},
                                                {'header': '# of JE sets processed'},
                                                {'header': '# of individual JEs processed'}]})
        case 'PR':
            pr_worksheet.add_table(f'A1:{col_num}{row_num}',
                                   {'data': write_log,
                                    'columns': [{'header': 'User'},
                                                {'header': '# of PRs reviewed'}]})
        case _:
            return


for sql in os.listdir(sql_dir):
    with open(sql_dir + '/' + sql, 'r') as files:
        sql_script = files.read()
        with cnxn.cursor() as cur:
            rows = cur.execute(sql_script)
            for row in rows:
                write_log.append(row)
    which_sql = get_sql_stnt(sql)
    sql_to_excel(which_sql)
    print(which_sql, 'put into Excel successfully')
    write_log.clear()

cnxn.close()
workbook.close()

shutil.copyfile('./GA_Stats.xlsx', "") # redacted destination file path
print('Excel copied to S drive successfully')
print('Peace out!')
