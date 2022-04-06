from enum import Enum
from ..types.type import *

class CTypeQualifier(Enum):
    CONST = "const",
    VOLATILE = "volatile",
    RESTRICT = "restrict",
    ATOMIC = "_Atomic",
    STATIC = "static"