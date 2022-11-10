import win32com.client as win32
import datetime
import pathlib

def scan_todays_email(email_address='/O=EXCHANGELABS/OU=EXCHANGE ADMINISTRATIVE GROUP (FYDIBOHF23SPDLT)/CN=RECIPIENTS/CN=99114A96025D4D768FB7BF3BC9DB1D36-SS-ASSESS-S',
                    filepath = 'C:\\Users\\ppzmis\\OneDrive - The University of Nottingham\\Documents\\DLO\\Extensions_to_approve\\'):

    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    messages=inbox.Items
    coursework = inbox.Folders['DLO'].Folders['coursework_extensions']


    #Filter email
    start_time = str(datetime.datetime.now().replace(hour=0,minute=0,second=0).strftime("%Y-%d-%m %H:%M %p"))
    stop_time = str(datetime.datetime.now().replace(hour=23,minute=59,second=59).strftime("%Y-%d-%m %H:%M %p"))
    messages = messages.Restrict("[ReceivedTime] >= '" + start_time + "' And [ReceivedTime] <= '" + stop_time + "'")
    messages = messages.Restrict("[SenderEmailAddress] = '{}'".format(email_address))
    inbox_msgs = list(messages)


    attachment_names = []
    for i,message in enumerate(inbox_msgs):
        if len(message.Attachments) > 1:
            for j,attachment in enumerate(message.Attachments):
                if attachment.FileName != 'image001.jpg':
                    output_file = 'request_'+str(i) + '_' + str(j) + pathlib.Path(attachment.FileName).suffix
                    attachment.SaveAsFile(filepath + output_file)
                    attachment_names.append(output_file)
            message.Move(coursework)

    return attachment_names




def send_email(attachment, email_dictionary, filepath = 'C:\\Users\\ppzmis\\OneDrive - The University of Nottingham\\Documents\\DLO\\Approved_extensions\\'):

    #Only works from local email client
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = email['to']
    mail.Subject = email['subject']
    mail.Body = email['body']
    #mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional
    mail.Attachments.Add(filepath + attachment)

    mail.Send()


if __name__ =='__main__':
    filename = 'test.docx'

    email = {
        'subject' : 'course work extension approved',
        'body' : 'approved',
        'to' : 'mike.i.smith@nottingham.ac.uk',
        }


    scan_todays_email()