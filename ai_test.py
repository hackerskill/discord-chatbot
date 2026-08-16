import os
from dotenv import load_dotenv
from openrouter import OpenRouter

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")

client = OpenRouter(
    api_key=os.getenv("api_key"),
    server_url=os.getenv("server_url"),
)

response = client.chat.send(
    model="nvidia/nemotron-3.5-lightning:free", #currently model is hardcoded, should be updated later
    messages=[
        {"role": "user", "content": "Introduce yourself"}
    ],
    max_tokens=1000,
    stream=False,
)
print("hello, world")
print(response.choices[0].message.content)
