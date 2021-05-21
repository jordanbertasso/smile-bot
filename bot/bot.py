from discord import Embed, Intents
from discord.ext import commands
from loguru import logger

from . import constants
from .exts.smiles.smile_leaderboard import SmileLeaderboard


class Bot(commands.Bot):
  def __init__(self) -> None:
    intents = Intents.default()
    intents.members = True
    intents.presences = True

    super().__init__(command_prefix=constants.PREFIX, intents=intents)
    self.add_cog(SmileLeaderboard(self))

  def run(self) -> None:
    """Run the bot with the token in constants.py/.env ."""
    logger.info("Starting bot")
    if constants.TOKEN is None:
      raise EnvironmentError(
          "token value is None. Make sure you have configured the TOKEN field in .env"
      )
    super().run(constants.TOKEN)

  async def on_ready(self) -> None:
    """Ran when the bot has connected to discord and is ready."""
    logger.info("Bot online")
