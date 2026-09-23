import dotenv
dotenv.load_dotenv()

import discord
import os

import client

client.bot.run(os.getenv("DISCORD_TOKEN"))