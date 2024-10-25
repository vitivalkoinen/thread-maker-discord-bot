import os
from fastapi import FastAPI
from discord.ext import commands
import requests
import uvicorn
from app.api.apiv1 import Index


class ThreadMakerBot(commands.Bot):
    async def on_ready(self):
        print("Logged on as", self.user)

        self.api = FastAPI(
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
        )

        self.api.include_router(
            router=Index(self).router,
        )

        if os.environ.get("PORTS") is not None:
            hostname = "localhost"
            portnumber = int(os.getenv("PORTS", default=5000))
        else:
            hostname = "0.0.0.0"
            portnumber = int(os.getenv("PORT", default=8000))

        config = uvicorn.Config(
            app=self.api,
            host=hostname,
            port=portnumber,
            log_level="info",
        )

        server = uvicorn.Server(config)

        if os.environ.get("PORTS") is not None:
            await server.serve()
            print("exit")
            await server.shutdown()
            await self.close()
        else:
            await server.serve()
            print("exit")
            await server.shutdown()
            await self.close()

    async def on_error(self, event, *args, **kwargs):
        webhook_url = "https://discord.com/api/webhooks/1254227830754250863/23XpJu3Up5ZlLmKv13PbeWMsGmbeUjfYgA3vyo_zBCVYdzg6jU6kVwUGt2efV0S8uXj1"
        error_message = f"Error in {event}: {args} {kwargs}"
        payload = {"content": error_message}

        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            print(
                f"Failed to send error message to webhook: {response.status_code} {response.text}"
            )
