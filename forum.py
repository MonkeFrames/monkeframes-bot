import client
import discord
import typing

ISSUES_FORUM_ID = 1497004831028678837

@client.bot.tree.command(name="close", description="Close the issue")
@discord.app_commands.checks.has_role(1497007239708541103)
async def close_ticket(interaction: discord.Interaction):
    is_in_target_forum = (
        isinstance(interaction.channel, discord.Thread)
        and interaction.channel.parent_id == ISSUES_FORUM_ID
    )

    if not is_in_target_forum:
        await interaction.response.send_message("Must be in issues forum", ephemeral=True)
        return

    thread: discord.Thread = interaction.channel

    await add_tags(thread, ["Closed"])
    await thread.edit(name="[Closed] " + thread.name, locked=True)
    await interaction.response.send_message("Issue closed", ephemeral=True)

@client.bot.tree.command(name="accept", description="Accept an issue")
@discord.app_commands.describe(version="The MonkeFrames version you plan to implement this by")
@discord.app_commands.checks.has_role(1497007239708541103)
async def accept_ticket(interaction: discord.Interaction, version: str):
    is_in_target_forum = (
        isinstance(interaction.channel, discord.Thread)
        and interaction.channel.parent_id == ISSUES_FORUM_ID
    )

    if not is_in_target_forum:
        await interaction.response.send_message("Must be in issues forum", ephemeral=True)
        return

    thread: discord.Thread = interaction.channel

    await add_tags(thread, ["Accepted"])
    await thread.edit(name="[Accepted] " + thread.name, locked=True)
    await interaction.response.send_message("Issue closed", ephemeral=True)

@client.bot.tree.command(name="autotag", description="Apply necessary tags to an issue")
@discord.app_commands.describe(
    software="What the issue applies to",
    issue_type="What type of issue this is"
)
@discord.app_commands.checks.has_role(1497007239708541103)
async def autotag_ticket(interaction: discord.Interaction,
                       software: typing.Literal["Editor", "Compiler", "Editor + Compiler"],
                       issue_type: typing.Literal["Bug", "Features", "Misc"]
):
    is_in_target_forum = (
        isinstance(interaction.channel, discord.Thread)
        and interaction.channel.parent_id == ISSUES_FORUM_ID
    )

    if not is_in_target_forum:
        await interaction.response.send_message("Must be in issues forum", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    thread: discord.Thread = interaction.channel

    await thread.edit(applied_tags=[])
    await add_tags(thread, [software, issue_type])
    await interaction.followup.send("Tags have been applied", ephemeral=True)

async def add_tags(thread: discord.Thread, tags: list[str]):
    forum_channel = thread.parent
    tag_objs: list[discord.ForumTag] = []

    for tag in tags:
        tag_objs.append(discord.utils.get(forum_channel.available_tags, name=tag))
    
    if len(tag_objs) > 0:
        await thread.edit(applied_tags=thread.applied_tags + tag_objs)

async def remove_tags(thread: discord.Thread, tags: list[str]):
    forum_channel = thread.parent
    
    new_tags = [
        tag for tag in thread.applied_tags 
        if tag.name.lower() not in tags
    ]

    await thread.edit(applied_tags=new_tags)