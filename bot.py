from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
import replicate

load_dotenv()

intents = Intents.default()
intents.message_content = True

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

    await msg.edit(content=f"“{prompt}”\n{image}")


bot.run(os.environ["DISCORD_TOKEN"])
