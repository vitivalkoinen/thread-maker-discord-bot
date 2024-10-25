from discord.ext import commands
import requests


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
