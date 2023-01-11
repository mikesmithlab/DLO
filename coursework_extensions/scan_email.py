import os, sys

parent = os.path.abspath('.')
sys.path.insert(1, parent)

import win32com.client as win32
import datetime
import pathlib

#from messages import manual_email, approve_email

from emails import auto_email
from pydates.pydates import now, relative_datetime, format_datetime_to_str

def scan_recent_email(filepath=None):
    """
    Scan all email in last 14 days. Find those from SS_SERVICES containing attachments
    and then download with uniqueid for filename as long as they are not email signatures such as 'image001.jpg'
    """
    outlook = auto_email.open_outlook()
    
    email_addresses=auto_email.find_sender_emails(outlook, folder=('Inbox','DLO','coursework_extensions'))
    
    filter = {'start': relative_datetime(now(),delta_day=-14),
              'stop':relative_datetime(now(),delta_day=1),
              'has_attachments':True}   

    for email in email_addresses:
        filter['from_email'] = email
        msgs = auto_email.get_emails(outlook, filter=filter)
        auto_email.download_attachments(msgs, filepath, filter_out=('.jpg','.png'), change_filename=True)
        auto_email.move_emails(outlook, msgs, folder=('Inbox','DLO','coursework_extensions'))

def clean_email():
    #Ridding inbox of all the support plan notifications
    outlook = auto_email.open_outlook()
    
    email_addresses=auto_email.find_sender_emails(outlook, folder=('Inbox','DLO','support_plan'))  

    filter = {'subject':'Support Plan'} 

    for email in email_addresses:
        filter['from_email'] = email
        msgs = auto_email.get_emails(outlook, filter=filter)
        auto_email.move_emails(outlook, msgs, folder=('Inbox','DLO','coursework_extensions'))

if __name__ == '__main__':
    clean_email()
"""
def send_email(msg, attachments=None, filepath = DLO_DIR + 'Approved_extensions/'):
    
    Only works from local outlook email client

    msg is a dictionary of the info for email
    attachments should be a list of filenames.
    

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = msg['to']
    mail.Subject = msg['subject']
    mail.Body = msg['body']
    if 'html_body' in msg.keys():
        mail.HTMLBody = msg['html_body']

    if attachments is not None:
        for attachment in attachments:
            mail.Attachments.Add(attachment)

    mail.Send()

#if __name__ == '__main__':
#    scan_recent_email(email_address='ppzmjs@exmail.nottingham.ac.uk')
"""