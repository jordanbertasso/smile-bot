from discord import Reaction, User, Member, Emoji, PartialEmoji, Embed
from collections import defaultdict
from typing import Optional, Union
from discord.ext import commands
from discord.ext.commands.context import Context
from loguru import logger


class SmileLeaderboard(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.reaction_counts = defaultdict(int)

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction: Reaction, user: Union[Member,
                                                                  User]):
    emoji: Union[Emoji, PartialEmoji, str] = reaction.emoji
    emoji_name: Optional[str] = emoji.name

    if 'smile' in emoji_name:
      logger.info(f'Adding smile for {user.name}#{user.discriminator}')
      self.reaction_counts[user.id] += 1
      logger.info(self.reaction_counts)

  @commands.Cog.listener()
  async def on_reaction_remove(self, reaction: Reaction, user: Union[Member,
                                                                     User]):
    emoji: Union[Emoji, PartialEmoji, str] = reaction.emoji
    emoji_name: Optional[str] = emoji.name

    if 'smile' in emoji_name:
      logger.info(f'Removing smile for {user.name}#{user.discriminator}')
      self.reaction_counts[user.id] -= 1
      logger.info(self.reaction_counts)

  @commands.command(aliases=['lb'])
  async def leaderboard(self, ctx: Context):

    d = {'fields': []}
    for user_id, count in self.reaction_counts.items():
      d['fields'].append({
          'name': (await self.bot.fetch_user(user_id)).name,
          'value': f'**{count}** smiles'
      })

    embed = Embed.from_dict(d)

    if not d['fields']:
      await ctx.send('None yet')
    else:
      await ctx.send(embed=embed)
