"""Custom types module"""

from enum import Enum

from pydantic import BaseModel, Field


class BazelModel(BaseModel):
    text: str = Field(..., description="The bazel content in text format.")


class BazelType(Enum):
    """Bazeltype enum"""

    NORMAL = "normal"
    CUSTOM = "custom"
