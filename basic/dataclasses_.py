from dataclasses import dataclass,field


@dataclass
class Student:
    name: str='default'
    gender: str='default'
    age: int='default'
    number: int='default'
    listdata: list=field(default_factory=list)
    dictdata: dict=field(default_factory=dict)
    admin: bool=True


stu01 = Student('KK', 'F', 23, 2201, [1,2], {'ca':' ca'}, True)
print(stu01)
print(stu01.name)
print(stu01.dictdata)