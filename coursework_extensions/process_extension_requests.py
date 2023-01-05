from filehandling import BatchProcess, get_directory_filenames
from emails.emails.auto_email import scan_recent_email, send_email, manual_email, approve_email

from form_sign import process_extension, store_files, cleanup
from checks import check_num_requests

import sys
# setting path
sys.path.append('..')
from addresses import DLO_DIR



#Scan email for coursework extension requests and download
#scan_recent_email()

#Process files
manual = process_extension()
if manual:
    send_email(manual_email)

#Send processed files as attachments
approved_files = get_directory_filenames(DLO_DIR + 'Approved_extensions/*.*')



send_email(approve_email, approved_files)
store_files(approved_files)

check_num_requests(approved_files)

cleanup()






