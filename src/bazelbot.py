"""Module for the bazelbot"""

# TODO: Fix async issues with the bot: https://chatgpt.com/c/677126d1-e4ac-8012-ae0e-bad269144dc5
import os
import logging
import discord

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv

from src import bazels_controller
from src import bazels_repo
from src.custom_types import BazelType
from src.utils import configure_logging, create_image_save_path_from_bazel

# Load in .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MESSAGE_LIMIT = int(os.getenv("MESSAGE_LIMIT"))
RATE_LIMIT = int(os.getenv("RATE_LIMIT"))

# Set up logging
discord.utils.setup_logging()
configure_logging()
logger = logging.getLogger(__name__)

# Set up the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


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
            "Command not found! Try `/help_daddy` for a list of available commands."
        )


# Help command
@bot.command(name="help_daddy")
async def help(ctx):
    help_message = """**🤖 Hulpcommando's voor de bot!**
Jongens, jongens... weet je het nu nog niet? 😞
Hier zijn de commando's die je kan gebruiken:

📜 **Algemene commando's**
- `/help`
   : _Lijst van hulpcommando's._
- `/bazel`
   : _Genereer een bazel._
- `/bazel_pic`
   : _Genereer een bazel tesamen met een afbeelding van die bazel._
- `/cumstom_bazel <context>`
   : _Genereer een bazel die de gegeven context bevat._
- `/cumstom_bazel_pic <context>`
   : _Genereer een bazel die de gegeven context bevat, tesamen met een afbeelding van die bazel._
- `/update_bazels`
   : _Update de bazels in de database._

✋ **Interactie met de bot**
- `/klets_bots`
   : _De bot een mep verkopen._
- `/klets <object>`
   : _Iemand of iets een klets verkopen._

😇 **Gedrag van de bot**
- `/stout`
   : _Als de bot niet braaf is._
- `/braaf`
   : _Als de bot niet stout is._
"""
    logger.info("Supplying the help doctring...")
    await ctx.send(help_message)


# Core commands
@bot.command(name="bazel")
@cooldown(1, RATE_LIMIT, BucketType.user)
async def bazel(ctx):
    """Generate a bazel"""
    # Generate the bazel
    try:
        new_bazel = bazels_controller.generate_bazel()

        # Return the answer to the discord channel
        await ctx.send(new_bazel.text)
    except Exception as exc:
        # Provide error logging
        logger.error(f"Something went wrong while generating the bazel: {exc}")
        await ctx.send(f"OOPSIE WOOPSIE EEN ERROR: {exc}")


@bot.command(name="cumstom_bazel")
@cooldown(1, RATE_LIMIT, BucketType.user)
async def custom_bazel(ctx, *, user_context):
    """Generate custom bazel."""
    # Generate custom bazel
    try:
        new_custom_bazel = bazels_controller.generate_bazel(
            user_context=user_context, bazel_type=BazelType.CUSTOM
        )

        # Return the answer to the discord channel
        await ctx.send(new_custom_bazel.text)
    except Exception as exc:
        # Provide error logging
        logger.error(f"Something went wrong while generating the custom bazel: {exc}")
        await ctx.send(f"OOPSIE WOOPSIE EEN ERROR: {exc}")


@bot.command(name="bazel_pic")
@cooldown(1, 6 * RATE_LIMIT, BucketType.user)
async def bazel_with_image(ctx):
    """Generate a bazel with image."""
    # Generate the bazel
    try:
        new_bazel = bazels_controller.generate_bazel(generate_image=True)

        # Return the answer to the discord channel
        await ctx.send(new_bazel.text)

        # Send image to discord
        bazel_image_save_path = create_image_save_path_from_bazel(
            new_bazel.text_english
        )

        await ctx.send(file=discord.File(bazel_image_save_path))

        # Delete image locally
        bazel_image_save_path.unlink()
    except Exception as exc:
        # Provide error logging
        logger.error(f"Something went wrong while generating the bazel: {exc}")
        await ctx.send(f"OOPSIE WOOPSIE EEN ERROR: {exc}")


@bot.command(name="cumstom_bazel_pic")
@cooldown(1, 6 * RATE_LIMIT, BucketType.user)
async def custom_bazel_with_image(ctx, *, user_context):
    """Generate custom bazel with image."""
    # Generate custom bazel
    try:
        new_custom_bazel = bazels_controller.generate_bazel(
            generate_image=True, user_context=user_context, bazel_type=BazelType.CUSTOM
        )

        # Return the answer to the discord channel
        await ctx.send(new_custom_bazel.text)

        # Send image to discord
        bazel_image_save_path = create_image_save_path_from_bazel(
            new_custom_bazel.text_english
        )

        await ctx.send(file=discord.File(bazel_image_save_path))

        # Delete image locally
        bazel_image_save_path.unlink()
    except Exception as exc:
        # Provide error logging
        logger.error(f"Something went wrong while generating the custom bazel: {exc}")
        await ctx.send(f"OOPSIE WOOPSIE EEN ERROR: {exc}")


@bot.command(name="update_bazels")
@cooldown(1, RATE_LIMIT, BucketType.user)
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
@cooldown(1, 1, BucketType.user)
async def klets(ctx):
    """klets the bot"""
    logger.info("Petsing the bot...")
    response = "auw! 🤕"
    await ctx.send(response)


@bot.command(name="klets")
@cooldown(1, 1, BucketType.user)
async def klets_someone(ctx, name):
    """klets someone: !klets_someone <name>"""
    logger.info(f"Petsing {name}...")
    response = f"Hierzie {name} een klets!"
    await ctx.send(response)


@bot.command(name="stout")
@cooldown(1, 1, BucketType.user)
async def stout(ctx):
    """stout"""
    logger.info("Telling the bot he has been bad...")
    response = "Sorry papi 😢"
    await ctx.send(response)


@bot.command(name="braaf")
@cooldown(1, 1, BucketType.user)
async def braaf(ctx):
    """braaf"""
    logger.info("Telling the bot he is a good LLM...")
    response = "*Wiggles LLM-tail* 🙂"
    await ctx.send(response)


# Run the bot
bot.run(BOT_TOKEN)
