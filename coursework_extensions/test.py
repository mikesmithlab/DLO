from enum import auto
import os
import os, sys

parent = os.path.abspath('.')
sys.path.insert(1, parent)

import addresses

from emails import auto_email



    
class Test:
    def __init__(self):
        self.FileName = 'asdij.docx'

attachment = Test()

print(auto_email._keep_attachment(attachment, ('.jpg',)))


