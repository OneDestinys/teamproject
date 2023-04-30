# Sources: https://docs.pycord.dev/en/stable/ext/commands/api.html#discord.ext.commands.Bot.command_prefix

# Application command - /slash command (from discord import Bot)
# PRefixed command (Application Command) - from discord.ext.commands
# BRidge commands - from discord.ext.bridge Cogs
import io
from discord.ext import commands
from discord.ext.bridge import Bot, BridgeContext, has_permissions
from discord.ui import Button, View
import discord
from settings import TOKEN, MONGODBURL, TRANSCRIPT_CHANNEL_ID
from pymongo import MongoClient
import chat_exporter
import requests

# Creating bot object and assigning it to a variable, passing my command prefix and permissions as parameters
my_bot = Bot(command_prefix="!", intents=discord.Intents.all())
client = MongoClient(MONGODBURL)
database = client["Cluster0"]
tickets = database["Cluster0"]


# https://pymongo.readthedocs.io/en/stable/tutorial.html
@my_bot.event
async def on_ready():
    print(f"Now running {my_bot.user.name}...")
    my_bot.add_view(Panel_Options())
    # adding my class into the possible selectable items you can view


# bridge command will await message with prefix or /
@my_bot.bridge_command(description="To get a pong back!")
async def ping(ctx: BridgeContext):
    # waiting for the user to respond with !ping or /ping to respond with Pong
    await ctx.respond("Pong")


@my_bot.bridge_command(description="A command to ban users")
# Checking attributes permissions to make sure that the user who is operating this command has admin
@has_permissions(administrator=True)
async def ban(ctx: BridgeContext, user: discord.Member):
    await ctx.guild.ban(user)
    await ctx.respond(f"{user.mention} has been banned!")


@my_bot.bridge_command(description="A command to add users from a ticket")
# Checking attributes permissions to make sure that the user who is operating this command has admin
@has_permissions(administrator=True)
async def add(ctx: BridgeContext, user: discord.Member):
    if ctx.channel.category.name != "tickets":
        ctx.respond("Sorry, we can only add members to tickets.")
        return
    channel: discord.TextChannel = ctx.channel

    await channel.set_permissions(
        target=user,
        overwrite=discord.PermissionOverwrite(
            view_channel=True, send_messages=True, read_messages=True
        ),
    )
    await ctx.respond(f"Added {user.mention} to channel")
    await user.send(f"You've been added to the channel {ctx.channel.mention}")


@my_bot.bridge_command(description="To generate a cute cat!")
async def cat(ctx: BridgeContext):
    resp = requests.get("https://api.thecatapi.com/v1/images/search").json()
    url = resp[0]["url"]
    resp_quote = requests.get("https://zenquotes.io/api/random").json()
    quote = resp_quote[0]["q"]
    embed = discord.Embed(title=quote)
    embed.set_image(url=url)
    await ctx.respond(embeds=[embed])


@my_bot.bridge_command(description="To close your ticket")
# https://github.com/mahtoid/DiscordChatExporterPy
async def close(ctx: BridgeContext):
    user = None
    try:
        user = ctx.user
    except:
        user = ctx.author

    # Had original attribute errors where 'bridgeextcontext' object did not have user attribute, so I did a try/except so if user = ctx.user rose an error it would do the
    channel = ctx.channel
    guild = ctx.guild
    if channel.category.name == "tickets":
        await ctx.respond("Your ticket is being archived")
        transcript = await chat_exporter.export(ctx.channel)
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html",
        )
        transcript_file_2 = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html",
        )
        transc = guild.get_channel(TRANSCRIPT_CHANNEL_ID)
        await transc.send(
            f"<@!{channel.topic}>'s ticket has been archived by {user.mention}",
            files=[transcript_file],
        )
        member = await guild.fetch_member(channel.topic)
        await member.send(
            f"Your ticket was archived by {user.mention}", files=[transcript_file_2]
        )
        await channel.delete()
    else:
        ctx.respond("You're currently not in a ticket!")


@ban.error
async def ban_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond("Please enter a user to ban")
    print(error)


class Panel_Options(View):
    def __init__(self):
        super().__init__(timeout=None)
        # calling super to override the view class, setting timeout = none so the bot recognizes my buttons even after a restart

    @discord.ui.button(
        label="Open a Ticket", custom_id="1", style=discord.ButtonStyle.primary
    )
    async def callback(self, btn, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, invisible=False)
        # the bot only has 5 seconds to respond and this can be slow, so we need to let it 'think' for a bit
        Create_Category = True
        category = None
        for item in interaction.guild.categories:
            if "tickets" == item.name:
                Create_Category = False
                category = item
        if Create_Category:
            category = await interaction.guild.create_category(name="tickets")
        # waiting for interaction to finish so it can make the ticket

        for channel in category.text_channels:
            if channel.topic == str(interaction.user.id):
                await interaction.followup.send(content="You already have a ticket")
                return

        ticket_id = tickets.estimated_document_count() + 1
        ticket = await interaction.guild.create_text_channel(
            name=f"ticket-{ticket_id}",
            category=category,
            overwrites={
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True, send_messages=True, read_messages=True
                ),
                interaction.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                ),
            },
            topic=f"{interaction.user.id}",
        )
        tickets.insert_one({"creator": interaction.user.id, "channel": ticket.id})
        await interaction.followup.send(
            content=f"You've created a new ticket {ticket.mention}"
        )


@my_bot.command()
async def panel(ctx):
    await ctx.send(
        view=Panel_Options(),
        embeds=[
            discord.Embed(
                color=0xA020F0,
                title="Ticket Panel",
                description="Click on the button below to make a ticket",
            )
        ],
    )
    # https://www.youtube.com/watch?v=kNUuYEWGOxA
    # https://towardsdatascience.com/binary-hex-and-octal-in-python-20222488cee1


my_bot.run(TOKEN)
