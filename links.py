import client
import discord

@client.bot.tree.command(name="source", description="Download the MonkeFrames source code")
async def get_source(interaction: discord.Interaction):
    await interaction.response.send_message("https://github.com/MonkeFrames/MonkeFrames")

@client.bot.tree.command(name="download", description="Download the latest release of MonkeFrames")
async def get_download(interaction: discord.Interaction):
    await interaction.response.send_message("https://github.com/MonkeFrames/MonkeFrames/releases/latest")