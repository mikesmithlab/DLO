from enum import auto
import os
import os, sys

parent = os.path.abspath('.')
sys.path.insert(1, parent)

import addresses

from emails import auto_email

outlook = auto_email.open_outlook()

    


