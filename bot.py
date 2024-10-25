import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests


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

    async def on_error(self, event, *args, **kwargs):
        webhook_url = "https://discord.com/api/webhooks/1254227830754250863/23XpJu3Up5ZlLmKv13PbeWMsGmbeUjfYgA3vyo_zBCVYdzg6jU6kVwUGt2efV0S8uXj1"
        error_message = f"Error in {event}: {args} {kwargs}"
        payload = {"content": error_message}

        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            print(
                f"Failed to send error message to webhook: {response.status_code} {response.text}"
            )


class ThreadMakerException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class ThreadAlreadyExists(ThreadMakerException):
    def __str__(self):
        return f"this thread is already exists: {self.arg}"


class ThreadMakerCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="make")
    async def make_thread(self, ctx: commands.Context):
        if not isinstance(ctx.channel, discord.TextChannel):
            await ctx.send("テキストチャンネルではないのでスレッドを作成できません。")
            return

        thread_name = self._generate_class_name()
        try:
            thread = await self._create_thread(ctx.channel, thread_name)
            await self._add_all_members(thread, ctx.channel.members)
        except ThreadAlreadyExists as e:
            print(e)
            await ctx.send("既に授業用スレッドが存在します")
            return
        except Exception as e:
            raise e

        # そのチャンネルの全メンバーをスレッドに追加

        await ctx.send(
            f"スレッド「{thread.name}」が正常に作成され、全メンバーが追加されました。"
        )

    def _is_exists_thread(self, txtch: discord.TextChannel, thread_name: str) -> bool:
        # 既存のスレッドをチェック
        existing_threads = set(thread.name for thread in txtch.threads)
        return thread_name in existing_threads

    async def _create_thread(
        self, txtch: discord.TextChannel, thread_name: str
    ) -> discord.Thread:
        if self._is_exists_thread(txtch, thread_name):
            raise ThreadAlreadyExists(thread_name)

        # 新しいスレッドを作成
        thread = await txtch.create_thread(
            name=thread_name, reason="授業用スレッドの作成"
        )

        return thread

    async def _add_all_members(
        self, thread: discord.Thread, members: list[discord.Member]
    ) -> None:
        for member in members:
            if not member.bot:
                await thread.add_user(member)

    @staticmethod
    def _generate_class_name() -> str:
        return datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y/%m/%d の授業")


if __name__ == "__main__":
    asyncio.run(main())
