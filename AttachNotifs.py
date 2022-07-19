# SH
# Send notification when link for document/attachment updated
# Based on SQL query, exported to CSV
# Will only send notifications
# Last updated: February 24, 2022
# Converted previously plaintext email to HTML email

import csv
import ctypes
import getpass
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyodbc
from dateutil import parser
from tabulate import tabulate

# setting most variables
log = []
doc_id = 0
table = ""
column = ""
oldValue = ""
newValue = ""
changedWhen = ""
changedWho = ""
smtp_server = '' # redacted server
senderEmail = 'SKHobson@SolanoCounty.com'
pwd = ''
recipientEmails = ['SKHobson@SolanoCounty.com'] # redacted other recipients
textFilePath = '' # redacted file path
recordCount = 0

# Get the date when the script was last run from text file (as string)
with open(textFilePath, 'r') as file:
    fileDate = file.read().rstrip()

fileDate = datetime.strptime(fileDate, '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y %H:%M:%S')

# Convert date string to actual date and output in pop-up box
lastRunDate = parser.parse(fileDate)
ctypes.windll.user32.MessageBoxW(0, fileDate, "Last time script was run", 1)

user = getpass.getuser()

try:
    pwd = getpass.getpass("Password for %s:\n" % user)
except Exception as e:
    print('Error occurred: ', e)
    quit()

# Create connection to SQL database
cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};'
                      'SERVER=' # redacted server
                      'DATABASE=' # redacted database
                      'trusted_connection=yes')
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin-1')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')
cnxn.setencoding(encoding='latin-1')

# Run SQL query
crsr = cnxn.cursor()
statement = f"select imdata.doc_id, imstr.table_name, imdtl.column_name, imlog.old_value, imlog.new_value, " \
            f"imlog.log_when, imlog.log_who from IM_INDEX_DATA_x imlog, im_index_data imdata, im_index_dtl imdtl, " \
            f"im_index_mstr imstr, oh_bir_mstr bir where imlog.rec_unique_key = imdata.unique_key and imdata.index_id" \
            f" = imdtl.index_id and imdata.field_id = imdtl.field_id and imdata.index_id = imstr.index_id and " \
            f"imdtl.index_id = imstr.index_id	and bir.oh_ref = imlog.new_value and imlog.event_id = 'U' and oh_ref " \
            f"in (select oh_ref from ohb_batch_dtl where ohb_sec_cd is not null and ohb_sec_cd <> '') and " \
            f"imlog.log_when > '{datetime.strptime(fileDate, '%B %d, %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')}' " \
            f"order by log_when desc,doc_id "
rows = crsr.execute(statement)

# Write output of SQL query to CSV file
with open('', 'w', newline='') as csvfile: # redacted file path
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')

    for row in rows:
        writer.writerow(row)
        recordCount += 1

if recordCount < 1:
    text = """
Hello,
Since the last time this script was run on """ + fileDate + """, there have been no updates to links for documents.
{table}"""
    html = """
<html><body>
<p>Hello,<br>Since the last time this script was run on """ + fileDate + """, there have been no updates 
to links for documents.</p> 
<p>Good day,</p>
<p>SH</p> </body></html> """
    message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html, 'html')])
    message['Subject'] = 'No links for documents have been updated'
    message['From'] = senderEmail
    message['To'] = ", ".join(recipientEmails)
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    server.login(senderEmail, pwd)
    server.sendmail(senderEmail, recipientEmails, message.as_string())
    server.quit()
else:
    # Open CSV file in read-mode and read to "data" variable
    fi = open('', 'r') # redacted file path
    data = fi.read()
    fi.close()

    # Write data from first CSV file to new CSV file to get rid of null bytes (\x00)
    fo = open('', 'w') # redacted file path
    fo.write(data.replace('\x00', ''))
    fo.close()

    # Get rid of first CSV file as it is not needed anymore (first checks to make sure it's there and exists as a file)
    deleteFile = '' # redacted file path
    if os.path.exists(deleteFile) and os.path.isfile(deleteFile):
        os.remove(deleteFile)

    text = """
Hello,
Since the last time this script was run on """ + fileDate + """, the following links for documents have been updated:"""
    html = """
<html><body>
<p>Hello,<br>Since the last time this script was run on """ + fileDate + """, the following links for 
documents have been updated:</p> 
{table} 
<p>Good day,</p>
<p>SH</p> 
</body></html> """

    with open('') as table_file: # redacted file path
        reader = csv.reader(table_file)
        data = list(reader)

        text = text.format(table=tabulate(data, headers=['Doc ID', 'Table', 'Column', 'Old value', 'New value',
                                                         'Changed when', 'Changed by'], tablefmt='pretty',
                                          numalign='center', stralign='center'))
        html = html.format(table=tabulate(data, headers=['Doc ID', 'Table', 'Column', 'Old value', 'New value',
                                                         'Changed when', 'Changed by'], tablefmt='html',
                                          numalign='center', stralign='center'))

    message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html, 'html')])
    message['Subject'] = 'Some link(s) for document(s) have been updated'
    message['From'] = senderEmail
    message['To'] = ", ".join(recipientEmails)
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    server.login(senderEmail, pwd)
    server.sendmail(senderEmail, recipientEmails, message.as_string())
    server.quit()

# Get the current time and convert to readable format
now = datetime.now()
now = now.strftime('%Y-%m-%d %H:%M:%S')

# Update the text file to reflect the last time when this script was run
with open(textFilePath, "w") as f:
    f.write(now)
