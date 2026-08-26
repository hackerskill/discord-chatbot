#used to test discord bot connection, as it echoes the message sent by user to the same chat

import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    #ignored bot's own messages to stop looping

    if message.content == "!clear": #for clearing bot chat

        async for msg in message.channel.history(limit=100):
            if msg.author == client.user:
                await msg.delete()

        return

    # echoing the message sent by user for testing
    await message.channel.send(f"You said: {message.content}")


client.run(TOKEN)
