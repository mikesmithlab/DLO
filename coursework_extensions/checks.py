from filehandling import list_files

from addresses import DLO_DIR



def check_num_requests(approved_files, filepath=DLO_DIR + 'Approved_extensions/'):
    """
    Check if students are creating excessive numbers of coursework extension requests
    """
    for file in approved_files:
        student_name = file.split('_')[-1]
        year = file.split('_')[0]
        folder = year + '_' + student_name
        num_coursework_requests = len(list_files(filepath + folder))
        if num_coursework_requests >= 4:
            print(student_name + ' has now requested ' str(num_coursework_requests) ' coursework requests this year')



