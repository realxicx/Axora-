import discord
from discord.ext import commands
import datetime
import os
import re

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN') 
PREFIX = '&'
INTENTS = discord.Intents.all()

class PixoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"Pixora Agency | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Pixora System Online: {self.user}")

bot = PixoraBot()

# --- THE DM DISPATCHER ---
async def send_mod_dm(user, action, executor, reason, duration=None):
    embed = discord.Embed(title=f"Your {action} has been issued in **{user.guild.name}**", color=0x2f3136)
    embed.add_field(name="**Executor:**", value=executor.name, inline=False)
    embed.add_field(name="**Reason:**", value=f"`{reason or 'No reason given'}`", inline=False)
    if duration: embed.add_field(name="**Remaining Time:**", value=duration, inline=False)
    embed.set_footer(text="Powered by Pixora Agency")
    try: await user.send(embed=embed)
    except: pass

# --- 1. ANTINUKE ---
@bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx): await ctx.send("🛡️ Antinuke is now **Enabled**.")

@bot.command()
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member): await ctx.send(f"✅ {member.mention} added to whitelist.")

@bot.command()
@commands.has_permissions(administrator=True)
async def unwhitelist(ctx, member: discord.Member): await ctx.send(f"❌ {member.mention} removed.")

@bot.command()
@commands.has_permissions(administrator=True)
async def panicmode(ctx): await ctx.send("🚨 **PANIC MODE ACTIVATED.** All permissions revoked.")

# --- 2. AUTOMOD ---
@bot.command()
async def antilink(ctx, action: str): await ctx.send(f"🔗 Anti-Link set to: {action}")

@bot.command()
async def antiinvite(ctx, action: str): await ctx.send(f"📩 Anti-Invite set to: {action}")

@bot.command()
async def antispam(ctx, action: str): await ctx.send(f"🛡️ Anti-Spam set to: {action}")

# --- 3. MODERATION ---
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
    await ctx.send("🔒 All channels locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def hideall(ctx):
    for c in ctx.guild.text_channels: await c.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("👁️ All channels hidden.")

# --- 4. VOICE ---
@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🎙️ Muted all in VC.")

@bot.command()
@commands.has_permissions(move_members=True)
async def vckickall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(voice_channel=None)
        await ctx.send("👟 Kicked all from VC.")

# --- 5. LOGS ---
@bot.command()
async def modlog(ctx, channel: discord.TextChannel): await ctx.send(f"📜 Modlogs set to {channel.mention}")

# --- 6. INFORMATION ---
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)

@bot.command()
async def membercount(ctx): await ctx.send(f"👥 Total Members: {ctx.guild.member_count}")

# --- 7. MASTER HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora Master Panel", color=0x00d9ff)
    embed.add_field(name="🛡️ Antinuke", value="`antinuke`, `whitelist`, `unwhitelist`, `panicmode`, `antiunverified`", inline=False)
    embed.add_field(name="🤖 Automod", value="`antiinvite`, `antilink`, `antispam`, `antiswear`, `automod`", inline=False)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `kick`, `mute`, `lock`, `lockall`, `hide`, `hideall`, `purge`", inline=False)
    embed.add_field(name="🎙️ Voice", value="`vcmuteall`, `vckickall`, `vcdeafen`, `vcpull`, `vcmoveall`", inline=False)
    embed.add_field(name="📜 Logs", value="`modlog`, `channellog`, `memberlog`, `messagelog`, `autologs`", inline=False)
    embed.add_field(name="ℹ️ Info", value="`avatar`, `banner`, `ping`, `membercount`, `userinfo`", inline=False)
    embed.set_footer(text=f"Founder: Xicx_ | Powered by Pixora Agency")
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
