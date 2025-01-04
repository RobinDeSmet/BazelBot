from enum import Enum
from pydantic import BaseModel, Field


class BazelType(Enum):
    """Bazeltype enum"""

    NORMAL = "normal"
    CUSTOM = "custom"


class BazelFlavour(BaseModel):
    bazel_flavour_name: str = Field(
        ..., description="The name of the bazel text flavour."
    )
    bazel_instructions: str = Field(
        ...,
        description="The instructions that need to be added to the prompt to use this bazel text flavour",
    )
    image_flavour_name: str = Field(
        ..., description="The name of the bazel image flavour."
    )
    image_instructions: str = Field(
        ...,
        description="The instructions that need to be added to the prompt to use this bazel image flavour",
    )

    def __str__(self):
        output = ""
        output += "\nBAZEL FLAVOUR DATA:\n"
        output += f"bazel flavour name: {self.bazel_flavour_name}\n"
        output += f"bazel instructions: {self.bazel_instructions}\n"
        output += f"image flavour name: {self.image_flavour_name}\n"
        output += f"image instructions: {self.image_instructions}\n"
        return output


class BazelImageDescriptionModel(BaseModel):
    description: str = Field(
        ...,
        description="The detailed description of the bazel used to generate an image.",
    )


class BazelGenerationIntermediateModel(BaseModel):
    text: str = Field(..., description="The bazel content in text format.")
    text_english: str = Field(..., description="The English version of the bazel.")


class BazelModel(BaseModel):
    text: str = Field(..., description="The bazel content in text format.")
    bazel_flavour: BazelFlavour = Field(
        ...,
        description=" The flavour of the bazel.",
    )
    text_english: str = Field(..., description="The English version of the bazel.")
    image_description: str = Field(
        ..., description="The detailed description of the image."
    )

    def __str__(self):
        output = ""
        output += f"\nBAZEL: {self.text}\n"
        output += f"English translation: {self.text_english}\n"
        output += f"{self.bazel_flavour}\n"
        return output
