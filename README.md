# BazelBot
This is a discord bot that generates non-sensical gibberish for entertainment purposes.
The goal of this project is to use the power of LLM's to give my friends a good chuckle.

The main idea is that the bot will pull a certain amount of messages from a discord text channel.
He will store those messages in a database. When the user wants to use the `!bazel` command,
the bot will take 10 random messages from the database and generate a gibberish sentence, based on those messages.

# Deploy
* Clone the code in a directory of your choosing.
* Navigate to the root directory of this project.
* Create and fill in the required details in the `.env` file. You can copy this from `.env.template`
  * You will have to create a discord bot by following these steps: https://discordpy.readthedocs.io/en/stable/discord.html (Make sure to give him admin privileges)
    In the developer portal, you can retrieve the bot token
  * Activate developer mode in discord: https://support-dev.discord.com/hc/en-us/articles/360028717192-Where-can-I-find-my-Application-Team-Server-ID
    and copy the ID of a text channel of your choice. This channel will be used as the inspiration for the bot.
  * Also make sure that the `DB_CONNECTION_URL` in the `.env` file matches the `sqlalchemy.url` parameter in the `alembic.ini` file:
  ```
    sqlalchemy.url = postgresql+psycopg2://postgres:postgres@bazelbot-db-1:5432/bazelbot_db
  ```
* To fascilitate the bot, we will use `ollama` and have the `gurubot/llama3-guru-uncensored:latest` model installed. This is a specific model that is uncensored, so it is able to generate the NSFW content that we need. The model will be pulled using the `ollama-pull` service in docker compose. The only thing that is needed, is to enable the `NVIDIA Container Toolkit` to be able to use the GPU's power. You can install it by following the steps in this link: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

* If you do not have an Nvidia GPU or a GPU installed you can comment out the following lines in the `docker-compose.yaml`.
Note that this will tremendously slow down the bot!
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
* Finally, execute `docker compose up -d` in the root directory of the project. Now you should be good to go!


# Dev

* Clone the repo and make sure you have docker and poetry installed
* Navigate to the root directory of the project
* Run `poetry install`
* Create and fill in the required details in the `.env` file. You can copy this from `.env.template`
  * You will have to create a discord both by following these steps: https://discordpy.readthedocs.io/en/stable/discord.html (Make sure to give him admin privileges)
    In the developer portal, you can retrieve the bot token
  * Activate developer mode in discord: https://support-dev.discord.com/hc/en-us/articles/360028717192-Where-can-I-find-my-Application-Team-Server-ID
    and copy the ID of a text channel of your choice. This channel will be used as the inspiration for the bot.
  * Also make sure that the `DB_CONNECTION_URL` in the `.env` file matches the `sqlalchemy.url` parameter in the `alembic.ini` file:
  ```
    sqlalchemy.url = postgresql+psycopg2://postgres:postgres@localhost:5433/bazelbot_db
  ```
* Make sure you have ollama installed on your system: `curl -fsSL https://ollama.com/install.sh | sh` and make sure that the ollama service is running: `systemctl start ollama`
* Install this model for ollama: `gurubot/llama3-guru-uncensored:latest`. Do this my running: `ollama pull gurubot/llama3-guru-uncensored:latest`
* Run `make test-up`
* Run `make run` to run the bot locally

* If you want to run the test suite, run `make test`


ENJOY BAZELING!

