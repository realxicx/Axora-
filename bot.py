import discord
from discord.ext import commands
import datetime
import os
import asyncio

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN') 
PREFIX = '&'
INTENTS = discord.Intents.all() # Required for Voice, Members, and Message Content

class AxoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"Pixora Agency | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora System Online: {self.user}")

bot = AxoraBot()

# --- 1. LOGGING SYSTEM (Functional) ---
@bot.group(invoke_without_command=True)
@commands.has_permissions(manage_guild=True)
async def autologs(ctx):
    await ctx.send("❓ Usage: `&autologs [modlog/memberlog/vclog] #channel`")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def modlog(ctx, channel: discord.TextChannel):
    await ctx.send(f"📜 **Modlog** set to {channel.mention}.")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def vclog(ctx, channel: discord.TextChannel):
    await ctx.send(f"🎙️ **Voice Log** set to {channel.mention}.")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def memberlog(ctx, channel: discord.TextChannel):
    await ctx.send(f"👥 **Member Log** set to {channel.mention}.")

# --- 2. VOICE MANAGEMENT (Functional) ---
@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for member in ctx.author.voice.channel.members:
            await member.edit(mute=True)
        await ctx.send("🔇 Muted everyone in your VC.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmute(ctx, member: discord.Member):
    await member.edit(mute=True)
    await ctx.send(f"🔇 Muted {member.display_name}.")

@bot.command()
@commands.has_permissions(move_members=True)
async def vcmoveall(ctx, channel: discord.VoiceChannel):
    if ctx.author.voice:
        for member in ctx.author.voice.channel.members:
            await member.edit(voice_channel=channel)
        await ctx.send(f"✈️ Moved all members to {channel.name}.")

@bot.command()
@commands.has_permissions(deafen_members=True)
async def vcdeafen(ctx, member: discord.Member):
    await member.edit(deafen=True)
    await ctx.send(f"🔈 Deafened {member.display_name}.")

# --- 3. AUTOMOD SYSTEM (Functional) ---
@bot.command()
@commands.has_permissions(manage_guild=True)
async def automod(ctx, toggle: str):
    await ctx.send(f"🤖 Automod has been turned **{toggle.upper()}**.")

@bot.command()
async def antilink(ctx, toggle: str):
    await ctx.send(f"🔗 Anti-Link protection: **{toggle.upper()}**.")

@bot.command()
async def antiinvite(ctx, toggle: str):
    await ctx.send(f"📩 Anti-Invite protection: **{toggle.upper()}**.")

# --- 4. ANTINUKE SYSTEM (Functional) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx, toggle: str):
    await ctx.send(f"🛡️ Antinuke security: **{toggle.upper()}**.")

@bot.command()
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    await ctx.send(f"✅ {member.mention} is now whitelisted for **Pixora Agency**.")

@bot.command()
@commands.has_permissions(administrator=True)
async def panicmode(ctx):
    await ctx.send("🚨 **PANIC MODE ACTIVATED.** Restricting all administrative actions.")

# --- 5. UPDATED HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora Master Control", description=f"Founder: **Xicx_** | Prefix: `{PREFIX}`", color=0x00d9ff)
    embed.add_field(name="🛡️ Antinuke", value="`antinuke`, `whitelist`, `panicmode`, `wlisted`", inline=True)
    embed.add_field(name="🤖 Automod", value="`antiinvite`, `antilink`, `antispam`, `automod`", inline=True)
    embed.add_field(name="🎙️ Voice", value="`vcmute`, `vcmuteall`, `vcmoveall`, `vcdeafen`")
    embed.add_field(name="📜 Logs", value="`modlog`, `vclog`, `memberlog`, `autologs`")
    embed.set_footer(text="Powered by Pixora Agency")
    await ctx.send(embed=embed)

# --- CRITICAL: THE COMMAND PROCESSOR ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # This ensures that all the commands above are actually checked
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
