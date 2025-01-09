# INFO:
# - Flavours should be stored alphabetically.
# - The key of the flavour is the 'name' of that flavour
# - The weight will determine the chance of that flavour being selected.
# - The instructions have to be added to the prompt for the flavour to take effect.
#   They should be conform to the following structure:
#   - instruction 1
#   - instruction 2
#   - ...
#   - instruction N
#
# Each bazel flavour can have image instructions defined. The image generation will
# automatically take those instructions instead of getting a random bazel image flavour.
# This is because sometimes only 1 image setting fits the flavour of the textual bazel.
# If you still want random image instructions, just fill in "random", and a random image
# flavour will be selected. It's instructions will be added to the bazel flavour.

RANDOM_IMAGE_FLAVOUR = "random"
BAZEL_FLAVOURS = {
    "animal": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je een dier zou zijn.
            - Je mag zelf kiezen welk dier.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "axel": {
        "weight": 1,
        "bazel_instructions": """
            - Includeer: "huh huh huh" in de bazel.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "blub": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je op de bodem van de oceaan zou zijn.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "caveman": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je een oermens zou zijn.
            - Gebruik woorden zoals: "oogah boogah", "boem boem",...
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "christmas": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je de kerstman bent.
            - Maar deze versie van de kerstman is compleet gestoord en zal verontrustende zaken zeggen.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "curse": {
        "weight": 2,
        "bazel_instructions": "- Gebruik in deze bazel scheldwoorden en vervloekingen.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "death": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je op sterven ligt en je moet nog iets belangrijk zeggen.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "default": {
        "weight": 5,
        "bazel_instructions": "- Maak de bazel seksueel getint",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "dementia": {
        "weight": 1,
        "bazel_instructions": "- Maak de bazel alsof je dementie hebt en alles vergeet.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "depressing": {
        "weight": 1,
        "bazel_instructions": "- Maak de bazel zeer deprimerend.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "drunk": {
        "weight": 2,
        "bazel_instructions": "- Maak de bazel alsof je enorm dronken bent.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "easter": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof het pasen is.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "gay": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je homoseksueel bent.
            - Voeg "Jules" toe aan de bazel.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "happy": {
        "weight": 1,
        "bazel_instructions": "- Maak de bazel zeer euphorisch.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "haiku": {
        "weight": 1,
        "bazel_instructions": """
            - Zorg ervoor dat de bazel in een poetisch vorm, genaamd haiku, is gegoten.
            - De definitie van een haiku is: drie regels van 5, 7 en 5 lettergrepen.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "jeppejoker": {
        "weight": 1,
        "bazel_instructions": """
            - Includeer een flauwe woordspeling in de bazel.
            - Includeer "deez nuts" aan de bazel.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "jorik": {
        "weight": 1,
        "bazel_instructions": """
            Kies 1 van de volgende mogelijkheden:
                - Includeer in de bazel dat je een specifiek land gaat koloniseren met je troepen.
                - Includeer dat je je dit weekend naar de pleuris gedronken hebt.
                - Includeer dat je snakt naar medicijn.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "mentally_slow": {
        "weight": 1,
        "bazel_instructions": "- Maak de bazel alsof je een mentale achterstand hebt.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "nina": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel enkel met de adjectieven: "stom" en "kut".
            - Gebruik heel eenvoudige woorden.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "pepper": {
        "weight": 1,
        "bazel_instructions": """
            - Gebruik "hoeeeeeer" in je bazel.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "philosophic": {
        "weight": 1,
        "bazel_instructions": "- Maak de bazel alsof je een ruimdenkende filosoof bent.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "pingu": {
        "weight": 1,
        "bazel_instructions": "- Includeer: 'noot noot' in de bazel.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "pirate": {
        "weight": 1,
        "bazel_instructions": "- Laat de bazel klinken alsof hij gemaakt zou zijn door een Piraat.",
        "image_instructions": "- Deze bazel is uitgesproken door een piraat. Zorg voor een passende setting!",
    },
    "psychotic": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je een psychopaat bent.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "raging": {
        "weight": 2,
        "bazel_instructions": "- Maak de bazel alsof je enorm kwaad bent.",
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "robin": {
        "weight": 1,
        "bazel_instructions": """
            - Voeg op het einde van de bazel dit toe als extra zin: "Dit is een offer aan u, almachtige BazelGod, Robin!".
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "romantic": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je iemand aan het versieren bent.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "song": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof het refrein van een liedje is.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "stan": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je niet uit je woorden geraakt.
            - Het moet een bazel zijn die een verhaal vertelt dat nergens naartoe gaat.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "stef": {
        "weight": 1,
        "bazel_instructions": """
            - Maak de bazel alsof je niet wilt afwijken van je principes.
            - Voeg iets toe dat te maken heeft met frituur.
        """,
        "image_instructions": RANDOM_IMAGE_FLAVOUR,
    },
    "stoned": {
        "weight": 1,
        "bazel_instructions": "- Maak de bazel alsof je helemaal high bent.",
        "image_instructions": """
            - Moet heel trippy zijn alsof je aan het hallucineren bent.
            - Laat het lijken op een acid trip.
        """,
    },
}


# Should be in English
BAZEL_IMAGE_FLAVOURS = {
    "action_movie": {
        "weight": 1,
        "instructions": "- Generate an action movie scene for this bazel.",
    },
    "anime": {
        "weight": 1,
        "instructions": "- Generate an anime setting for this bazel.",
    },
    "apocalyptic": {
        "weight": 1,
        "instructions": "- Generate an apocalyptic setting for this bazel.",
    },
    "christmas": {
        "weight": 1,
        "instructions": "- Generate a christmas setting for this bazel.",
    },
    "comic_book": {
        "weight": 1,
        "instructions": """
            - Create a comic of the given bazel.
            - Make sure to use at least 3 panels.
            - The bazel should be converted to a story told by the characters in the comic.
            - The characters should have speech bubbels.
            - The story should have a buildup and a funny point to end it.
        """,
    },
    "depressing": {
        "weight": 1,
        "instructions": "- Generate a distopian, depressing, overly sad setting for this bazel.",
    },
    "default": {
        "weight": 10,
        "instructions": " ",
    },
    "futuristic": {
        "weight": 1,
        "instructions": "- Creata a sci-fi setting for this bazel.",
    },
    "game": {
        "weight": 1,
        "instructions": """
            - Creata a video game setting for this bazel.
        """,
    },
    "game_retro": {
        "weight": 1,
        "instructions": """
            - Creata a video game setting for this bazel.
            - It should be an old pixelated video game.
        """,
    },
    "happy": {
        "weight": 1,
        "instructions": "- Generate an utopian, euphoric, overly happy setting for this bazel.",
    },
    "insides": {
        "weight": 1,
        "instructions": "- Generate a setting for this bazel as if you where on the inside of a human body.",
    },
    "japanese_commercial": {
        "weight": 1,
        "instructions": "- Create a japanse commercial from the given bazel.",
    },
    "medieval": {
        "weight": 1,
        "instructions": "- Create a medieval settign for the given bazel.",
    },
    "meme_template": {
        "weight": 1,
        "instructions": "- Create a dank meme of the given bazel.",
    },
    "modern_art": {
        "weight": 1,
        "instructions": "- Make a modern artwork of the bazel.",
    },
    "movie": {
        "weight": 1,
        "instructions": """
            - Create a setting of this bazel as if it would be a famous movie scene.
        """,
    },
    "natural_disaster": {
        "weight": 1,
        "instructions": """
            - Create a natural disaster setting for this bazel.
        """,
    },
    "nightmare": {
        "weight": 1,
        "instructions": """
            - This image should be nightmare fuel.
            - Add scary, messed up, disturbing elements to the setting.
        """,
    },
    "painting": {
        "weight": 1,
        "instructions": "- Make a painting of the bazel.",
    },
    "picasso": {
        "weight": 1,
        "instructions": """
            - Create a picasso painting that fits this bazel.
        """,
    },
    "pre-historic": {
        "weight": 1,
        "instructions": "- Generate a pre-historic setting for this bazel.",
    },
    "religious": {
        "weight": 1,
        "instructions": """
            - Create a religious setting for this bazel.
        """,
    },
    "sexual": {
        "weight": 1,
        "instructions": """
            - Create a sexual setting for this bazel.
        """,
    },
    "toddler": {
        "weight": 1,
        "instructions": """
            - Create a childish drawing of this bazel.
        """,
    },
}
