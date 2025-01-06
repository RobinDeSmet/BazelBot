import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from src.prompts.system import SYSTEM_PROMPT
from src.utils.errors import GenerationFailedError

logger = logging.getLogger(__name__)

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


class LLM:
    """Gemini LLM."""

    def __init__(
        self, model: str = GEMINI_MODEL, system_instruction: str = SYSTEM_PROMPT
    ):
        """Init an LLM instance.

        Args:
            model (str, optional): The specific llm model. Defaults to GEMINI_MODEL.
            system_instruction (str, optional): The system instructions. Defaults to SYSTEM_PROMPT.
        """
        # Configure the safety settings
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Configure the model
        self.llm = genai.GenerativeModel(
            model,
            safety_settings=self.safety_settings,
            system_instruction=system_instruction,
        )

    def get_llm(self) -> genai.GenerativeModel:
        """Return the Gemini LLM.

        Returns:
            genai.GenerativeModel: The specific Gemini model.
        """
        return self.llm

    def generate_content(
        self, prompt: str, generation_config: genai.GenerationConfig
    ) -> Any:
        """Generate content with the LLM.

        Args:
            prompt (str): The user prompt.
            generation_config (genai.GenerationConfig): The config for generating content.

        Returns:
            Any: The model specified in the generation config response schema.

        Raises:
            GenerationFailedError: When the generation fails.
        """
        for i in range(4):
            try:
                response = self.llm.generate_content(
                    prompt, generation_config=generation_config
                )
                return generation_config.response_schema(**json.loads(response.text))
            except Exception as e:
                if i >= 3:
                    logger.error(f"Could not generate content: {e}")
                    raise GenerationFailedError(f"Could not generate content: {e}")
                else:
                    logger.info("Generation of content failed. Retrying...")
