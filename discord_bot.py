# Sources: https://docs.pycord.dev/en/stable/ext/commands/api.html#discord.ext.commands.Bot.command_prefix

# Application command - /slash command (from discord import Bot)
# PRefixed command (Application Command) - from discord.ext.commands
# BRidge commands - from discord.ext.bridge Cogs
from discord.ext import commands
from discord.ext.bridge import Bot, BridgeContext, has_permissions
from discord.ui import Button, View
import discord
from settings import TOKEN, MONGODBURL
from pymongo import MongoClient

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
@my_bot.bridge_command()
async def ping(ctx: BridgeContext):
    # waiting for the user to respond with !ping or /ping to respond with Pong
    await ctx.respond("Pong")


@my_bot.bridge_command(description="A command to ban users")
# Checking attributes permissions to make sure that the user who is operating this command has admin
@has_permissions(administrator=True)
async def ban(ctx: BridgeContext, user: discord.Member):
    await ctx.guild.ban(user)
    await ctx.respond(f"{user.mention} has been banned!")


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
        await interaction.response.defer()
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
            if channel.topic == interaction.user.id:
                await interaction.response.send_message("You already have a ticket")
                return

        ticket_id = tickets.estimated_document_count() + 1
        ticket = await interaction.guild.create_text_channel(
            name=f"ticket-{ticket_id}",
            category=category,
            overwrites={
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True),
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False)
            },
            topic=f'{interaction.user.id}'
        )
        tickets.insert_one({
            "creator": interaction.user.id,
            "channel": ticket.id
        })


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
