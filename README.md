# discord-chatbot
An AI wrapper in the form of a discord bot

## Features
* **AI Chat** — Directly send prompts to an AI model from Discord.
* **Discord Support** — Works directly in Discord DMs and servers.
* **Memory** — Remembers previous messages in a conversation.
* **Multiple AI Models** — Switch between different AI models.
* **Bot Info** — See the current model and settings.
* **Token Control** — Control the maximum number of tokens in responses.
* **Slash Commands** — Short commands for controlling the bot.
* **Typing Indicator** — Shows when the bot is thinking.

## Slash Commands
* **`ping`** — Check chatbot connectivity status.
* **`model`** — Change the AI model from options presented.
* **`max_tokens`** — Adjust the maximum number of tokens a response can have.
* **`bot_info`** — See info about current bot settings like model and conversation history.
* **`clear`** — Clear recent messages by chatbot.
* **`about`** — Shows information about the bot itself.

## Setup

1. Get API keys for Discord bot at [Discord Developer Portal](https://discord.com/developers/) and AI gateway.

2. Clone the repo

3. **Create and activate a virtual environment:**
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
4. **Change `.env.example` to `.env` with the following keys-**
    * Discord token specific for a bot
    * AI gateway API key
    * AI gateway server URL

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Verification (Optional)

Before running the main application, you can optionally test your API key or discord token connections or AI model using the utility scripts provided:

* **`discord_test.py`** — Validates your discord token connection wherein any message sent to bot is relayed back as echo test.
* **`model_test.py`** - Verifies your API key setup and communication with the AI service with a hardcoded model and prompt.
* **`ai_test.py`** — Tests different models and conversation context..

### Running the Application

Once setup is verified, `main.py` can be run to start the discord chatbot.

---

**Made by hackerskill**