import pollinations as ai
from huggingface_hub import InferenceClient
from datetime import datetime

IMAGE_PATH = "./experiments/image-output-pollinations-nsfw"
TOKEN = "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"


def generate_img_pollinations(prompt: str, save_path: str):
    for i in range(5):
        model_obj = ai.ImageModel(model=ai.evil, seed="random", width=700, height=700)

        _image = model_obj.generate(
            prompt=prompt,
            save=True,
            file=save_path,
        )


def generate_img_with_diffuser(prompt: str, save_path):
    client = InferenceClient("prashanth970/flux-lora-uncensored", token=TOKEN)

    # output is a PIL.Image object
    image = client.text_to_image(prompt)
    image.save(save_path)


if __name__ == "__main__":
    # llm = get_llm(
    #     system_instruction="You need to convert a sentence to a detailed description that "
    #     "I can use to generate an image. "
    # )

    # response = llm.generate_content(
    #     "If Stan ever has a girlfriend, fumbling and tumbling in the upper ballsack of Nina."
    # )

    # print(response)

    prompts = [
        'image_title_bovenste_balzak_stan_nina**Image Description:**\n\n**Overall Tone:** Surreal, absurd, slightly uncomfortable, humorous (in a dark and ironic way).\n\n**Scene:** The image will not be a literal depiction of the sentence, but rather a visual metaphor for its themes. The scene will feel like a dream or a distorted memory.\n\n**Composition:** The scene will be dominated by abstract, organic shapes that suggest a human form but are not explicitly human. The focus will be on a central, bulbous, vaguely testicular form. This can be large and imposing, possibly a bit fleshy or textured, with an uneven surface. Colors will be muted and slightly unsettling. \n\n**Key Visual Elements:**\n\n*   **"Stan":** This will not be a recognizable person. Instead, depict him as a series of vaguely human-shaped forms. They will be smaller and less defined, appearing as if they are trying to maneuver or navigate around the central form. These could be made of a softer, more malleable material, like clay or play-doh. They\'ll appear awkward and clumsy, their bodies bent in unnatural ways.\n*   **"Nina":** She won\'t be a literal human female. She is represented by the central, bulbous form. It should be visually striking and oddly compelling. Think of a surreal anatomical structure, smooth in some places, with folds and creases in others. The color should be a slightly off-putting shade, possibly a pale, bruised pink or a dull grey-purple, suggesting fragility and perhaps discomfort. It\'s not overtly sexual, but rather an abstract representation of a body part that is both familiar and strange. \n*  **Movement and Action:** The "Stans" will appear to be awkwardly moving and tumbling around and partially inside the main form. This will be conveyed through the dynamic poses and slightly blurred edges, creating the impression of fumbling, chaotic movement. Use overlapping elements to suggest the idea of being \u201cinside\u201d or struggling within.\n*   **Lighting and Color:** The lighting should be soft and diffused, creating a dreamy atmosphere. Avoid harsh shadows and stark contrasts. The color palette should be muted and slightly desaturated. Use colors like pale pinks, soft purples, light grays, and muted greens or blues. A touch of slightly unsettling yellow could be introduced for an added layer of discomfort. The colors contribute to the surreal and slightly disturbing tone of the image.\n*   **Texture:** Incorporate a mix of textures to add depth to the image. The larger form ("Nina") can have a mix of smooth and rough surfaces. "Stan" should have a less defined texture, with an almost malleable quality, perhaps suggesting a soft or squishy feel.\n* **Background:** The background should be kept simple and abstract, perhaps a soft gradient or a subtle, non-distracting pattern. Don\'t add any specific contextual elements that would ground the scene in a particular location. The lack of a clear background enhances the surreal and dreamlike nature of the image.\n\n**Overall Effect:** The goal is to create an image that is bizarre, thought-provoking, and slightly unsettling. It should visually translate the awkwardness and absurdity of the original sentence without being explicit. The image should spark curiosity and perhaps a touch of discomfort, making the viewer question what they are seeing and why.\n\n'
    ]

    # prompts = [
    #     "If Stan ever has a girlfriend, fumbling and tumbling in the upper ballsack of Nina.",
    #     "That croacks like my dick under the weight of your mother."
    #     "The morning wood inspection of my anus sips DNA to the outside.",
    #     "I don't fuck my mates, I fuck the long neck of my mates.",
    #     "Because Hitler does not do Kung Fu, I will drink milk from the tiramikoe.",
    #     "The red speedo of my twelve dicks fits perfectly on his ass.",
    #     "I had promised my penis that I won't punish him because I was in bed with Pepper.",
    #     "The goat shit oozes out of Hitlers balls in the 100 year old pita.",
    #     "I'm horrific Stan, open your pants!",
    #     "The portal to hell is situated in my underpants.",
    #     "My parent's are dead, so I will fuck a bat.",
    # ]

    results = ""

    for prompt in prompts:
        # Rephrase prompt
        file_path_prefix = f"./experiments/{prompt[:25]}"
        diffuser_path = file_path_prefix + "-diffuser.jpg"
        pollinations_path = file_path_prefix + "-pollinations.jpg"
        try:
            start = datetime.now()
            generate_img_with_diffuser(prompt, diffuser_path)
            end = datetime.now()
            results += f"Diffuser generated: {prompt} in {end-start}s"
        except Exception as e:
            print(
                f"Something went wrong in the diffuser while generating: {prompt}: {e}"
            )
        try:
            start = datetime.now()
            generate_img_pollinations(prompt, pollinations_path)
            end = datetime.now()
            results += f"Pollinations generated: {prompt} in {end-start}s"
        except Exception as e:
            print(
                f"Something went wrong in the pollinations while generating: {prompt}: {e}"
            )

    with open("./experiments/results.txt", "w") as f:
        f.write(results)
