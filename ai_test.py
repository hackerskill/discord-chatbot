import os
from dotenv import load_dotenv
from openrouter import OpenRouter

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")
conversation=[]

client = OpenRouter(
    api_key=os.getenv("api_key"),
    server_url=os.getenv("server_url"),
)
while True:    
    query=input("Enter your message: ")
    conversation.append({"role": "user", "content": query})
# here the request is sent to open router
    response = client.chat.send(
    model="nvidia/nemotron-3.5-lightning:free", #currently model is hardcoded, should be updated later
    messages=conversation,
    max_tokens=1000,
    stream=False,
    )

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("hello, world")
    print(response.choices[0].message.content)
