"""Module for the bazelbot"""

import os
import logging
import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv

from src import bazels_controller
from src import bazels_repo
from src.custom_types import BazelType
from src.utils import configure_logging

# Load in .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MESSAGE_LIMIT = int(os.getenv("MESSAGE_LIMIT"))
NUM_THREADS = int(os.getenv("NUM_THREADS"))
OLLAMA_REQUEST_TIMEOUT = int(os.getenv("OLLAMA_REQUEST_TIMEOUT"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

# Set up logging
discord.utils.setup_logging()
configure_logging()
logger = logging.getLogger(__name__)

# Set up the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


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

        bazels_controller.populate_database(messages)
    except Exception as exc:
        logger.error(f"Something went wrong trying to fetch the existing bazels: {exc}")

    logger.info("Ready to BAZEL!")


# Error handling for command not found
@bot.event
async def on_command_error(ctx, error):
    """Error handling function"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Command not found! Try `!help` for a list of available commands."
        )


# Core commands
@bot.command(name="bazel")
@cooldown(1, 60, BucketType.user)
async def bazel(ctx):
    """Generate a bazel"""
    # Generate the bazel
    try:
        new_bazel = bazels_controller.generate_bazel()

        # Return the answer to the discord channel
        await ctx.send(new_bazel)
    except Exception as exc:
        # Provide error logging
        logger.error(f"Something went wrong while generating the bazel: {exc}")
        await ctx.send(f"OOPSIE WOOPSIE EEN ERROR: {exc}")


@bot.command(name="cumstom_bazel")
@cooldown(1, 60, BucketType.user)
async def custom_bazel(ctx, *, user_context):
    """Usage: !cumstom_bazel <type_your_input_here>"""
    # Generate custom bazel
    try:
        new_custom_bazel = bazels_controller.generate_bazel(
            user_context=user_context, bazel_type=BazelType.CUSTOM
        )

        # Return the answer to the discord channel
        await ctx.send(new_custom_bazel)
    except Exception as exc:
        # Provide error logging
        logger.error(f"Something went wrong while generating the custom bazel: {exc}")
        await ctx.send(f"OOPSIE WOOPSIE EEN ERROR: {exc}")


@bot.command(name="update_bazels")
@cooldown(1, 5, BucketType.user)
async def update_bazel(ctx):
    """Update the saved bazels"""
    # Retrieve all bazels from the channel and store them in our db
    try:
        channel = bot.get_channel(CHANNEL_ID)

        messages = [message async for message in channel.history(limit=MESSAGE_LIMIT)]

        amount_of_bazels = bazels_controller.populate_database(messages)

        await ctx.send(
            f"Added {amount_of_bazels} bazels, there are now {bazels_repo.count()} bazels stored"
        )
    except Exception as exc:
        logger.error(f"Something went wrong trying to fetch the existing bazels: {exc}")
        await ctx.send(f"Updating the bazels failed: {exc}")


# Basic commands
@bot.command(name="klets_bots")
@cooldown(1, 5, BucketType.user)
async def klets(ctx):
    """klets the bot"""
    logger.info("Petsing the bot...")
    response = "auw! 🤕"
    await ctx.send(response)


@bot.command(name="klets")
@cooldown(1, 5, BucketType.user)
async def klets_someone(ctx, name):
    """klets someone: !klets_someone <name>"""
    logger.info(f"Petsing {name}...")
    response = f"Hierzie {name} een klets!"
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
