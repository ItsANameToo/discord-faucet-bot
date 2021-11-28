import datetime
import discord
import logging
import os

from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
logger.add("logs/discordbot.log", backtrace=True, rotation="50 MB", compression="zip")
logger.info("Logger initialized")


# Intercept default logging data and pipe to Loguru: https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
# Discord.py for example uses default logging systems: https://discordpy.readthedocs.io/en/latest/logging.html
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

# level = 0 will show everything, can be useful for debugging
logging.basicConfig(handlers=[InterceptHandler()], level=20)

initial_extensions = [
    'cogs.faucet'
]

def get_prefix(bot, message):
    if "PREFIX" in os.environ:
        return os.getenv("PREFIX")
    return "!"


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name} !")
    await bot.change_presence(activity=discord.Game(name=f"!help"))


@bot.event
async def on_command_error(ctx, error):
    logger.exception(error)
    if isinstance(error, commands.CommandOnCooldown):
        formatted_date = str(datetime.timedelta(seconds=error.retry_after)).split(".")[0]
        await ctx.send(f"You are on a cooldown for this command, {formatted_date} left until you can use it again")
    if isinstance(error, commands.CommandNotFound):
        return
    # re-raise the error so all the errors will still show up in console
    raise error


@logger.catch
def main():
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(os.getenv("DISCORD_PRIVATE_KEY"), bot=True, reconnect=True)


if __name__ == '__main__':
    main()