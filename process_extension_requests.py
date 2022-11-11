from filehandling import BatchProcess, get_directory_filenames
from auto_email import scan_recent_email, send_email, manual_email, approve_email
from form_sign import process, store_files




scan_recent_email()
manual=False
for filename in BatchProcess('C:/Users/ppzmis/OneDrive - The University of Nottingham/Documents/DLO/Extensions_to_approve/*.*'):
    not_processed = process(filename=filename)
    if not_processed:
        manual=True

if manual:
    send_email(manual_email)

#Send processed files as attachments
approved_files = get_directory_filenames('C:/Users/ppzmis/OneDrive - The University of Nottingham/Documents/DLO/Approved_extensions/*.docx')

send_email(approve_email, approved_files)
store_files(approved_files, filepath='')




