"""Module for the bazelbot"""

import os
import logging
import random
import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv

from llama_index.llms.ollama import Ollama

import bazels_repo

# Load in .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LLM = os.getenv("LLM")
MESSAGE_LIMIT = int(os.getenv("MESSAGE_LIMIT"))
NUM_THREADS = int(os.getenv("NUM_THREADS"))
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
    model=LLM,
    request_timeout=float(OLLAMA_REQUEST_TIMEOUT),
    base_url=OLLAMA_BASE_URL,
    num_threads=NUM_THREADS,
)


# On ready
@bot.event
async def on_ready():
    """This function will retrieve all the bazels in the channels to fill the database"""
    logger.info(f"{bot.user.name} has connected to Discord!")
    logger.info("Populating the bazel context database...")

    # Retrieve all bazels from the channel and store them in our db
    try:
        channel = bot.get_channel(CHANNEL_ID)

        messages = [message async for message in channel.history(limit=MESSAGE_LIMIT)]

        if len(messages) == bazels_repo.count():
            logger.info("DB already populated with bazels!")

        else:
            new_bazels = []
            for message in messages:
                new_bazels.append(message.content)

            # Add bazels to the database
            bazels_repo.add_bazels(new_bazels)
    except Exception as exc:
        logger.error(f"Something went wrong trying to fetch the existing bazels: {exc}")

    logger.info("Ready to BAZEL!")


# Error handling
@bot.event
async def on_command_error(ctx, error):
    """Error handling function"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Command not found! Try `!help` for a list of available commands."
        )


# Core commands
@bot.command(name="test_bazel")
@cooldown(1, 60, BucketType.user)
async def bazel(ctx):
    """Generate a bazel"""
    # Generate the bazel context
    logger.info("Generating the bazel context")
    bazel_context = ""
    amount_of_bazels = bazels_repo.count()

    try:
        random_numbers = random.sample(range(0, amount_of_bazels), 10)

        for i in random_numbers:
            bazel_context += f"- {bazels_repo.get(i).content}\n"

    except Exception as exc:
        logger.error(f"The bazel context could not be generated: {exc}")

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


@bot.command(name="test_cumstom_bazel")
@cooldown(1, 60, BucketType.user)
async def custom_bazel(ctx, *, user_input):
    """Generate a bazel based on user input.
    Usage: !cumstom_bazel <type_your_input_here>
    """
    # Check for user input
    user_context = ""
    try:
        if user_input:
            logger.info(f"User input detected: {user_input}")
            user_context += f"You have to include this piece of text: {user_input}"
    except Exception as exc:
        logger.info(f"Could not parse user input: {exc}")

    # Generate the bazel context
    logger.info("Generating the bazel context")
    bazel_context = ""
    amount_of_bazels = bazels_repo.count()

    try:
        random_numbers = random.sample(range(0, amount_of_bazels), 10)

        for i in random_numbers:
            bazel_context += f"- {bazels_repo.get(i).content}\n"

    except Exception as exc:
        logger.error(f"The bazel context could not be generated: {exc}")

    # Format the prompt
    logger.info("Formatting the prompt")

    question = f"""
            QUESTION: Combine small parts of the context below to generate a sentence but do not make it long (max 20 words).
            The goal is to create a new sentence that does not make sense. It can be sexual, and you can be creative!
            FORMAT OF THE ANSWER: ----- <the generated sentence> -----
            {user_context}
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


@bot.command(name="test_update_bazels")
@cooldown(1, 5, BucketType.user)
async def update_bazel(ctx):
    """Update the saved bazels"""
    # Retrieve all bazels from the channel and store them in our db
    try:
        channel = bot.get_channel(CHANNEL_ID)

        messages = [message async for message in channel.history(limit=MESSAGE_LIMIT)]

        if len(messages) == bazels_repo.count():
            logger.info("DB already populated with bazels!")
        else:
            new_bazels = []
            for message in messages:
                new_bazels.append(message.content)

            # Add bazels to the database
            bazels_repo.add_bazels(new_bazels)

        await ctx.send(
            f"Bazels geupdated, there are now {bazels_repo.count()} bazels stored"
        )
    except Exception as exc:
        logger.error(f"Something went wrong trying to fetch the existing bazels: {exc}")
        await ctx.send(f"Updating the bazels failed: {exc}")


# Basic commands
@bot.command(name="klets")
@cooldown(1, 5, BucketType.user)
async def klets(ctx):
    """klets"""
    logger.info("Petsing the bot...")
    response = "auw! 🤕"
    await ctx.send(response)


@bot.command(name="stout")
@cooldown(1, 5, BucketType.user)
async def stout(ctx):
    """stout"""
    logger.info("Telling the bot he has been bad...")
    response = "Sorry papi 😢"
    await ctx.send(response)


@bot.command(name="braaf")
@cooldown(1, 5, BucketType.user)
async def braaf(ctx):
    """braaf"""
    logger.info("Telling the bot he is a good LLM...")
    response = "*Wiggles LLM-tail* 🙂"
    await ctx.send(response)


# Run the bot
bot.run(BOT_TOKEN)
