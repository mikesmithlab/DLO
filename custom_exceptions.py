class StudentIdException(Exception):
    def __init__(self):
        super().__init__()
        print('Student ID format incorrect. Should be int or str, 8 digits, beginning with 1 or 2.')

class ModuleCodeException(Exception):
    def __init__(self):
        super().__init__()
        print('Module code not valid. Should be an 8 digit string containing 4 letters followed by 4 numbers and be from the enumerated list')

class YearGroupException(Exception):
    def __init__(self):
        super().__init__()
        print('Year group not acceptable value')