import discord
from discord.ext import commands
import datetime
import os

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
PREFIX = '&'
INTENTS = discord.Intents.all()
COLOR = 0x2b2d31 

class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ System Online.")

bot = Axora()

# --- SERVER INFO COMMAND (&si) ---
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    
    # Text formatting based on your requirement
    description = (
        f"## __About {guild.name}__\n"
        f"**Name:** {guild.name}\n"
        f"**ID:** {guild.id}\n"
        f"**Owner:** 👑 {guild.owner} ({guild.owner_id})\n"
        f"**Server Created:** <t:{int(guild.created_at.timestamp())}:R>\n"
        f"**Members:** {guild.member_count}\n"
        f"**Description:** {guild.description or 'No description set.'}\n\n"
        f"## __Extra__\n"
        f"**Verification Level:** {str(guild.verification_level).title()}\n"
        f"**Upload Limit:** {guild.filesize_limit / 1024 / 1024} MB\n"
        f"**Inactive Timeout:** {guild.afk_timeout / 60} minutes\n"
        f"**System Message Channel:** {guild.system_channel.mention if guild.system_channel else 'None'}\n"
        f"**System Welcome Messages:** {'🟢 Enabled' if guild.system_channel_flags.join_notifications else '🔴 Disabled'}\n"
        f"**System Boost Messages:** {'🟢 Enabled' if guild.system_channel_flags.premium_subscription_notifications else '🔴 Disabled'}\n"
        f"**Default Notifications:** {'Only @mentions' if guild.default_notifications == discord.NotificationLevel.only_mentions else 'All Messages'}\n"
        f"**Explicit Media Content Filter:** {'🟢 Enabled' if guild.explicit_content_filter != discord.ContentFilter.disabled else '🔴 Disabled'}\n"
        f"**2FA Requirements:** {'🟢 Enabled' if guild.mfa_level == 1 else '🔴 Disabled'}"
    )

    embed = discord.Embed(description=description, color=COLOR)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.set_author(name=f"Axora™ Info System", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.name} | Founder: Xicx_", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed=embed)

# --- ANTINUKE & AUTOMOD (Buttons System Integrated) ---
# [Previous commands logic remains here...]

# --- HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Command Infrastructure", color=COLOR)
    embed.add_field(name="🛡️ **Security**", value="`antinuke`, `automod`, `whitelist (w)`")
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `purge`")
    embed.add_field(name="ℹ️ **Info**", value="`si`, `avatar`, `ping`, `userinfo` (All Updated)")
    embed.set_footer(text="Founder: Xicx_ | Axora™ Core v2.0")
    await ctx.send(embed=embed)

# --- COMMAND PROCESSOR ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
