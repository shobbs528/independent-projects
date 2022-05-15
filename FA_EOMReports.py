import csv
import os
import smtplib
import ssl
import pyodbc
import getpass
from datetime import datetime

fund_source_log = []
depreciation_log = []
port = 587
smtp_server = 'hybrid.solanocounty.com'
sender_email = 'SKHobson@SolanoCounty.com'
pwd = ''
recipient_emails = ['SKHobson@SolanoCounty.com']
message = ''
parent_file_path = '//solano/root/auditor/GENACCT/FixedAssets/SH/SQL'
now = datetime.now().date().strftime('%Y-%m-%d')

# Create connection to SQL database
cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};'
                      'SERVER=CACOSP04\onesolution;'
                      'DATABASE=production_finance;'
                      'trusted_connection=yes')
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin-1')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')
cnxn.setencoding(encoding='latin-1')
assocCrsr = cnxn.cursor()
ac_depreciation_record_count = depreciation_record_count = ac_fund_source_record_count = fund_source_record_count = 0

depr_crsr = cnxn.cursor()
depreciation_statement = f"select depr.faid, count(depr.faid),	stat from fa_depr depr, fa_idnt idnt where" \
                         f" idnt.faid = depr.faid group by stat, depr.faid having count(depr.faid) > 1 order by stat"
fndsrc_crsr = cnxn.cursor()
fund_source_statement = f"select fnd.faid, count(fnd.faid), idnt.stat from fa_fndsrc fnd, fa_idnt idnt where" \
                        f" idnt.faid = fnd.faid and idnt.faid not in ('1018481','B170-050-04G') and stat <> 'DI'" \
                        f" group by idnt.stat, fnd.faid having count(fnd.faid) > 1 order by idnt.stat"


def check_count(check_num, check_str='AC'):
    global fund_source_log, depreciation_log, ac_depreciation_record_count, depreciation_record_count, \
        ac_fund_source_record_count, fund_source_record_count
    if check_num == 0:
        for i in range(len(fund_source_log)):
            if fund_source_log[i][2].lower() == check_str.lower():
                ac_fund_source_record_count += 1
    elif check_num == 1:
        for i in range(len(depreciation_log)):
            if depreciation_log[i][2].lower() == check_str.lower():
                ac_depreciation_record_count += 1
    elif check_num == 2:
        fund_source_record_count = fund_source_log.__len__()
    else:
        depreciation_record_count = depreciation_log.__len__()


def execute_sql(sql_statement, crsr):
    rows = crsr.execute(sql_statement)
    return rows


def conv_csv_list(table, rows_name, log_name):
    global parent_file_path
    new_file = parent_file_path + '/' + table + 'Log.csv'

    with open(new_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='')

        for row in rows_name:
            writer.writerow(row)

    fi = open(new_file, 'r')
    data = fi.read()
    fi.close()

    file = new_file[:-4] + 'New.csv'

    fo = open(file, 'w')
    fo.write(data.replace('\x00', ''))
    fo.close()

    if os.path.exists(new_file) and os.path.isfile(new_file):
        os.remove(new_file)

    with open(file, 'rt', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            for col in range(len(row)):
                row[col] = row[col].strip()
            log_name.append(row)

    return log_name


def parse_logs(tab_name, log_name):
    global message
    message = message + '\n\nThe following are FAIDs that have a duplicate on the ' + tab_name + ' tab:\n'

    for i in range(len(log_name)):
        for j in range(len(log_name[i])):
            faid = log_name[i][0]
            count = log_name[i][1]
            asset_status = log_name[i][2]

        if asset_status.lower() != 'ac'.lower():
            break
        else:
            message = message + '\nThe FAID ' + faid + ' with status ' + asset_status + ' has ' + count + ' duplicate records.\n'


fund_source_rows = execute_sql(fund_source_statement, fndsrc_crsr)
fund_source_log = conv_csv_list('FundSource', fund_source_rows, fund_source_log)

depreciation_rows = execute_sql(depreciation_statement, depr_crsr)
depreciation_log = conv_csv_list('Depreciation', depreciation_rows, depreciation_log)

func_count = 4
for i in range(func_count):
    check_count(i)

message = """Subject: Depreciation and Fund Source Reports
Hello,
As of today, """ + now + """, here is the status of duplicates for the Depreciation and Fund Source tabs:"""

if ac_fund_source_record_count > 0 and ac_depreciation_record_count > 0:
    parse_logs('Depreciation', depreciation_log)
    parse_logs('Fund Source', fund_source_log)
elif ac_depreciation_record_count > 0 and ac_fund_source_record_count < 1:
    parse_logs('Depreciation', depreciation_log)
elif ac_depreciation_record_count < 1 and ac_depreciation_record_count > 0:
    parse_logs('Fund Source', fund_source_log)
else:
    message = message + '\n\nThere are no duplicates to report for FAIDs with a status of AC.\n\nHowever, if you would like to view the logs for non-AC FAIDs, please visit the folder: S:\\GENACCT\\FixedAssets\\SH\\SQL and view the two .csv files: DepreciationLogNew.csv and FundSourceLogNew.csv.'

message = message + '\nGood day.'

user = getpass.getuser()

try:
    pwd = getpass.getpass("Password for %s:\n" % user)
except Exception as e:
    print('Error occurred: ', e)
    quit()

context = ssl._create_unverified_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.login(sender_email, pwd)
    server.sendmail(sender_email, recipient_emails, message)
