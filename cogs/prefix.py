from discord import Guild
from discord.ext.commands import Cog, Context, command
from bot import CovidBot
import utils


class Prefix(Cog):
    def __init__(self, bot: CovidBot):
        self.bot = bot
        self.db = bot.pickle_db
        self.logger = bot.get_logger(self)

        self.logger.info("initialized")
    
    @command(aliases=["접두사설정"])
    @utils.server_command
    @utils.guild_permission("서버관리자만 접두사를 변경할 수 있습니다.")
    async def setprefix(self, ctx: Context, *args):
        if len(args) == 0:
            await ctx.send(f"명령어 사용법 : ``{ctx.prefix}접두사설정 !``")
        guild: Guild = ctx.guild
        prefix = " ".join(args)
        self.db["covid19"]["prefix"].update_one({"_id": guild.id}, {
            "$set": {
                "prefix": prefix
            }
        }, upsert=True)
        await ctx.send(f"{prefix}(으)로 접두사를 변경했습니다. ``{prefix}도움``과 같이 사용하실 수 있습니다.")
    
    @command(aliases=["접두사초기화"])
    @utils.server_command
    @utils.guild_permission("서버관리자만 접두사를 변경할 수 있습니다.")
    async def resetprefix(self, ctx: Context, *args):
        guild: Guild = ctx.guild
        self.db["covid19"]["prefix"].remove({"_id": guild.id})
        await ctx.send("접두사를 초기화 했습니다. ``!도움``과 같이 사용하실 수 있습니다.")
        


def setup(bot: CovidBot):
    bot.add_cog(Prefix(bot))
