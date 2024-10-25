import os
import asyncio
from discord import Intents
from dotenv import load_dotenv

from app.bot.threadmaker import ThreadMakerBot
from app.bot.commands import ThreadMakerCommand


async def main():
    load_dotenv()
    token = str(os.getenv("DISCORD_BOT_TOKEN"))
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = ThreadMakerBot(
        command_prefix="!",
        intents=intents,
    )
    await bot.add_cog(ThreadMakerCommand(bot))
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
