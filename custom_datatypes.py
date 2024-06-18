from custom_exceptions import StudentIdException, ModuleCodeException, YearGroupException
from collections import UserDict

class StudentId(int):
    """StudentID type which enforces possible value"""
    def __new__(cls, value):
        print(value)
        if len(str(value)) != 8:
            raise StudentIdException
        if (str(value)[0] != '1') and (str(value)[0] != '2'):
            raise StudentIdException
        return int.__new__(cls, value)

class StudentRecord(UserDict):
    def __new__(cls):
        return UserDict.__new__(cls)
        

class ModuleCode(str):
    def __new__(cls, value):
        module_codes = ['PHYS3001', 'PHYS2005', 'PHYS1001', 'PHYS1004', 'PHYS4002', 'PHYS4015', 'COMP3009', 'MATH2008','MATH4015', 'PHYS1002', 'MATH3002', 'MATH1001', 'MATH4017', 'HIST1008', 'PHYS3002', 'MATH3010', 'PHYS2002', 'LANG1003', 'LANG3002', 'LANG1007', 'PSGY1005', 'PHYS2006', 'LANG4003', 'COMP4008', 'LIFE2018', 'LANG4001', 'PHYS3008', 'LANG2006', 'MMME4060', 'PHYS4035', 'PHIL3002', 'PHYS2003', 'LANG3007', 'PHYS4010', 'MATH4022', 'LANG1012', 'PHYS3004', 'MATH3004', 'LANG1001', 'LANG2001', 'MUSI2011', 'THEO1007', 'LANG1002', 'PHYS4024', 'LANG2003', 'LANG2009', 'PHIL3003', 'MATH1005', 'LANG3005', 'PHYS4004', 'EEEE3019', 'MATH4049', 'THEO2001', 'PHYS4031', 'MATH4065', 'LANG3001', 'LANG1004', 'LANG1014', 'PHIL3001', 'LANG3004', 'LIFE4030', 'PHYS1003', 'PHYS4021', 'MATH2007', 'MATH4016', 'MATH4009', 'PHYS4008', 'PHYS4026', 'PHYS4003', 'MATH3024', 'PHYS4020', 'LANG1010', 'LANG3009', 'PHYS1005', 'MATH2009', 'LANG4004', 'MATH3011', 'MATH2005', 'LANG4002', 'COMP3020', 'LANG2012', 'PHYS4036', 'PHYS2004', 'LANG3014', 'PHYS4007', 'PHYS3011', 'PHYS3005', 'LANG1019', 'LANG1009', 'LANG2002', 'LIFE2046', 'LANG2010', 'MATH1006', 'PHYS4016', 'LANG3012', 'LANG1013', 'PHYS4019', 'PHYS4038', 'LANG3008', 'LANG1008', 'LANG1011', 'LANG1015', 'PHIL3008', 'PHYS4018', 'PHYS4030', 'PHYS4014', 'PHYS4029', 'PHIL1012', 'COMP2005', 'MATH2012', 'PHYS4013', 'PHIL3013', 'PHYS4037', 'PHYS4022', 'PHYS3013', 'PHYS2001', 'PHYS3010', 'PHIL2004', 'PHYS4006', 'PHYS1006', 'MATH3035', 'PHYS3015', 'MATH1007', 'PHYS4025', 'COMP4124', 'MATH3018', 'PHYS4032', 'MLAC1100', 'PHYS4017', 'MATH3017', 'PHIL1013', 'PHIL3011', 'PHIL2007', 'PHYS3009', 'PHYS4005', 'PHYS3012', 'PHYS3007', 'PHIL2008', 'PHYS4041', 'PHIL2006', 'PHYS4009', 'PHIL1014', 'MATH2013', 'PHIL1016', 'COMP4106', 'PHIL2009', 'PHIL2013', 'MATH3016', 'BIOS1052', 'COMP4019', 'PSGY4063', 'MATH3027', 'MATH4045', 'PHIL2054', 'PHYS2007', 'PSGY4062', 'PHIL3022', 'MTHS3003', 'PHIL2055', 'COMP4105', 'PHIL3028', 'COMP2006', 'PHIL2053', 'PHIL2012', 'PHIL3034', 'CHEM4006', 'MMME3066', 'MATH2019', 'PHIL3035', 'BIOS3103', 'EDUC2039', 'EEEE4125'
            ]

        if type(value) is not type(' '):
            raise ModuleCodeException

        value = value.upper()

        if value not in module_codes:
            raise ModuleCodeException
            
        return str.__new__(cls, value)

class YearGroup(str):
    def __new__(cls, value):
        Years = ['01','02','03','04','PGT','PGR']
        
        if type(value) is not type(' '):
            print(value)
            #raise YearGroupException

        value=str(value).lstrip("0").upper()
        if value.isnumeric():
            value = "0" + value

        if value not in Years:
            #raise YearGroupException
            print(value)

        return str.__new__(cls, value)


if __name__ =='__main__':
    bob = StudentRecord()
    bob['test']=5
    print(bob.keys())

