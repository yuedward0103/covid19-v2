from discord import Game, Message, Embed
from discord.ext.commands import AutoShardedBot, Context
from discord.ext.commands.errors import CommandNotFound
import logging
import os
import random
import traceback
from db import PickleDB

class CovidBot(AutoShardedBot):
    name = "CovidBot"
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("command_prefix", get_command_prefix)
        super().__init__(*args, help_command=None, **kwargs)

        self.logger = logging.getLogger(self.name or self.__class__.__name__)
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] (%(name)s: %(filename)s:%(lineno)d) > %(message)s")

        handler = logging.StreamHandler()
        handler.setLevel('DEBUG')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.setLevel('DEBUG')

        self.pickle_db = PickleDB()

    def get_logger(self, cog):
        name = cog.__class__.__name__
        logger = logging.getLogger(name and self.name + "." + name or self.name or self.__class__.__name__)
        logger.setLevel('DEBUG')
        return logger

    def run(self, *args, **kwargs):
        self.logger.info("Starting bot")
        super().run(*args, **kwargs)

    async def on_ready(self):
        self.logger.info("Bot ready")
        await self.change_presence(
            activity=Game("!도움으로 명령어 확인")
        )

    async def on_command_error(self, ctx: Context, e: Exception):
        if isinstance(e, CommandNotFound):
            await super().on_command_error(ctx, e)
            return
        logChannel = os.getenv("LOG_CHANNEL")
        if logChannel:
            t = "%x" % random.randint(0, 16**8)
            embed = Embed(
                title="⚠️ 오류가 발생했습니다.",
                description="[팀 피클 공식 포럼](http://forum.tpk.kr)에 버그를 제보해주세요.\n" \
                    f"코드 ``{t}``를 알려주시면 더 빠른 처리가 가능합니다.",
                color=0xffff00
            )
            await ctx.send(embed=embed)
            await (await self.fetch_channel(logChannel)).send(
                ("Code: {t}\n" \
                    "Requester: {requesterStr}#{requesterS}({requesterNum})\n" \
                    "Message: {message}\n" \
                    "```py\n{trace}```").format(
                        t=t,
                        requesterStr=ctx.author.name,
                        requesterS=ctx.author.discriminator,
                        requesterNum=ctx.author.id,
                        message=ctx.message.content,
                        trace="".join(traceback.format_exception(type(e), e, e.__traceback__))
                )
            )
        

def get_command_prefix(bot: CovidBot, msg: Message):
    return os.getenv("prefix") or "!"