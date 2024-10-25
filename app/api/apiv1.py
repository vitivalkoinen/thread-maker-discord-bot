from fastapi import APIRouter, Request
from typing import Any

from app.bot.threadmaker import ThreadMakerBot


class Index:
    router = APIRouter()

    def __init__(self, bot: ThreadMakerBot):
        self.bot = bot

    @router.get("/")
    async def root(self, request: Request) -> dict[str, Any]:
        return {"message": f"bot id:{self.bot.application_id}"}
