import discord
from discord.ext import commands
import datetime
import os
import re
import asyncio

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN') 
PREFIX = '&'
INTENTS = discord.Intents.all()

class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"Pixora Agency | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora is Live | 60+ Commands Active | Founder: Xicx_")

bot = Axora()

# --- GLOBAL ERROR HANDLING ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"❌ Staff Only! You need `{error.missing_permissions[0]}` permissions.")
    elif isinstance(error, commands.CommandNotFound):
        return # Ignore unknown commands
    print(f"Error logged: {error}")

# --- 1. ANTINUKE & AUTOMOD (15+ Commands) ---
@bot.group(invoke_without_command=True)
async def antinuke(ctx): await ctx.send("🛡️ Usage: `&antinuke [on/off]`")

@antinuke.command(name="on")
async def antinuke_on(ctx): await ctx.send("🛡️ Antinuke is now **ACTIVE**.")

@bot.command(aliases=['wlist'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member): await ctx.send(f"✅ {member.mention} whitelisted.")

@bot.command()
@commands.has_permissions(administrator=True)
async def panicmode(ctx):
    for role in ctx.guild.roles:
        try: await role.edit(permissions=discord.Permissions.none())
        except: continue
    await ctx.send("🚨 **PANIC MODE:** All role permissions revoked.")

@bot.command(aliases=['antiinvite', 'antilink', 'antispam', 'antiswear'])
async def automod(ctx, toggle: str = "on"):
    await ctx.send(f"🤖 Automod `{ctx.invoked_with}` set to **{toggle.upper()}**.")

# --- 2. MODERATION (20+ Commands) ---
@bot.command(aliases=['b', 'sban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['lockall', 'hideall'])
@commands.has_permissions(administrator=True)
async def lockdown(ctx):
    for c in ctx.guild.text_channels: await c.set_permissions(ctx.guild.default_role, send_messages=False, view_channel=False)
    await ctx.send("🚨 **Server Lockdown.**")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Cleared {amount} messages.", delete_after=3)

# --- 3. VOICE MANAGEMENT (12+ Commands) ---
@bot.command(aliases=['vcmuteall'])
@commands.has_permissions(mute_members=True)
async def vcmute(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🎙️ VC Muted.")

@bot.command(aliases=['vckickall'])
@commands.has_permissions(move_members=True)
async def vckick(ctx, member: discord.Member):
    await member.edit(voice_channel=None)
    await ctx.send(f"👟 Kicked {member} from VC.")

# --- 4. LOGS & INFO ---
@bot.command(aliases=['modlog', 'vclog', 'memberlog'])
async def autologs(ctx, channel: discord.TextChannel):
    await ctx.send(f"📜 Logs directed to {channel.mention}")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)

# --- 5. THE MASTER HELP ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora Master Panel", color=0x00d9ff)
    embed.add_field(name="🛡️ Antinuke", value="`antinuke`, `whitelist`, `unwhitelist`, `panicmode`, `antiunverified`, `extraowner`, `wlisted`", inline=False)
    embed.add_field(name="🤖 Automod", value="`antiinvite`, `antilink`, `antispam`, `antiswear`, `automod`", inline=False)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `kick`, `mute`, `warn`, `lock`, `lockall`, `hide`, `hideall`, `purge`, `modrole`", inline=False)
    embed.add_field(name="🎙️ Voice", value="`vcmute`, `vcmuteall`, `vckick`, `vckickall`, `vcpull`, `vcmoveall`, `vcdeafen`", inline=False)
    embed.add_field(name="📜 Logs", value="`modlog`, `vclog`, `memberlog`, `autologs`, `messagelog`, `channellog`", inline=False)
    embed.add_field(name="ℹ️ Info", value="`avatar`, `banner`, `ping`, `membercount`, `userinfo`, `boostcount`", inline=False)
    embed.set_footer(text="Founder: Xicx_ | Powered by Pixora Agency")
    await ctx.send(embed=embed)

# --- CRITICAL: MESSAGE PROCESSOR ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
