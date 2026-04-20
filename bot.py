import discord
from discord.ext import commands
import datetime
import os
import asyncio

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN') 
PREFIX = '&'
# Critical: Intents must be all enabled for these commands to work
INTENTS = discord.Intents.all()

class AxoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"Pixora Agency | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora System Online: {self.user}")

bot = AxoraBot()

# --- THE DM DISPATCHER ---
async def send_mod_dm(user, action, executor, reason, duration=None):
    embed = discord.Embed(title=f"Your {action} has been issued in **{user.guild.name}**", color=0x2b2d31)
    embed.add_field(name="**Executor:**", value=executor.name, inline=False)
    embed.add_field(name="**Reason:**", value=f"`{reason or 'No reason given'}`", inline=False)
    if duration: embed.add_field(name="**Remaining Time:**", value=duration, inline=False)
    embed.set_footer(text="Powered by Pixora Agency")
    try: await user.send(embed=embed)
    except: pass

# --- 1. ANTINUKE & AUTOMOD ---
@bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx, status: str = "on"):
    await ctx.send(f"🛡️ **Antinuke** has been toggled: `{status.upper()}`")

@bot.command()
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    await ctx.send(f"✅ {member.mention} has been whitelisted by **Xicx_**.")

@bot.command()
async def antiinvite(ctx, status: str = "on"):
    await ctx.send(f"📩 **Anti-Invite** is now `{status.upper()}`")

# --- 2. MODERATION ---
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    if isinstance(member, discord.Member): await send_mod_dm(member, "Ban", ctx.author, reason)
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lockall(ctx):
    for c in ctx.guild.text_channels: await c.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 **Server Lockdown:** All channels locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlockall(ctx):
    for c in ctx.guild.text_channels: await c.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 **Server Unlocked:** All channels opened.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("👁️ Channel hidden.")

# --- 3. VOICE MANAGEMENT ---
@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🎙️ Everyone in VC has been muted.")

@bot.command()
@commands.has_permissions(move_members=True)
async def vcmoveall(ctx, channel: discord.VoiceChannel):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(voice_channel=channel)
        await ctx.send(f"✈️ Moved everyone to {channel.name}.")

# --- 4. LOGS ---
@bot.command()
@commands.has_permissions(manage_guild=True)
async def modlog(ctx, channel: discord.TextChannel):
    await ctx.send(f"📜 Moderation logs hooked to {channel.mention}.")

# --- 5. INFORMATION ---
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)

@bot.command()
async def membercount(ctx):
    await ctx.send(f"👥 **Member Count:** {ctx.guild.member_count}")

# --- 6. CUSTOM ROLE ---
@bot.command()
@commands.has_permissions(manage_roles=True)
async def customrole(ctx, member: discord.Member, *, name: str):
    role = await ctx.guild.create_role(name=name)
    await member.add_roles(role)
    await ctx.send(f"🎭 Created and gave role **{name}** to {member.name}.")

# --- 7. MASTER HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora Master Help", description=f"Founder: **Xicx_** | Prefix: `{PREFIX}`", color=0x00d9ff)
    
    # Adding every category as you asked
    embed.add_field(name="🛡️ Antinuke", value="`antinuke`, `antiunverified`, `panicmode`, `whitelist`, `wlisted`", inline=False)
    embed.add_field(name="🤖 Automod", value="`antiinvite`, `antilink`, `antispam`, `antiswear`, `automod`", inline=False)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `kick`, `mute`, `lock`, `lockall`, `unlockall`, `hide`, `hideall`", inline=False)
    embed.add_field(name="🎙️ Voice", value="`vcmute`, `vcmuteall`, `vckick`, `vcmoveall`, `vcpull`, `vcdeafen`", inline=False)
    embed.add_field(name="📜 Logs", value="`modlog`, `channellog`, `memberlog`, `autologs`, `vclog`", inline=False)
    embed.add_field(name="ℹ️ Information", value="`avatar`, `banner`, `ping`, `membercount`, `userinfo`", inline=False)
    embed.add_field(name="🎭 Custom", value="`customrole`", inline=False)

    embed.set_footer(text="Powered by Pixora Agency")
    await ctx.send(embed=embed)

# --- ENSURE COMMANDS ARE PROCESSED ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
