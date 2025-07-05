import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

REGULAR_MESSAGES = [
    "is now hanging out in",
    "has joined",
    "is chilling in",
    "jumped into",
    "entered",
    "is vibing in",
    "is now in",
]


def is_member_joined(before: discord.VoiceState, after: discord.VoiceState) -> bool:
    return before.channel is None and after.channel is not None


def get_channel_for_message(discord_mod, bot_client, guild_id):
    guild = bot_client.get_guild(guild_id)
    for ch in guild.text_channels:
        if ch.permissions_for(guild.me).send_messages:
            return ch
    return None


def main() -> None:
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        raise ValueError("DISCORD_TOKEN environment variable is not set.")

    intents = discord.Intents.default()
    intents.members = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents)

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

    bot.run(token)


if __name__ == "__main__":
    main()
