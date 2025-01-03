# INFO:
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
# Bazel instructions are mandatory.

BAZEL_FLAVOURS = {
    "default": {
        "weight": 2,
        "bazel_instructions": "- Maak de bazel seksueel getint",
        "image_instructions": "random",
    },
    "trump": {
        "weight": 1,
        "bazel_instructions": "- Laat de bazel klinken alsof Donald Trump hem zou uitspreken",
        "image_instructions": "- Deze bazel is uitgesproken door president Donald Trump. Zorg voor een passende setting!",
    },
    "haiku": {
        "weight": 1,
        "bazel_instructions": """
            - Zorg ervoor dat de bazel in een poetisch vorm, genaamd haiku, is gegoten.
            - De definitie van een haiku is:  drie regels van 5, 7 en 5 lettergrepen.,
        """,
        "" "image_instructions": "random",
    },
}

BAZEL_IMAGE_FLAVOURS = {
    "default": {
        "weight": 1,
        "instructions": " ",
    },
    "anime": {
        "weight": 1,
        "instructions": "- Genereer een anime setting voor deze bazel.",
    },
    "nightmare": {
        "weight": 1,
        "instructions": """
            - Maak van deze bazel een met nachtmerries gevulde afbeelding.
            - Voeg enge, verschrikkelijke beelden en scenes toe voor deze bazel afbeelding.
        """,
    },
    "comic_book": {
        "weight": 1,
        "instructions": """
            - Maak een stripverhaal van deze bazel.
            - Zorg ervoor dat er minstens 3 panelen aanwezig zijn in de afbeelding.
            - De bazel moet wat verhalend worden met teksballonnen rond de characters.
            - Het verhaal moet een mooie opbouw hebben en eindigen met een grappige clou.
        """,
    },
    "modern_art": {
        "weight": 1,
        "instructions": "- Genereer een modern kunstwerk voor deze bazel.",
    },
    "meme_template": {
        "weight": 1,
        "instructions": "- Genereer een meme voor deze bazel.",
    },
    "happy": {
        "weight": 1,
        "instructions": "- Genereer een utopische, super happy setting voor deze bazel.",
    },
    "deprimerend": {
        "weight": 1,
        "instructions": "- Genereer een distopische, super neerslachtige setting voor deze bazel.",
    },
    "sexual": {
        "weight": 1,
        "instructions": "- Genereer een sexuele expliciete setting voor deze bazel.",
    },
    "christmas": {
        "weight": 1,
        "instructions": "- Genereer een kerstachtige setting voor deze bazel.",
    },
}
