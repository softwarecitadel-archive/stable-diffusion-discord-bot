# Build and deploy a Stable Diffusion XL Discord bot with Replicate and Software Citadel

## Prerequisites

- A [Replicate](https://replicate.com) account
- A [Software Citadel](https://softwarecitadel.com) account, with a registered payment method

## Introduction

[Replicate](https://replicate.com) is a platform that allows to run and fine-tune open-source models. In this tutorial, we will use Replicate to run Stable Diffusion XL generations.

[Software Citadel](https://softwarecitadel.com) allows you to deploy applications from a Dockerfile. In this tutorial, we will use Software Citadel to deploy a Discord bot that will generate Stable Diffusion XL generations.

## Prerequisites

- A [Replicate](https://replicate.com) account
- A [Software Citadel](https://softwarecitadel.com) account, with a registered payment method
- A [Discord](https://discord.com) account

## Setting up the Discord bot

1. Log in to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application. You can name it whatever you want.

![Discord bot](/images/new_application.png)
![Discord bot](/images/create_an_application.png)

2. Go to the "Bot" tab, and turn on the "Message Content Intent" option.

![Discord bot](/images/message_content_intent.png)

In this section, you can also click on "Reset token" to generate a new token for your bot.

![Discord bot](/images/reset_token.png)

3. Now, let's invite the bot, so we can test it. Go to the "OAuth2" tab, and the "URL Generator" tab. Select the "bot" scope, and the "Send Messages" permission. Then, copy the generated URL and paste it in your browser. You will be asked to select a server to invite the bot to. Select a server, and click on "Authorize".

## Developing the Bot

### Initializing the workspace

First, we need to create a new directory for our bot:

```bash
mkdir gilbert-bot
cd gilbert-bot
```

Then, we are going to create a new Python project using Poetry:

```bash
# Install Poetry (if you don't have it already)
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
# Initialize a new Python project
poetry init -n
# Install the dependencies
poetry add discord.py python-dotenv replicate
```

Let's create new file called `.env` in the root of the project. For your Discord token, grab it from the [Discord Developer Portal](https://discord.com/developers/applications). You also need to get a Replicate API token from the [Replicate website](https://replicate.com). You can find your API token in the [settings page](https://replicate.com/account/api-tokens).

```bash
touch .env
```

Open the `.env` file and add the following line:

```bash
DISCORD_TOKEN="YOUR_DISCORD_TOKEN"
REPLICATE_API_TOKEN="YOUR_REPLICATE_API_TOKEN"
```

Do not forget to add this .env file to your `.gitignore` file.

Alright, we are ready to start coding!

Let's create a new file called `bot.py` in the root of the project. This file will contain the code for our bot.

```bash
touch bot.py
```

Open the `bot.py` file and add the following code:

```python
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
import replicate

# We load the environment variables
load_dotenv()

# We set up the intents to allow the bot to read messages
intents = Intents.default()
intents.message_content = True

# We initialize the bot
bot = commands.Bot(
    command_prefix="/",
    intents=intents,
)


@bot.command()
async def imagine(ctx, *, prompt):
    # We send a message to let the user know we're working on it.
    msg = await ctx.send(f"“{prompt}”\n> Dreaming up an image...")

    # We use the Stable Diffusion XL model to generate images.
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "prompt": prompt,
            # Customize the following parameters to your liking
            # https://replicate.com/stability-ai/sdxl?input=python
        },
    )
    image = output[0]

    # We edit the message to show the generated image.
    await msg.edit(content=f"“{prompt}”\n{image}")

# Run the bot with the Discord token from the .env file
bot.run(os.environ["DISCORD_TOKEN"])
```

## Deploying the Bot with Software Citadel

To deploy your bot, you can use Software Citadel. Follow these steps:

1. Install Software Citadel CLI:

```bash
curl -L https://cli.softwarecitadel.com/install.sh | sh
```

2. Authenticate with Software Citadel:

```bash
citadel auth login
```

3. Initialize Software Citadel:

```bash
citadel init
```

4. Dockerize your bot:

```Dockerfile
FROM python:3.11

RUN pip install poetry

WORKDIR /project

COPY poetry.lock pyproject.toml /project/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /project

CMD python bot.py
```

5. Deploy your bot:

```bash
citadel deploy
```

Congratulations! You have successfully deployed your Discord bot. To test it, you can send a message to your bot in Discord.

![Discord bot](/images/final_screenshot.png)
