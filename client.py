import discord
from discord.ext import commands

class BotClient(commands.Bot):
    def __init__(self, *, intents, **options):
        global instance
        super().__init__(intents=intents, **options)

    @staticmethod
    def instance() -> BotClient:
        global bot
        return bot

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        await self.sync_commands()

    async def sync_commands(self):
        FRAMES_GUILD = discord.Object(id=1494137109848789113)
        self.tree.copy_global_to(guild=FRAMES_GUILD)
        await self.tree.sync(guild=FRAMES_GUILD)

        print("Slash commands synced")

intents = discord.Intents.default()
intents.message_content = True

bot = BotClient(
    command_prefix="!",
    intents=intents,
    status=discord.Status.idle
)

@bot.tree.command(name="ping", description="Check server status")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong ({bot.latency * 1000}ms)", ephemeral=True)

import links
import forum