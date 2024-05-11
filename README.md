# BazelBot
This is a NSFW discord bot that generates non-sensical gibberish for entertainment purposes.
The goal of this project is to use the power of LLM's to give my friends a good chuckle.


# Set up
* Clone the code in a directory of your choosing.
* Navigate to the root directory of this project.
* Create and fill in the required details in the `.env` file. You can copy this from `.env.template`
* Make sure that the data directory has write permissions for non-root users. You can do this by running: `chmod 777 src/data`
* To fascilitate the bot, you will need `Ollama` and have the `gurubot/llama3-guru-uncensored:latest` model installed. This is a specific model that is uncensored, so it is able to generate the NSFW content that we need. The model will be pulled using the `ollama-pull` service in docker compose. The only thing that is needed, is to enable the `NVIDIA Container Toolkit` to be able to use the GPU's power. You can install it by following the steps in this link: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
* Normally, everything should be up and running after executing `docker compose up -d` in the root directory of the project.


If you do not have an Nvidia GPU or a GPU installed you can comment out the following lines in the `docker-compose.yaml`
```
services:
  server:
    build:
      context: .
    env_file:
      - .env
    ports:
      - 8000:8000
    volumes:
      - ./src/data:/app/src/data
    depends_on:
      ollama-pull:
          condition: service_completed_successfully
  ollama-pull:
    image: docker/genai:ollama-pull
    env_file:
      - .env
  ollama:
      image: ollama/ollama:latest
      ports:
        - "11434:11434"
      volumes:
        - ollama_volume:/root/.ollama
      # deploy:
      #  resources:
      #    reservations:
      #      devices:
      #        - driver: nvidia
      #          count: all
      #          capabilities: [gpu]
volumes:
  ollama_volume:
```
