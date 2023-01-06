import os, sys
parent = os.path.abspath('.')
sys.path.insert(1, parent)

from filehandling import list_files

from addresses import DLO_DIR



def check_num_requests(approved_files, filepath=DLO_DIR + 'Approved_extensions/'):
    """
    Check if students are creating excessive numbers of coursework extension requests
    """
    for file in approved_files:
        filename = os.path.basename(file)
        student_name = filename.split('_')[-1].split('.')[0]
        year = filename.split('_')[0]
        folder = year + '_' + student_name
        num_coursework_requests = len(list_files(filepath + folder + '/*'))
        if num_coursework_requests >= 4:
            print(student_name + ' has now requested ' + str(num_coursework_requests) + ' coursework requests this year')


