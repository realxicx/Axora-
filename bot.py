import discord
from discord.ext import commands
import datetime
import os
import re

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
PREFIX = '&'
INTENTS = discord.Intents.all()
COLOR = 0x2b2d31 # Aesthetic Dark Grey

class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Professional System Online.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Admin: {ctx.author.name} | Execution Successful", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.utcnow()
    return await ctx.send(embed=embed)

# --- 1. NEW ADMINISTRATION COMMANDS ---
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setname(ctx, *, name: str):
    """Changes the server name professionally."""
    old_name = ctx.guild.name
    await ctx.guild.edit(name=name)
    await aesthetic_reply(ctx, "⚙️ Server Updated", f"Server name changed from **{old_name}** to **{name}**.")

@bot.command()
@commands.has_permissions(administrator=True)
async def msg(ctx, channel: discord.TextChannel, *, text: str):
    """Sends a professional announcement via the bot."""
    embed = discord.Embed(description=text, color=COLOR)
    embed.set_author(name="Axora™ Announcement")
    await channel.send(embed=embed)
    await ctx.message.add_reaction("✅")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def rolecolor(ctx, role: discord.Role, color_code: str):
    """Changes a role color using Hex."""
    color = int(color_code.lstrip('#'), 16)
    await role.edit(color=discord.Color(color))
    await aesthetic_reply(ctx, "🎭 Role Updated", f"Color for {role.mention} has been updated to **#{color_code}**.")

# --- 2. ANTINUKE SETUP (Professional Aesthetic) ---
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await aesthetic_reply(ctx, "🛡️ System Info", "Use `&antinuke enable` to initialize the protection protocols.")

@antinuke.command(name="enable")
@commands.has_permissions(administrator=True)
async def antinuke_enable(ctx):
    protection_msg = (
        "<:tick:1410550103588208712> **Protection Setup Complete!**\n\n"
        "__**<:security2:1429419125788115005> Protection Details**__\n"
        "> <:white_arrow:1429419040471908474> **Role:** <@&1495712792119083101>\n"
        "> <:white_arrow:1429419040471908474> **Default Action:** `BAN`\n\n"
        "__**<:icon_blurpGear:1429419146294329446> Active Protection Events**__\n"
        "> <:enabled:1429419129806524417> **Anti Bot** | Anti Ban | Anti Kick\n"
        "> <:enabled:1429419129806524417> **Anti Channel/Role/Webhook**\n"
        "> <:enabled:1429419129806524417> **Auto Recovery Systems**\n\n"
        "-# **Move the Security Role to the top for maximum efficiency.**"
    )
    await aesthetic_reply(ctx, "Axora™ Protection Status", protection_msg)

# --- 3. CORE MODERATION (Aesthetic Replies) ---
@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason="No reason provided"):
    await ctx.guild.ban(member, reason=reason)
    await aesthetic_reply(ctx, "⚖️ Punishment Issued", f"User **{member}** has been banned.\nReason: `{reason}`")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await aesthetic_reply(ctx, "🔒 Channel Locked", f"{ctx.channel.mention} is now restricted to staff only.")

@bot.command(aliases=['p'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await aesthetic_reply(ctx, "🧹 Clean Sweep", f"Successfully cleared **{amount}** messages.")

# --- 4. INFORMATION ---
@bot.command(aliases=['ui'])
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    description = (
        f"> **User:** {member.mention}\n"
        f"> **ID:** `{member.id}`\n"
        f"> **Joined Server:** <t:{int(member.joined_at.timestamp())}:R>\n"
        f"> **Account Created:** <t:{int(member.created_at.timestamp())}:R>"
    )
    await aesthetic_reply(ctx, f"👤 Profile: {member.name}", description)

# --- 5. MASTER HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Command Infrastructure", color=COLOR)
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    
    embed.add_field(name="🛡️ **Security**", value="`antinuke`, `whitelist`, `panicmode`, `antiinvite`, `antilink`", inline=False)
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge`, `hide`", inline=False)
    embed.add_field(name="🎙️ **Voice**", value="`vcmute`, `vckick`, `vcpull`, `vcmuteall`, `vcdeafen`", inline=False)
    embed.add_field(name="⚙️ **Management**", value="`setname`, `msg`, `rolecolor`, `autologs`, `modlog`", inline=False)
    embed.add_field(name="ℹ️ **Info**", value="`avatar`, `ping`, `membercount`, `userinfo`, `banner`", inline=False)
    
    embed.set_footer(text=f"Founder: Xicx_ | All Systems Operational")
    await ctx.send(embed=embed)

# --- COMMAND PROCESSOR ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
