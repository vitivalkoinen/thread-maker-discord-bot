from fastapi import APIRouter
from typing import Dict

from discord.ext import commands


class Index:

    def __init__(self, bot: commands.Bot):
        self.router = APIRouter()
        self.bot = bot

        self.router.add_api_route("/", self.root, methods=["GET"])

    async def root(self) -> Dict:
        return {"message": f"bot id:{self.bot.application_id}"}
