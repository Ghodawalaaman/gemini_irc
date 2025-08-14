import asyncio
import os
import pydle
import google.generativeai as genai

# Initialize the model
model = genai.GenerativeModel('gemini-2.5-flash')

class MyClient(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """

    async def on_connect(self):
        await super().on_connect()
        await self.join('#bsah')

    async def on_join(self, channel, user):
        await super().on_join(channel, user)
        if user == self.nickname:
            response = model.generate_content("Explain how AI works in a few words")
            await self.message(channel, f'{response.text}')
            await self.message(channel, 'SkyNet is activated!')

    async def on_message(self, target, source, message):
        if source != self.nickname and message.startswith(f"{self.nickname}"):
            try:
               response = model.generate_content(f"{message[(len(self.nickname)+1):].strip()}")
            except Exception as e:
                await self.message(target, f"Error generating response: {e}")
                return
            lines = response.text.split("\n")
            for line in lines:
                if len(line.strip()) == 0 or line.strip() == "\n":
                    continue
                await self.message(target, f'{line.strip()}')
                await asyncio.sleep(0.5)  # Non-blocking sleep

async def start():
    client = MyClient('gemini_bot')
    await client.connect('irc.libera.chat', tls=True)
    await client.handle_forever()

if __name__ == "__main__":
    asyncio.run(start())
