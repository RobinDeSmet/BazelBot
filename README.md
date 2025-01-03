# 🎉 BazelBot 🤖

BazelBot is a Discord bot designed to generate nonsensical gibberish for entertainment purposes, guaranteed to bring laughter to you and your friends! 😂

#### ✨ Project Goal

The goal of this project is to harness the power of large language models (LLMs) to create humorous, absurd, and downright silly content. By generating random gibberish, BazelBot transforms ordinary text into something hilariously unexpected! 🤪

#### 🛠️ How It Works
- 📥 Message Collection: BazelBot pulls a set number of messages from a designated Discord text channel.
- 📦 Data Storage: These messages are saved in a database for future hilarity.
- 🎲 Bazel Generation: When a user requests a "bazel," the bot selects K random messages from the database and uses them as inspiration to generate a gibberish sentence.

Each bazel is a unique blend of randomness and creativity, making it perfect for a good chuckle with friends! 🤩

## Environment Variables

The following environment variables need to be configured for the application to function properly:

| Variable Name              | Description                                                                                 | Default Value                                       |
|----------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------------|
| `BOT_TOKEN`                | Discord bot token for authentication.                                                      | `YOUR_BOT_TOKEN`                                 |
| `CHANNEL_ID`               | Discord channel ID to pull messages for generating gibberish.                              | `YOUR_CHANNEL_ID`                             |
| `DB_CONNECTION_URL`        | Database connection URL for connecting to the PostgreSQL database.                         | `postgresql+psycopg2://postgres:postgres@localhost:5432/bazelbot_db` |
| `MAX_BAZEL_LENGTH`         | Maximum length of a bazel (in words).                                                      | `30`                                             |
| `MESSAGE_LIMIT`            | Number of messages to pull from the channel.                                               | `10000`                                          |
| `RATE_LIMIT`               | Minimum time (in seconds) between bazel requests by a user.                                      | `10`                                             |
| `MAX_BAZELS_IN_CONTEXT`    | Maximum number of bazels allowed in a single context window.                                       | `25`                                             |
| `GEMINI_API_KEY`           | API key for the Gemini API.                                                                | `YOUR_GEMINI_API_KEY`                            |
| `GEMINI_MODEL`             | Gemini model.                                              | `gemini-2.0-flash-exp`                           |
| `BAZEL_IMAGE_WIDTH`             | The width of the generated bazel image.                                              | `350`                           |
| `BAZEL_IMAGE_HEIGHT`             | The height of the generated bazel image.                                              | `350`                           |
| `BAZEL_IMAGE_SAVE_PATH`             | The path to the directory where the generated bazel image will be stored.                                             | `src/data`                           |


## Maintainers

* Clone the repo and make sure you have docker and poetry installed
* Navigate to the root directory of the project
* Run `poetry install`
* Create and fill in the required details in the `.env` file. You can copy this from `.env.template`
  * You will have to [create a discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) and give him admin rights.
    In the developer portal, you can retrieve the bot token.
  * Activate [developer mode](https://support-dev.discord.com/hc/en-us/articles/360028717192-Where-can-I-find-my-Application-Team-Server-ID) in discord.
    Then, copy the ID of a text channel of your choice. This channel will be used as the inspiration for the bot.
* Run `make up`
* Run `make run` to run the bot locally


## Testing
We have 2 types of tests, one that require an LLM and one that does not.
Naturally, only the tests will be run that do not require the LLM.
They are excluded by a custom marking: `@pytest.mark.llm`.

* If you do not have the postgres container up and running: `make test-up`
* If you want to run the normal test suite, run `make test`
* If you want to run the llm test suite, run `make test-llm`
