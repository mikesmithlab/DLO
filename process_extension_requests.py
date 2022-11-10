from filehandling import BatchProcess
from auto_email import scan_todays_email, send_email
from form_sign import process_docx


#scan_todays_email()

for filename in BatchProcess('C:\\Users\\ppzmis\\OneDrive - The University of Nottingham\\Documents\\DLO\\Extensions_to_approve\\*.docx'):
    print(filename)
    process_docx(filename=filename)


