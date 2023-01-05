import win32com.client as win32
import datetime
import pathlib

import sys

# setting path
sys.path.append('..')

from addresses import DLO_DIR, SS_SERVICES, MEL
from messages import manual_email, approve_email

from emails import auto_email
from pydates.pydates import now, relative_datetime




def scan_recent_email(email_addresses=SS_SERVICES,
                    filepath=DLO_DIR + 'Extensions_to_approve/'):

    outlook = auto_email.open_outlook()

    if type(email_addresses) == str:
        email_addresses = [email_addresses]

    filter = {'start': relative_datetime(now(),delta_day=1),
              'stop':relative_datetime(now(),delta_day=-7),
              'has_attachments':True}

    for email in email_addresses:
        filter['from_email'] = email
        msgs = auto_email.get_emails(outlook, filter=filter)
        auto_email.download_attachments(msgs, filepath)



    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages=inbox.Items
    coursework = inbox.Folders['DLO'].Folders['coursework_extensions']

    inbox_msgs = list(messages)

    attachment_names = []
    for i,message in enumerate(inbox_msgs):
        if len(message.Attachments) >= 1:
            for j,attachment in enumerate(message.Attachments):
                if attachment.FileName != 'image001.jpg':
                    output_file = 'request_'+str(i) + '_' + str(j) + pathlib.Path(attachment.FileName).suffix
                    attachment.SaveAsFile(filepath + output_file)
                    attachment_names.append(output_file)
            message.Move(coursework)

    return attachment_names

def send_email(msg, attachments=None, filepath = DLO_DIR + 'Approved_extensions/'):
    """
    Only works from local outlook email client

    msg is a dictionary of the info for email
    attachments should be a list of filenames.
    """

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