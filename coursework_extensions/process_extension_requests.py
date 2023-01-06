import os, sys

parent = os.path.abspath('.')
sys.path.insert(1, parent)

from filehandling import BatchProcess, get_directory_filenames
from emails.auto_email import send_email
from scan_email import scan_recent_email

from form_sign import process_extension, store_files, cleanup
from messages import manual_email, approve_email
from checks import check_num_requests


from addresses import DLO_DIR


#Scan email for coursework extension requests and download
scan_recent_email(filepath=DLO_DIR + 'Extensions_to_approve/')


#Process files
manual = process_extension()
if manual:
    send_email(manual_email)

#Send processed files as attachments
approved_files = get_directory_filenames(DLO_DIR + 'Approved_extensions/*.*')
print(approved_files)

#Send email with approved files attached
send_email(approve_email, approved_files)

store_files(approved_files)

check_num_requests(approved_files)

cleanup()






