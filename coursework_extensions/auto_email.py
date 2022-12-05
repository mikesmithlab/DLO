import win32com.client as win32
import datetime
import pathlib


from addresses import DLO_DIR, SS_SERVICES

approve_email = {
        'subject' : 'course work extension approved',
        'body' : 'approved',
        'to' : 'mike.i.smith@nottingham.ac.uk',
        }

manual_email = {
        'subject' : 'You have manual extensions to process',
        'body' : '',
        'to' : 'mike.i.smith@nottingham.ac.uk',
        }

"""
disregard_element_email = {
    'subject' : 'Concern about your tutee',
    'body' : '',
    'to' : '',
    'cc : 'frazer.pearce@nottingham.ac.uk; kim
}
"""




def scan_recent_email(email_address=SS_SERVICES,
                    filepath = DLO_DIR + 'Extensions_to_approve/'):

    #/O=EXCHANGELABS/OU=EXCHANGE ADMINISTRATIVE GROUP (FYDIBOHF23SPDLT)/CN=RECIPIENTS/CN=99114A96025D4D768FB7BF3BC9DB1D36-SS-ASSESS-S

    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages=inbox.Items
    coursework = inbox.Folders['DLO'].Folders['coursework_extensions']

    #Filter email
    start_time = str((datetime.datetime.now().replace(hour=0,minute=0,second=0)-datetime.timedelta(days=7)).strftime("%Y-%d-%m %H:%M %p"))
    stop_time = str(datetime.datetime.now().replace(hour=23,minute=59,second=59).strftime("%Y-%d-%m %H:%M %p"))
    messages = messages.Restrict("[ReceivedTime] >= '" + start_time + "' And [ReceivedTime] <= '" + stop_time + "'")
    messages = messages.Restrict("[SenderEmailAddress] = '{}'".format(email_address))
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

