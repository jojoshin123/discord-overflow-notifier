import discord
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
FOX_CHANNEL_ID = os.getenv("FOX_CHANNEL_ID")
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))
OUTPUT_CHANNEL_ID = int(os.getenv("OUTPUT_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

mentionPrefix = ""

@bot.event
async def on_ready():
    global mentionPrefix
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(OUTPUT_CHANNEL_ID)
    for member in channel.members:
        mentionPrefix += member.mention

@bot.event
async def on_message(message):
    global mentionPrefix
    if message.channel.id == TEST_CHANNEL_ID:  # Replace with your channel ID
        print(f"New message in {message.channel.name}: {message.content}")
        channel = bot.get_channel(OUTPUT_CHANNEL_ID)
        await channel.send(mentionPrefix + "\n" + message.content)

bot.run(BOT_TOKEN)



