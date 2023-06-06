from dataclasses import dataclass


@dataclass
class Student:
    name: str='default'
    gender: str='default'
    age: int='default'
    number: int='default'
    admin: bool=True


stu01 = Student('KK', 'F', 23, 2201)
print(stu01.name)
stu02 = Student('MM', 'M', 20, 2202)
print(stu02 == stu01)
stu03 = Student()
print(stu03)