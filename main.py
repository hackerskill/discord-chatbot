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
tokens_limit=2000

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

ai_client = OpenRouter(
    api_key=os.getenv("api_key"),
    server_url=os.getenv("server_url"),
)

@tree.command(name="ping", description="Ping the bot to check connection")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="clear", description="clearing the bot's messages")
async def clear(interaction: discord.Interaction):
    await interaction.response.send_message("Clearing messages...")
    async for msg in interaction.channel.history(limit=100):
                if msg.author == client.user:
                    await msg.delete()

@tree.command(name="model", description="change the model used by the bot")
@app_commands.choices(
    model=[
        app_commands.Choice(name="nvidia/nemotron-3.5-lightning:free", value="nvidia/nemotron-3.5-lightning:free"),
        app_commands.Choice(name="z-ai/glm-5.2:free", value="z-ai/glm-5.2:free"),
        app_commands.Choice(name="nvidia/nemotron-3-ultra-550b-a55b:free", value="nvidia/nemotron-3-ultra-550b-a55b:free"),
    ]
)
async def model(interaction: discord.Interaction, model: app_commands.Choice[str]):
    await interaction.response.send_message("Choosing model...")
    await interaction.followup.send(f"Model name: {model.value}")
    global current_model
    current_model = model.value
    print(f"Model changed to: {current_model}")

@tree.command(name="bot_info", description="Get information about current state of chatbot")
async def bot_info(interaction: discord.Interaction):
    await interaction.response.send_message(f"Current model: {current_model}\nMax. tokens: {tokens_limit}\nConversation length: {len(conversation)}")

@tree.command(name="max_tokens", description="adjust max tokens for AI model")
async def max_tokens(interaction: discord.Interaction, tokens: int):
    await interaction.response.send_message("adjusting max tokens...")
    await interaction.followup.send(f"Max. tokens: {tokens}")
    global tokens_limit
    tokens_limit = tokens
    print(f"Max. tokens changed to: {tokens_limit}")

@tree.command(name="about", description="Get information about this chatbot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("This is a discord chatbot, built as a wrapper around openrouter api, where variety of AI models can be directly accessed from discord chats."
    "\n\n_Built by hackerskills_")

@client.event
async def on_message(message):

    if message.author == client.user:
        return 
    #ignored bot's own messages to stop looping

    conversation.append({"role": "user", "content": message.content})
    async with message.channel.typing(): #typing affect
        print("sending request to open router")
# here the request is sent to open router
        response = await asyncio.to_thread(
            ai_client.chat.send,
            model=current_model, #currently model is hardcoded, should be updated later
            messages=conversation,
            max_tokens=tokens_limit,
            stream=False,
    )

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("hello, world")
    await message.channel.send(response.choices[0].message.content)

client.run(token)