from enum import Enum, unique

@unique
class Color(Enum):
    Red=(255,0,0)
    Green=(0,255,0)
    Blue=(0,0,255)