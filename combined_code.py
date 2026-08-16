import os
from dotenv import load_dotenv
from openrouter import OpenRouter
import discord

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
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


    response = ai_client.chat.send(
    model="nvidia/nemotron-3.5-lightning:free", #currently model is hardcoded, should be updated later
    messages=[
        {"role": "user", "content": message.content}
    ],
    max_tokens=1000,
    stream=False,
    )
    print("hello, world")
    #print(response.choices[0].message.content)

    await message.channel.send(response.choices[0].message.content)


client.run(token)