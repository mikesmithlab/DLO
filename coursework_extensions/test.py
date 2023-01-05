
from filehandling import BatchProcess


filter = 'C:/Users/mikei/OneDrive - The University of Nottingham/Documents/DLO/Approved_extensions/*/2022_12_*'

for i, file in enumerate(BatchProcess(filter)):
    print(i)
