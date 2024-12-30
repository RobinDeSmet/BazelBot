"""Custom types module"""

from enum import Enum
import logging
import random
import aiohttp
import requests
import datetime
import time
import io

from PIL import Image
from pydantic import BaseModel, Field

IMAGE_API: str = "image.pollinations.ai"
HEADER: dict = {"Content-Type": "application/json"}

logger = logging.getLogger(__name__)


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


class ImageObject(object):
    def __init__(
        self,
        prompt: str = "",
        negative: str = "",
        model: str = "",
        params: dict = {},
        *args,
        **kwargs,
    ) -> None:
        self.prompt: str = str(prompt)
        self.negative: str = str(negative)
        self.model: str = str(model)
        self.params: dict = dict(params)
        self.time: str = (
            f"[{datetime.date.today().strftime('%Y-%m-%d')}] {time.strftime('%H:%M:%S')}"
        )

    def save(
        self, file: str = "image-output.png", timeout: int = 60, *args, **kwargs
    ) -> object:
        request: requests.Request = requests.get(
            url=self.params["url"],
            headers=HEADER,
            timeout=timeout,
        )
        Image.open(io.BytesIO(request.content)).save(file)

    def __str__(self) -> str:
        return f"ImageObject({self.prompt=}, {self.negative=}, {self.model=}, {self.params=}, {self.time=})"

    def __repr__(self) -> repr:
        return repr(self.__str__())


class ImageModel(object):
    def __init__(
        self,
        model: str = "evil",
        seed: int = 0,
        width: int = 1024,
        height: int = 1024,
        enhance: bool = False,
        nologo: bool = False,
        private: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.model: str = str(model)
        self.seed: int = seed
        self.width: int = int(width)
        self.height: int = int(height)
        self.enhance: bool = bool(enhance)
        self.nologo: bool = bool(nologo)
        self.private: bool = bool(private)

    async def generate(
        self,
        prompt: str,
        negative: str = "",
        save: bool = False,
        file: str = "image-output.png",
        timeout: int = 60,
        *args,
        **kwargs,
    ) -> ImageObject:
        prompt: str = str(prompt)
        save: bool = bool(save)
        file: str = str(file)

        seed: int = self.seed

        if self.seed == "random":
            seed: int = random.randint(0, 9999999999)

        params: str = (
            f"negative={negative}&seed={seed}&width={self.width}&height={self.height}&nologo={self.nologo}&private={self.private}&model={self.model}&enhance={self.enhance}"
        )
        url: str = f"https://{IMAGE_API}/prompt/{prompt}?{params}"

        async with aiohttp.ClientSession(
            headers={"Content-Type": "application/json"}
        ) as session:
            async with session.get(url=url) as response:
                if response.status == 200:
                    content = await response.read()
                    try:
                        image: Image = Image.open(io.BytesIO(content))
                        if save:
                            image.save(file)

                        params = {
                            "seed": seed,
                            "width": self.width,
                            "height": self.height,
                            "nologo": self.nologo,
                            "private": self.private,
                            "enhance": self.enhance,
                            "url": url,
                        }
                        image_object: ImageObject = ImageObject(
                            prompt=prompt,
                            negative=negative,
                            model=self.model,
                            params=params,
                        )
                        return image_object
                    except Exception as e:
                        logger.error(
                            "Image generation failed while processing content."
                        )
                        raise ValueError(
                            f"Image generation failed while processing content: {e}"
                        ) from e
                else:
                    logger.error(
                        f"Image generation failed with status {response.status}"
                    )
                    raise Exception(f"Failed to fetch: {response.status}")
