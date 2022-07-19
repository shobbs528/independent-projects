from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate
import csv
import getpass
import os
import pyodbc
import smtplib


full_stats_log = []
cur_stats_log = []
smtp_server = '' # redacted server
recipient_emails = ['SKHobson@SolanoCounty.com']
sender_email = 'SKHobson@SolanoCounty.com'
text = ''
pwd = ''
parent_folder = '' # redacted file path
cur_month = datetime.now().strftime('%B')
cur_year = datetime.now().year
temp_log = []
stats_path = f"file:///" # redacted file path
table = ''

cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};'
                      'SERVER=' # redacted server
                      'DATABASE=' # redacted database
                      'trusted_connection=yes')
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin-1')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')
cnxn.setencoding(encoding='latin-1')

crsr = cnxn.cursor()
stmt = f"select case when CAST(MONTH(MAX(wf_when_out)) as INT) = 1 THEN 'JANUARY' when CAST(MONTH(MAX(wf_when_out)) " \
       f"as INT) = 2 THEN 'FEBRUARY' when CAST(MONTH(MAX(wf_when_out)) as INT) = 3 THEN 'MARCH' when CAST(MONTH(MAX(" \
       f"wf_when_out)) as INT) = 4 THEN 'APRIL' when CAST(MONTH(MAX(wf_when_out)) as INT) = 5 THEN 'MAY' when CAST(" \
       f"MONTH(MAX(wf_when_out)) as INT) = 6 THEN 'JUNE' when CAST(MONTH(MAX(wf_when_out)) as INT) = 7 THEN 'JULY' " \
       f"when CAST(MONTH(MAX(wf_when_out)) as INT) = 8 THEN 'AUGUST' when CAST(MONTH(MAX(wf_when_out)) as INT) = 9 " \
       f"THEN 'SEPTEMBER' when CAST(MONTH(MAX(wf_when_out)) as INT) = 10 THEN 'OCTOBER' when CAST(MONTH(MAX(" \
       f"wf_when_out)) as INT) = 11 THEN 'NOVEMBER' when CAST(MONTH(MAX(wf_when_out)) as INT) = 12 THEN 'DECEMBER' " \
       f"end as 'Month Approved',CAST(YEAR(MAX(wf_when_out)) as INT) as 'Year Approved', wf_us_id, wf_status, " \
       f"CAST(count(bir.oh_ref) as INT) from oh_bir_mstr bir, ohb_batch_dtl batch, wf_history wf where bir.oh_ref = " \
       f"batch.oh_ref and bir.unique_key = wf_key and ohb_sec_cd is not null and ohb_sec_cd <> '' and wf_activity_id " \
       f"like 'A19_0%' and wf_status in ('Y','N') and wf_activity_id like 'A19_0%' group by MONTH(wf_when_out), " \
       f"YEAR(wf_when_out), wf_us_id, wf_status order by 2,MONTH(wf_when_out), 3, 4"

rows = crsr.execute(stmt)

if os.path.isdir(parent_folder):
    file_name = parent_folder + '/GA_Stats.csv'
else:
    os.makedirs(parent_folder)
    file_name = parent_folder + '/GA_Stats.csv'

with open(file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in rows:
        writer.writerow(row)

with open(file_name, 'rt', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        for col in range(len(row)):
            row[col] = row[col].strip()
        full_stats_log.append(row)

for element in full_stats_log:
    element[4] = int(element[4])

user = getpass.getuser()
pwd = getpass.getpass(f"Password for {user}:\n")

try:
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    server.login(sender_email, pwd)
    server.quit()
except Exception as e:
    print('Invalid password:\n', e)
    quit()

text = """ \
Hello,\n
Here are the stats for the GA ININ reviewers for the month of """ + cur_month + """ """ + str(cur_year) +""":
{table}
file:///""" + # redacted file
"""\n
Good day,
SH
"""

html = """ \
<html>
<body>
<p>Hello,</p>
<p>Here are the stats for the GA ININ reviewers for the month of """ + cur_month + """ """ + str(cur_year) + """:</p>
{table}
<a href="file:///.txt">Link to full stats</a><br>""" # redacted file path
+ """<p>Good Day,</p>
<p>SH</p>
</body>
</html>
"""

print('\n'.join(' '.join(map(str, sub)) for sub in full_stats_log))

# go through full stats list and parse down to current month and year
for i in range(len(full_stats_log)):
    for j in range(len(full_stats_log[i])):

        if full_stats_log[i][0].lower() == cur_month.lower() and int(full_stats_log[i][1]) == cur_year:
            temp_log.append(full_stats_log[i][0])
            temp_log.append(full_stats_log[i][1])
            temp_log.append(full_stats_log[i][2])

            if full_stats_log[i][3].lower() == 'n':
                temp_log.append('Rejections')
            elif full_stats_log[i][3].lower() == 'y':
                temp_log.append('Approvals')
            else:
                temp_log.append('other')

            temp_log.append(full_stats_log[i][4])
            break
        else:
            break
    if not all(x == [] for x in temp_log):
        cur_stats_log.append(temp_log[:])
        temp_log.clear()

# print('\n'.join(' '.join(map(str, sub)) for sub in cur_stats_log))

text = text.format(table=tabulate(cur_stats_log, headers=['Month', 'Year', 'Approver', 'Action', '#'], tablefmt='html', stralign='center', numalign='center'))

html = html.format(table=tabulate(cur_stats_log, headers=['Month', 'Year', 'Approver', 'Action', '#'], tablefmt='html', stralign='center', numalign='center'))

full_table = tabulate(full_stats_log, headers=['Month', 'Year', 'Approver', 'Action', '#'], tablefmt='pretty', stralign='center', numalign='center')

fo = open('GA_Stats.txt', 'w') # redacted file path
fo.write(full_table)
fo.close()

print(cur_month, cur_year)
print(full_table)

message = MIMEMultipart('alternative')
message['Subject'] = 'GA Review Stats for ' + cur_month + ' ' + cur_year.__str__()
message['From'] = sender_email
message['To'] = ", ".join(recipient_emails)
message.attach(MIMEText(text, 'plain'))
message.attach(MIMEText(html, 'html'))
server = smtplib.SMTP(smtp_server)
server.ehlo()
server.starttls()
server.login(sender_email, pwd)
server.sendmail(sender_email, recipient_emails, message.as_string())
server.quit()

print(message)
