import os
from datetime import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = str(os.getenv("DISCORD_BOT_TOKEN"))
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = ThreadMaker(
        command_prefix="!",
        intents=intents,
    )

    bot.add_command(make_thread)
    bot.add_command(print_member)
    bot.run(token)


class ThreadMaker(commands.Bot):
    async def on_ready(self):
        print("Logged on as", self.user)


@commands.command(name="print_member")
async def print_member(ctx: commands.Context):
    if not isinstance(ctx.channel, discord.TextChannel):
        return
    for member in ctx.channel.members:
        await ctx.send(member.name)


@commands.command(name="make")
async def make_thread(ctx: commands.Context):
    if not isinstance(ctx.channel, discord.TextChannel):
        return

    thread_name = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y/%m/%d の授業")

    if is_exists_thread(ctx.channel, thread_name):
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


def is_exists_thread(text_channel: discord.TextChannel, thread_name: str) -> bool:
    # 既存のスレッドをチェック
    existing_threads = set(thread.name for thread in text_channel.threads)
    return thread_name in existing_threads


if __name__ == "__main__":
    main()
