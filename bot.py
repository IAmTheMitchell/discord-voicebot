import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into the environment

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True  # needed for display_name
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

REGULAR_MESSAGES = [
    "is now hanging out in",
    "has joined",
    "is chilling in",
    "jumped into",
    "entered",
    "is vibing in",
    "is now in",
]


def is_member_joined(before: discord.VoiceState, after: discord.VoiceState):
    return before.channel is None and after.channel is not None


def get_channel_for_message(discord_mod, bot_client, guild_id):
    guild = bot_client.get_guild(guild_id)
    # pick the first text channel the bot can send to
    for ch in guild.text_channels:
        if ch.permissions_for(guild.me).send_messages:
            return ch
    return None


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user} (id={bot.user.id})")
    else:
        print("Bot user is not initialized.")


@bot.event
async def on_voice_state_update(member, before, after):
    if is_member_joined(before, after):
        to_channel = get_channel_for_message(discord, bot, member.guild.id)
        if to_channel is None:
            return
        message_text = random.choice(REGULAR_MESSAGES)
        await to_channel.send(
            f"{member.display_name} {message_text} **{after.channel.name}**!",
            delete_after=300,
        )
        # TODO: store to DB if desired (db.add_member_join_event...)


if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set.")
bot.run(TOKEN)
