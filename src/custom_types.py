"""Custom types module"""

from enum import Enum


class BazelType(Enum):
    """Bazeltype enum"""

    NORMAL = "normal"
    CUSTOM = "custom"
