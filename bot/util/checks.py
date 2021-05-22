from .. import constants
from discord.ext import commands

def is_jordan(ctx):
  def predicate(ctx):
    return ctx.message.author.id == constants.JORDAN_ID
  return commands.check(predicate)
