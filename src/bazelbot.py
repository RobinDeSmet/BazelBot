import os
import discord
import logging
import csv
import random

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv

from llama_index.llms.ollama import Ollama

# Load in .env variables
load_dotenv()
BAZELS_FILE_PATH = os.getenv("BAZELS_FILE_PATH")
BOT_LLM = os.getenv("BOT_LLM")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_NAME = os.getenv("SERVER_NAME")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
OLLAMA_REQUEST_TIMEOUT = int(os.getenv("OLLAMA_REQUEST_TIMEOUT"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

# Set up logging
discord.utils.setup_logging()
logger = logging.getLogger(__name__)

# Set up the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Set up the LLM
llm = Ollama(
    model=BOT_LLM,
    request_timeout=float(OLLAMA_REQUEST_TIMEOUT),
    base_url=OLLAMA_BASE_URL,
)


# On ready
@bot.event
async def on_ready():
    """This function will retrieve all the bazels in the channels to fill the database"""
    logger.info(f"{bot.user.name} has connected to Discord!")

    # Retrieve all bazels from the channel
    try:
        channel = bot.get_channel(CHANNEL_ID)

        messages = [message async for message in channel.history(limit=10000)]

        # Write them to a CSV file
        with open(BAZELS_FILE_PATH, "w+", newline="") as csvfile:
            writer = csv.writer(csvfile)

            for message in messages:
                writer.writerow([message.content])

        logger.info(f"Retrieved {len(messages)} bazels from the server")
    except Exception as e:
        logger.error(f"Something went wrong trying to fetch the existing bazels: {e}")

    logger.info("Ready to BAZEL!")


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Command not found! Try `!help` for a list of available commands."
        )


# Core commands
@bot.command(name="bazel")
@cooldown(1, 60, BucketType.user)
async def bazel(ctx):
    # Generate the bazel context
    logger.info("Generating the bazel context")
    bazel_context = ""

    try:
        bazel_context = ""

        with open(BAZELS_FILE_PATH, "r") as csvfile:
            bazels = csv.reader(csvfile)

            bazels = [line for line in bazels]

            random_numbers = [random.randint(0, len(bazels)) for _ in range(10)]

            for i in random_numbers:
                bazel_context += f"- {bazels[i][0]}\n"

    except Exception as e:
        logger.error(f"The bazel context could not be generated: {e}")

    # Format the prompt
    logger.info("Formatting the prompt")

    question = f"""
            QUESTION: Combine small parts of the context below to generate a sentence but do not make it long (max 20 words).
            The goal is to create a new sentence that does not make sense. It can be sexual, and you can be creative!
            FORMAT OF THE ANSWER: ----- <the generated sentence> -----
            CONTEXT
            {bazel_context}
            """

    logger.info(question)

    # Generate the answer and format it
    answer = llm.complete(question)

    answer = str(answer).split("-----")[1].replace('"', " ")

    logger.info(answer)

    # Return the answer to the discord channel
    await ctx.send(answer)


@bot.command(name="update_bazels")
@cooldown(1, 5, BucketType.user)
async def bazel(ctx):
    # Retrieve all bazels from the channel
    try:
        channel = bot.get_channel(CHANNEL_ID)

        messages = [message async for message in channel.history(limit=10000)]

        # Write them to a CSV file
        with open(BAZELS_FILE_PATH, "w+", newline="") as csvfile:
            writer = csv.writer(csvfile)

            for message in messages:
                writer.writerow([message.content])

        logger.info(f"Retrieved {len(messages)} bazels from the server")

        await ctx.send(f"Bazels geupdated, there are now {len(messages)} bazels stored")
    except Exception as e:
        logger.error(f"Something went wrong trying to fetch the existing bazels: {e}")
        await ctx.send(f"Updating the bazels failed: {e}")


# Basic commands
@bot.command(name="klets")
@cooldown(1, 5, BucketType.user)
async def bazel(ctx):
    logger.info("Petsing the bot...")
    response = "auw! 🤕"
    await ctx.send(response)


@bot.command(name="stout")
@cooldown(1, 5, BucketType.user)
async def bazel(ctx):
    logger.info("Telling the bot he has been bad...")
    response = "Sorry papi 😢"
    await ctx.send(response)


@bot.command(name="braaf")
@cooldown(1, 5, BucketType.user)
async def bazel(ctx):
    logger.info("Telling the bot he is a good LLM...")
    response = "*Wiggles LLM-tail* 🙂"
    await ctx.send(response)


# Run the bot
bot.run(BOT_TOKEN)
