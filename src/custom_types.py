"""Custom types module"""

from enum import Enum

from pydantic import BaseModel, Field


class BazelModel(BaseModel):
    text: str = Field(..., description="The bazel content in text format.")
    text_english: str = Field(..., description="The English version of the Bazel.")


class BazelImageDescriptionModel(BaseModel):
    description: str = Field(
        ...,
        description="The detailed description of the Bazel used to generate an image.",
    )


class BazelType(Enum):
    """Bazeltype enum"""

    NORMAL = "normal"
    CUSTOM = "custom"
