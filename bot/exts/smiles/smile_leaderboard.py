import json
from collections import defaultdict
from typing import Optional, Union

from discord import Embed, Emoji, Member, PartialEmoji, Reaction, User, utils
from discord.enums import ChannelType
from discord.ext import commands
from discord.ext.commands.context import Context
from discord_slash import SlashContext, cog_ext
from loguru import logger

from bot import constants

from ...util.checks import is_jordan


class SmileLeaderboard(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.reaction_counts = self.get_initial_reaction_counts()

  def get_initial_reaction_counts(self):
    try:
      with open('./data/leaderboard.json', 'r') as f:
        d = {int(k): v for k, v in json.load(f).items()}
        print(f"Saved scores: {d}")
        return defaultdict(int, d)
    except FileNotFoundError:
      return defaultdict(int)

  def save_reaction_counts(self):
    with open('./data/leaderboard.json', 'w') as f:
      json.dump(self.reaction_counts, f)

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction: Reaction, user: Union[Member,
                                                                  User]):
    if reaction.message.channel.type == ChannelType.private:
      return

    emoji: Union[Emoji, PartialEmoji, str] = reaction.emoji
    emoji_name: Optional[str] = emoji.name

    if 'smile' in emoji_name:
      logger.info(f'Adding smile for {user.name}#{user.discriminator}')
      self.reaction_counts[user.id] += 1
      self.save_reaction_counts()
      logger.info(self.reaction_counts)

  @commands.Cog.listener()
  async def on_reaction_remove(self, reaction: Reaction, user: Union[Member,
                                                                     User]):
    if reaction.message.channel.type == ChannelType.private:
      return
    emoji: Union[Emoji, PartialEmoji, str] = reaction.emoji
    emoji_name: Optional[str] = emoji.name

    if 'smile' in emoji_name:
      logger.info(f'Removing smile for {user.name}#{user.discriminator}')
      self.reaction_counts[user.id] -= 1
      self.save_reaction_counts()
      logger.info(self.reaction_counts)

  @commands.command(
      aliases=['lb'],
      help="Get the top 10 smilers",
  )
  async def leaderboard(self, ctx: Context):
    """Send an embed with the current top 10 smilers and their number of smiles

    Args:
        ctx (Context): Invocation context
    """

    d = {'fields': [], 'color': 0x5A8041}
    for i, (user_id, count) in enumerate(
        sorted(self.reaction_counts.items(),
               key=lambda item: item[1],
               reverse=True)):
      if i < 10:
        d['fields'].append({
            'name': (await self.bot.fetch_user(user_id)).name,
            'value': f'**{count}** smiles'
        })
      else:
        break

    embed = Embed.from_dict(d)

    if not d['fields']:
      await ctx.send('None yet')
    else:
      await ctx.send(embed=embed)

  @cog_ext.cog_slash(name="leaderboard",
                     description="Smilers",
                     guild_ids=[constants.MACS_GUILD_ID])
  async def leaderboard_slash(self, ctx: SlashContext):
    """Send an embed with the current top 10 smilers and their number of smiles

    Args:
        ctx (Context): Invocation context
    """

    d = {'fields': [], 'color': 0x5A8041}
    for i, (user_id, count) in enumerate(
        sorted(self.reaction_counts.items(),
               key=lambda item: item[1],
               reverse=True)):
      if i < 10:
        d['fields'].append({
            'name': (await self.bot.fetch_user(user_id)).name,
            'value': f'**{count}** smiles'
        })
      else:
        break

    embed = Embed.from_dict(d)

    if not d['fields']:
      await ctx.send('None yet')
    else:
      await ctx.send(embed=embed)

  @commands.command(aliases=['m'], help='Check your smiles')
  async def me(self, ctx: Context):
    """Check your score

    Args:
        ctx (Context): Invocation context
    """
    author: Union[User, Member] = ctx.author
    await ctx.send(
        f"You have smiled **{self.reaction_counts[author.id]}** times")

  @cog_ext.cog_slash(name="me",
                     description="Count your smiles",
                     guild_ids=[constants.MACS_GUILD_ID])
  async def me_slash(self, ctx: SlashContext):
    """Check your score

    Args:
        ctx (Context): Invocation context
    """
    author: Union[User, Member] = ctx.author
    await ctx.send(
        f"You have smiled **{self.reaction_counts[author.id]}** times")

  @commands.command(aliases=['s'], help='Check someone elses smiles')
  async def score(self, ctx: Context, user_id: int):
    """Check someone elses score

    Args:
        ctx (Context): Invocation context
    """
    user = await self.bot.fetch_user(user_id)
    await ctx.send(
        f"{user.name} has smiled **{self.reaction_counts[user.id]}** times")

  @cog_ext.cog_slash(name="score",
                     description="Count someones smiles",
                     guild_ids=[constants.MACS_GUILD_ID])
  async def score_slash(self, ctx: SlashContext, user_id: str):
    """Check someone elses score

    Args:
        ctx (Context): Invocation context
    """
    user = await self.bot.fetch_user(int(user_id))
    await ctx.send(
        f"{user.name} has smiled **{self.reaction_counts[user.id]}** times")

  @is_jordan()
  async def set_score(self, ctx: Context, user_id: int, score: int):
    self.reaction_counts[user_id] = score

    user = await self.bot.fetch_user(user_id)
    await ctx.send(f"Set {user.name}'s score to {score}")
