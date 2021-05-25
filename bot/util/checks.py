from discord.ext import commands
from discord.ext.commands.context import Context

from .. import constants


def is_jordan():
  def predicate(ctx: Context):
    return ctx.message.author.id == constants.JORDAN_ID

  return commands.check(predicate)


def in_botspam(ctx: Context):
  return ctx.channel.id in (constants.BOT_SPAM_CHANNEL_ID,
                            constants.DEV_BOT_SPAM_CHANNEL_ID)
