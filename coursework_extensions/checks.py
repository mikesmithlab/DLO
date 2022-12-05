from addresses import DLO_DIR


def check_num_requests(approved_files, filepath='C:/Users/ppzmis/OneDrive - The University of Nottingham/Documents/DLO/Approved_extensions/'):
    for file in approved_files:
        student_name = file.split('_')[-1]
        year = file.split('_')[0]
        folder = year + '_' + student_name

