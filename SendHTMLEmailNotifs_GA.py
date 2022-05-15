# SH
# This script uses two SQL queries and organizes the information into CSV files and list of lists variables, sorts the
# information, then sends emails to the reviewers with all the invoices that are pending upon them and some quick
# information about each invoice - Invoice number, Vendor ID, when it arrived at the reviewer's queue, and how many
# business days it has been there.
# Last updated: March 24, 2022
# Added the security code per invoice, which helps the GA reviewers with organization and allows them to prioritize
# which invoices to review first

import csv
import smtplib
import pyodbc
import time
import getpass
import numpy as np
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate
from operator import itemgetter

# Setting most variables
invoice_log = []
count_log = []
per_user_log = []
tab_log = []
smtp_server = 'hybrid.solanocounty.com:587'
recipient_emails = ['SKHobson@SolanoCounty.com']
sender_email = 'SKHobson@SolanoCounty.com'
text = ''
now = datetime.now().date().strftime('%B %d, %Y')
parent_folder = '//solano/root/Auditor/USERS/SKHobson/Desktop/ININFiles/GA'

# Create connection to SQL database
cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};'
                      'SERVER=CACOSP04\onesolution;'
                      'DATABASE=production_finance;'
                      'trusted_connection=yes')
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin-1')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')
cnxn.setencoding(encoding='latin-1')

# Setting the cursor and SQL statement for the query that brings back the actual invoices per user
invoice_crsr = cnxn.cursor()
invoice_statement = f"select wf_us_id, bir.oh_ref, bir.oh_pe_id, min(wf_when_in), DATEDIFF(DAY,min(wf_when_in)," \
                    f"GETDATE()), inst.wf_key, batch.ohb_sec_cd from wf_history hist inner join (select wf_key, " \
                    f"max(wf_change_count) as maxCount, max(wf_life_count) as maxLife from wf_history group by " \
                    f"wf_key) as histb on hist.wf_key = histb.wf_key and hist.wf_change_count = histb.maxCount and " \
                    f"hist.wf_life_count = histb.maxLife, us_usno_mstr us, oh_bir_mstr bir, wf_instance inst, " \
                    f"ohb_batch_dtl batch, ohh_batch_mstr ohh where hist.wf_key = bir.unique_key and hist.wf_us_id = " \
                    f"us.us_id and hist.wf_key = inst.wf_key and bir.oh_ref = batch.oh_ref and ohh.oh_batch_id = " \
                    f"batch.oh_batch_id and wf_activity_id like 'A19_0%' and bir.oh_post_state <> 'DS' and " \
                    f"ohh.oh_post_state <> 'DS' and inst.wf_ext_state not in ('ORIG','REJC','APRV','DEPT','NRWH') and" \
                    f" hist.wf_status not in ('F','Y') and batch.ohb_sec_cd <> '' and batch.ohb_sec_cd is not null " \
                    f"and ohh_batch_type = 'IN' group by hist.wf_key, wf_us_id, us_name, bir.oh_ref, bir.oh_pe_id, " \
                    f"us_email, inst.wf_key, batch.ohb_sec_cd order by 1, 5 desc, 7;"

# Setting the cursor and SQL statement for the query that brings back the number of invoices pending per user plus the
# info for the user (name, username, email)
count_crsr = cnxn.cursor()
count_statement = f"select wf_us_id, us_email, us_name,count(wf_us_id) from wf_history, us_usno_mstr where wf_us_id " \
                  f"= us_id and wf_model_id = 'AP_RVW' and wf_version = '4' and wf_status = 'P' and us_loc_cd = " \
                  f"'AUDITOR' and wf_activity_id like 'A19_0%' group by wf_us_id,us_name,us_email order by wf_us_id"


# Function that executes the sql query, writes it to a csv, then writes to a list of lists as a "log"
# Takes in: the crsr for the SQL statement, the SQL statement itself, the file name to complete the file path, and the
# log to write to
# Uses global parent folder string
# Executes the SQL statement (via the cursor)
# Writes the output to a csv file
# Reads the output back into a list of lists with the whitespaces stripped out
# Returns the list of lists
def sql_to_log(crsr, sql_statement, file_name, log):
    global parent_folder

    rows = crsr.execute(sql_statement)
    file_name = parent_folder + file_name + '.csv'

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)

    with open(file_name, 'rt', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            for col in range(len(row)):
                row[col] = row[col].strip()
            log.append(row)
    return log


# Gets the current user signed in to the computer (?)
# Requests the password for the user and puts the input into the pwd variable
# If nothing is entered or password is incorrect, script quits
user = getpass.getuser()
pwd = getpass.getpass("Password for %s:\n" % user)

# Attempting a login to the server to validate the password
# If the password is incorrect or empty, then the script will quit
try:
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    server.login(sender_email, pwd)
    server.quit()
except Exception as e:
    print('Invalid password:\n', e)
    quit()

# Calling the above sql_to_log function, giving the following as parameters:
# invoice statement cursor
# invoice sql statement
# 'ININ' as the file name addition
# the invoice log to be populated
invoice_log = sql_to_log(invoice_crsr, invoice_statement, 'ININ', invoice_log)
# Calling the above sql_to_log function, giving the following as parameters:
# invoice count statement cursor
# invoice count sql statement
# 'Count' as the file name addition
# the count log to be populated
count_log = sql_to_log(count_crsr, count_statement, 'Count', count_log)

# For-loop that goes through the rows of the count log, then through each column of each row
for i in range(len(count_log)):
    for j in range(len(count_log[i])):

        # Populate the following variables given data from the count log
        username = count_log[i][0]
        email = count_log[i][1]
        # Splitting the name variable into 3 parts - first, middle (with a wildcard), and last
        first, *middle, last = count_log[i][2].split()
        # Removes the middle name and appends a normally-capitalized first and last name for the email greeting
        full_name = first.capitalize() + ' ' + last.capitalize()
        num_aprvs = count_log[i][3]

    # Sets the plain text for the email body to be sent out with variables concatenated in their appropriate spots
    text = """
Hello """ + full_name + """,

As of this email (""" + now + """), there are currently """ + num_aprvs + """ invoice(s) pending your review in 
APOHININ. See below for a list of invoices that are pending, when they arrived at your queue, how many business 
days they have been in your queue, and the security code associated with the invoice: 
{table}
Good day,
SH"""

    # The HTML version of the plain text email, with appropriate breaks, formatting, etc. as well as variables
    # concatenated in their appropriate spots
    html = """
<html><body>
<p>Hello """ + full_name + """,<br></p>
<p>As of this email (""" + now + """), there are currently """ + num_aprvs + """ invoice(s) pending your review in 
APOHININ. See below for a list of invoices that are pending, when they arrived at your queue, how many business 
days they have been in your queue, and the security code associated with the invoice:</p>
{table} 
<p>Good day,</p>
<p>SH</p>
</body></html> """

    # For-loop through invoice log that uses two iterator variables (x, y)
    # x is used as an index for later data-grabbing
    # y is just a general iterator
    for x, y in enumerate(invoice_log):
        if username in y:
            invoice_index = x
            # Grabbing the date from the SQL output, parsing it, then reformatting it into a friendlier format
            invoice_date = datetime.strptime(invoice_log[invoice_index][3], '%Y-%m-%d %H:%M:%S').date().strftime(
                '%B %d, %Y')

            # Calculating the number of business days between the day the script runs and the day it arrived at the
            # reviewer's queue. Date also taken from SQL output and parsed, but reformatted differently
            bus_days = np.busday_count(datetime.strptime(invoice_log[invoice_index][3], '%Y-%m-%d %H:%M:%S')
                                       .strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d'))

            # Putting invoice details into a temp list...
            per_user_log.append(invoice_log[invoice_index][1])
            per_user_log.append(' | ' + invoice_log[invoice_index][2] + ' | ')
            per_user_log.append(invoice_date)
            per_user_log.append(bus_days)
            per_user_log.append(invoice_log[invoice_index][6])

            # ...to append here
            tab_log.append(per_user_log[:])
            # Clearing the list to get ready for the next iteration
            per_user_log.clear()

    # This sorts the tab log (invoices per reviewer) by the third column, which is the date that the invoice arrived at
    # the reviewer's queue.
    # This may be unnecessary, but I'm leaving it here until definitively deemed unnecessary.
    sorted(tab_log, key=itemgetter(2))

    # Takes the variable that's storing the plain text email body and formats the table that is instantiated within
    # the variable. This is for when the email is viewed in a plaintext-only email viewer and uses the formatting
    # "pretty," center aligned for strings and numbers, and contains headers:
    # Invoice number
    # Vendor ID
    # Date arrived at the reviewer's queue
    # Number of business days at the reviewer's queue
    text = text.format(table=tabulate(tab_log,
                                      headers=['Invoice #', 'PEID', 'Date arrived', '# days in queue', 'Security Code'],
                                      tablefmt='pretty', stralign='center', numalign='center'))

    # Takes the variable that's storing the HTML email body and formats the table that is instantiated within
    # the variable. This uses the formatting "html," center aligned for strings and numbers, and contains headers:
    # Invoice number
    # Vendor ID
    # Date arrived at the reviewer's queue
    # Number of business days at the reviewer's queue
    html = html.format(table=tabulate(tab_log,
                                      headers=['Invoice #', 'PEID', 'Date arrived', '# days in queue', 'Security Code'],
                                      tablefmt='html', stralign='center', numalign='center'))

    # Clear the tab log for the next iteration
    tab_log.clear()

    # If the email that is picked up from the original instantiation of the variables is not in the list of recipients,
    # add it
    if email not in recipient_emails:
        recipient_emails.append(email)
    # I was printing out the recipient emails to the console because of a bug that I was experiencing.
    # I'll leave it for now
    print(recipient_emails)

    # Setting the requisite headers and variables for sending an email:
    # Making the message of MIMEMultipart type
    message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html, 'html')])
    # Adding subject header, with the current date for organizational purposes for the reviewers
    message['Subject'] = 'There are invoice(s) pending in your APOHININ queue (' + now + ')'
    # Header that shows it's from me
    message['From'] = sender_email
    # This just joins all the recipient emails together as a comma-separated list and assigns them to the "To" header
    message['To'] = ", ".join(recipient_emails)
    # Point to the correct server (port embedded into above server string variable)
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    # Log in with email and the password collected from getpass above
    server.login(sender_email, pwd)
    # Sends email from the sender email to the recipient emails, and casting the message as a string because I noticed
    # sometimes it throws an error if it isn't cast as a string
    server.sendmail(sender_email, recipient_emails, message.as_string())
    # I put it to sleep for a bit to not trigger the server's spam email alert.
    # I may or may not have done that in the past
    time.sleep(30)
    server.quit()

    # Because the first two email addresses are to be on every email sent out, I am only taking off the address that
    # was added last; that is, I'm poppin' it
    if len(recipient_emails) > 2:
        recipient_emails.pop()
