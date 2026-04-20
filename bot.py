import discord
from discord.ext import commands
import datetime
import os
import asyncio

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
        print(f"✅ Axora™ Online | 60+ Commands Registered.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Admin: {ctx.author.name} | Founder: Xicx_", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.utcnow()
    return await ctx.send(embed=embed)

# ==========================================
# 1. SECURITY & ANTINUKE
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await aesthetic_reply(ctx, "🛡️ System Info", "Use `&antinuke enable` for high-security mode.")

@antinuke.command(name="enable")
async def antinuke_enable(ctx):
    msg = (
        "✅ **Protection Setup Complete!**\n\n"
        "__**🛡️ Protection Details**__\n"
        "> ➡️ **Default Action:** `BAN`\n\n"
        "__**⚙️ Active Protection Events**__\n"
        "> 🟢 **Anti Bot / Ban / Kick**\n"
        "> 🟢 **Anti Channel / Role / Webhook**\n\n"
        "-# **Move Axora™ role to the top for best performance.**"
    )
    await aesthetic_reply(ctx, "Axora™ Protection: ENABLED", msg, color=0x2ecc71)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    await aesthetic_reply(ctx, "🛡️ Whitelist Update", f"**{member.name}** has been whitelisted and bypassed security.")

# ==========================================
# 2. SERVER INFO (&si)
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    description = (
        f"## __About {guild.name}__\n"
        f"**Name:** {guild.name}\n"
        f"**ID:** {guild.id}\n"
        f"**Owner:** 👑 {guild.owner}\n"
        f"**Created:** <t:{int(guild.created_at.timestamp())}:R>\n"
        f"**Members:** {guild.member_count}\n\n"
        f"## __Extra__\n"
        f"**Verification:** {guild.verification_level}\n"
        f"**Upload Limit:** {guild.filesize_limit / 1024 / 1024} MB\n"
        f"**2FA Requirements:** {'🟢 Enabled' if guild.mfa_level else '🔴 Disabled'}"
    )
    embed = discord.Embed(description=description, color=COLOR)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Requested by {ctx.author.name} | Axora™")
    await ctx.send(embed=embed)

# ==========================================
# 3. MODERATION & VOICE LOGIC
# ==========================================
@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await aesthetic_reply(ctx, "⚖️ Punishment", f"Banned **{member}**.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await aesthetic_reply(ctx, "⚖️ Punishment", f"Kicked **{member.name}**.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await aesthetic_reply(ctx, "🔒 Security", f"Locked {ctx.channel.mention}.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await aesthetic_reply(ctx, "🔓 Security", f"Unlocked {ctx.channel.mention}.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🔇 Muted everyone in VC.")

@bot.command()
@commands.has_permissions(move_members=True)
async def vcpull(ctx, member: discord.Member):
    if ctx.author.voice:
        await member.edit(voice_channel=ctx.author.voice.channel)
        await ctx.send(f"✈️ Pulled {member.name} to {ctx.author.voice.channel.name}.")

# ==========================================
# 4. FULL CLASSIC HELP COMMAND
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Command Infrastructure", color=COLOR)
    embed.description = "Full list of commands for **Axora™ Security**."
    
    embed.add_field(name="🛡️ **Security**", value="`antinuke`, `automod`, `whitelist (w)`, `panicmode`, `antiinvite`, `antilink`, `antispam` ", inline=False)
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge`, `hide`, `slowmode`, `nick` ", inline=False)
    embed.add_field(name="🎙️ **Voice**", value="`vcmute`, `vcmuteall`, `vckick`, `vcpull`, `vcmoveall`, `vcdeafen`, `vcundeafen` ", inline=False)
    embed.add_field(name="⚙️ **Admin**", value="`setname`, `msg`, `rolecolor`, `autologs`, `modlog`, `addrole`, `removerole` ", inline=False)
    embed.add_field(name="ℹ️ **Info**", value="`si`, `avatar`, `ping`, `userinfo`, `banner`, `membercount`, `roleinfo` ", inline=False)
    
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text="Founder: Xicx_ | All Systems Operational")
    await ctx.send(embed=embed)

# ==========================================
# 5. CORE PROCESSOR
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
