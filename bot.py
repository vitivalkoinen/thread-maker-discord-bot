import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands
from dotenv import load_dotenv


async def main():
    load_dotenv()
    token = str(os.getenv("DISCORD_BOT_TOKEN"))
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = ThreadMakerBot(
        command_prefix="!",
        intents=intents,
    )
    await bot.add_cog(ThreadMakerCommand(bot))
    await bot.start(token)


class ThreadMakerBot(commands.Bot):
    async def on_ready(self):
        print("Logged on as", self.user)


class ThreadMakerCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="make")
    async def make_thread(self, ctx: commands.Context):
        if not isinstance(ctx.channel, discord.TextChannel):
            return

        thread_name = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y/%m/%d の授業")

        if self._is_exists_thread(ctx.channel, thread_name):
            await ctx.send(f"スレッド「{thread_name}」は既に存在します。")
            return

        # 新しいスレッドを作成
        thread = await ctx.message.create_thread(
            name=thread_name, reason="授業用スレッドの作成"
        )

        # そのチャンネルの全メンバーをスレッドに追加
        for member in ctx.channel.members:
            if not member.bot:
                await thread.add_user(member)

        await ctx.send(
            f"スレッド「{thread.name}」が正常に作成され、全メンバーが追加されました。"
        )

    def _is_exists_thread(
        self, text_channel: discord.TextChannel, thread_name: str
    ) -> bool:
        # 既存のスレッドをチェック
        existing_threads = set(thread.name for thread in text_channel.threads)
        return thread_name in existing_threads


if __name__ == "__main__":
    asyncio.run(main())
