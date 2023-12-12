from enum import StrEnum, auto


# Using auto() with StrEnum results in the lower-cased member name as the value.
class Process(StrEnum):
    THUMBNAIL = auto()
    BLUR = auto()
