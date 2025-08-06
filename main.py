import time
import asyncio
import pydle
from google import genai

client = genai.Client()

class MyClient(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """

    async def on_connect(self):
        await super().on_connect()
        await self.join('#bsah')

    async def on_join(self, channel, user):
        await super().on_join(channel, user)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents="Explain how AI works in a few words"
        )
        await self.message(channel, f'{response.text}')

    async def on_message(self, target, source, message):
        if source != "gemini_bot" and "gemini_bot" in message:
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=f"{message}"
            )
            lines = response.text.split("\n")
            for line in lines:
                await self.message(target, f'{line}')
                time.sleep(0.5)

async def start():
    client = MyClient('gemini_bot')
    await client.connect('irc.libera.chat', tls=True)
    await client.handle_forever()

asyncio.run(start())
