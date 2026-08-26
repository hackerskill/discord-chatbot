import os
from dotenv import load_dotenv
from openrouter import OpenRouter
import discord
from discord import app_commands
import asyncio

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree= app_commands.CommandTree(client)

current_model = "nvidia/nemotron-3.5-lightning:free"

conversation=[]

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

ai_client = OpenRouter(
    api_key=os.getenv("api_key"),
    server_url=os.getenv("server_url"),
)

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

    conversation.append({"role": "user", "content": message.content})
    async with message.channel.typing(): #typing affect
# here the request is sent to open router
        response = await asyncio.to_thread(
            ai_client.chat.send,
            model=current_model, #currently model is hardcoded, should be updated later
            messages=conversation,
            max_tokens=2000,
            stream=False,
    )

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("hello, world")
    await message.channel.send(response.choices[0].message.content)

client.run(token)