from enum import Enum, unique


@unique
class TimeUnitType(Enum):
    Year = 'Y'  # Year的value被设定为0
    Month = 'M'
    Decad = 'D'
    Week = 'W'
    Day = 'd'
    Hour = 'h'
    Minute = 'm'
    Second = 's'
