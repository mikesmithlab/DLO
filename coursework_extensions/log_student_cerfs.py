import os, sys

parent = os.path.abspath('.')
sys.path.insert(1, parent)
parent = os.path.abspath('..')
sys.path.insert(1, parent)

from filehandling import BatchProcess, get_directory_filenames
from emails.auto_email import send_email
from scan_email import scan_recent_email

from form_sign import process_extension, store_files, cleanup
from messages import manual_email, approve_email
from checks import check_num_requests


from addresses import DLO_DIR, CERF_LOG
import pandas as pd


#Scan email for coursework extension requests and download
print('scanning email...')
msgs = scan_recent_email(filepath=DLO_DIR + 'Extensions_to_approve/')
df = pd.read_excel(CERF_LOG)
print(df.head())
print(msgs)

