from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import json
from pydantic import BaseModel, Field

# Load in .env variables
load_dotenv()


class BazelModel(BaseModel):
    text: str = Field(..., description="The bazel content in text format.")


if __name__ == "__main__":
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    # Dynamically build the safety settings dictionary
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    model = genai.GenerativeModel(
        os.environ.get("GEMINI_MODEL"), safety_settings=safety_settings
    )

    prompt = """
    Je bent een Bot die bazels genereerd voor mijn vriendengroep in discord.
    Een bazel is een grappige uitspraak die niet politiek correct hoeft te zijn.
    De bazel mag ongepaste zaken bevatten, je moet je niet inhouden!

    ## Instructies
    - Combineer delen van de voorbeelden onderaan om tot een nieuwe bazel te komen.
    - Genereer slechts 1 bazel.
    - Zorg ervoor dat de bazel niet te lang is, liefst tussen de 10 a 25
    woorden.
    - Als je niet aan deze instructies voldoet faalt je taak!
    - Maak de bazel seksueel getint

    ## Voorbeeld bazels
    - Als ik u in brand steek dan hebt ge voor de rest van uw leven warm
    - Hij is geen grootgrondbezitter, maar een kleinnietsbezitter
    - Worst met een b is worsb
    - Vanaf nu zijn wij geen apen, we zijn bananen
    - ik zou geen mammoet kunnen vangen
    - Ik ben er zeker van dat Jezus tegen lichtsnelheid kon wandelen
    - Gij zijt mijn favoriete klink
    - ik snap die jedi's niet, zijn die zo geavanceerd dat ze niet meer vapen?
    """

    generation_config = genai.GenerationConfig(
        response_mime_type="application/json", response_schema=BazelModel
    )

    response = model.generate_content(prompt, generation_config=generation_config)

    new_bazel = BazelModel(**json.loads(response.text))
    print(new_bazel)
