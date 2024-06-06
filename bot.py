import os
import discord
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = str(os.getenv("DISCORD_BOT_TOKEN"))
    intents = discord.Intents.default()
    intents.message_content = True
    client = ThreadMaker(intents=intents)
    client.run(token)


class ThreadMaker(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content == "ping":
            await message.channel.send("pong")


if __name__ == "__main__":
    main()
