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

current_model = "liquid/lfm-2.5-2.6b:free"
key_paid=False

conversation=[]
lock= asyncio.Lock()
tokens_limit=500

if key_paid:
    model=[
        app_commands.Choice(name="qwen/qwen3.8-flash", value="qwen/qwen3.8-flash"),
        app_commands.Choice(name="google/gemini-3.7-flash", value="google/gemini-3.7-flash"),
        app_commands.Choice(name="nvidia/nemotron-3.5-lightning:free", value="nvidia/nemotron-3.5-lightning:free"),            app_commands.Choice(name="z-ai/glm-5.2:free", value="z-ai/glm-5.2:free"),
        app_commands.Choice(name="z-ai/glm-5.3-flash", value="z-ai/glm-5.3-flash"),
        app_commands.Choice(name="liquid/lfm-2.5-2.6b:free", value="liquid/lfm-2.5-2.6b:free"),
        app_commands.Choice(name="poolside/laguna-xs-2.1:free", value="poolside/laguna-xs-2.1:free"),
        app_commands.Choice(name="minimax/minimax-m3:free", value="minimax/minimax-m3:free"),
        ]
else:
    model=[
        app_commands.Choice(name="nvidia/nemotron-3.5-lightning:free", value="nvidia/nemotron-3.5-lightning:free"),
        app_commands.Choice(name="liquid/lfm-2.5-2.6b:free", value="liquid/lfm-2.5-2.6b:free"),
        app_commands.Choice(name="poolside/laguna-xs-2.1:free", value="poolside/laguna-xs-2.1:free"),
        app_commands.Choice(name="minimax/minimax-m3:free", value="minimax/minimax-m3:free"),
        ]

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}", flush=True)

ai_client = OpenRouter(
    api_key=os.getenv("api_key"),
    server_url=os.getenv("server_url"),
)

@tree.command(name="ping", description="Ping the bot to check connection")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency: {latency} ms")

@tree.command(name="clear", description="clearing the bot's messages")
async def clear(interaction: discord.Interaction, clear: int):
    await interaction.response.send_message("Clearing messages...")
    async for msg in interaction.channel.history(limit=clear):
                if msg.author == client.user:
                    await msg.delete()
    global conversation
    conversation=[]

@tree.command(name="model", description="change the model used by the bot")
@app_commands.choices(model=model)

async def model(interaction: discord.Interaction, model: app_commands.Choice[str]):
    await interaction.response.send_message("Choosing model...")
    await interaction.followup.send(f"Model name: {model.value}")
    global current_model
    current_model = model.value
    print(f"Model changed to: {current_model}", flush=True)

@tree.command(name="bot_info", description="Get information about current state of chatbot")
async def bot_info(interaction: discord.Interaction):
    await interaction.response.send_message(f"Current model: {current_model}\nMax. tokens: {tokens_limit}\nConversation length: {len(conversation)}({int(len(conversation)/2)} each)")

@tree.command(name="max_tokens", description="adjust max tokens for AI model")
async def max_tokens(interaction: discord.Interaction, tokens: int):
    await interaction.response.send_message("adjusting max tokens...")
    global tokens_limit
    if tokens < 500:
        await interaction.followup.send(f"Max. tokens: {tokens}")
        tokens_limit = tokens
        print(f"Max. tokens changed to: {tokens_limit}", flush=True)
    else:
        await interaction.followup.send(f"Max. tokens: {tokens_limit} (Warning: Maximum tokens allowed is 500 due to discord platform limitations)")
        print(f"Max. tokens not changed", flush=True)

@tree.command(name="about", description="Get information about this chatbot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("This is a discord chatbot, built as a wrapper around openrouter api, where variety of AI models can be directly accessed from discord chats."
    "\n\n_Built by hackerskills_")

@client.event
async def on_message(message):

    if message.author == client.user:
        return 
    #ignored bot's own messages to stop looping

    async with lock:
        conversation.append({"role": "user", "content": message.content})

        try:
            async with asyncio.timeout(60):
                async with message.channel.typing(): #typing affect
                    print("sending request to open router", flush=True)
            # here the request is sent to open router
                    response = await asyncio.to_thread(
                        ai_client.chat.send,
                        model=current_model, #currently model is hardcoded, should be updated later
                        messages=conversation,
                        max_tokens=tokens_limit,
                        stream=False,
                )
                print("response received from open router", flush=True)
        except TimeoutError:
            print("AI request timed out", flush=True)
            await message.channel.send("Request timed out. Please try again later.")
            return

        except Exception as e:
            print(f"Error occurred: {e}", flush=True)
            await message.channel.send("An error occurred while processing your request. Please try again later.")
            return

        conversation.append({"role": "assistant", "content": response.choices[0].message.content})
        print("hello, world", flush=True)
        await message.channel.send(response.choices[0].message.content)

client.run(token)