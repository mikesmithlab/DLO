from filehandling import BatchProcess, get_directory_filenames
from auto_email import scan_recent_email, send_email, manual_email, approve_email
from form_sign import process_extension, store_files, cleanup



#Scan email for coursework extension requests and download
#scan_recent_email()

#Process files
#manual = process_extension()
#if manual:
#    send_email(manual_email)

#Send processed files as attachments
approved_files = get_directory_filenames('C:/Users/ppzmis/OneDrive - The University of Nottingham/Documents/DLO/Approved_extensions/*.*')

send_email(approve_email, approved_files)
store_files(approved_files)
cleanup()




