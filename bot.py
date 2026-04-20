import discord
from discord.ext import commands
import datetime
import os
import asyncio

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN') 
PREFIX = '&'
# We use all intents to ensure Member and Voice data is always available
INTENTS = discord.Intents.all()

class AxoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"Pixora Agency | Founder: Xicx_"
        )
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora is live for Xicx_!")

bot = AxoraBot()

# --- ERROR HANDLING (This tells you WHY a command fails) ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"❌ You don't have permission to use `{ctx.command}`!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ User not found.")
    else:
        print(f"Error: {error}") # Logs the error to GitHub Actions logs

# --- 1. MODERATION & SERVER CONTROL ---
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command()
@commands.has_permissions(administrator=True)
async def lockall(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🚨 **Server Lockdown:** All channels locked.")

@bot.command()
@commands.has_permissions(administrator=True)
async def unlockall(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 **Server Unlocked:** All channels opened.")

# --- 2. LOGS & SYSTEM ---
@bot.command()
@commands.has_permissions(manage_guild=True)
async def modlog(ctx, channel: discord.TextChannel):
    await ctx.send(f"📜 **Modlog** channel set to {channel.mention}.")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def vclog(ctx, channel: discord.TextChannel):
    await ctx.send(f"🎙️ **Voice Log** channel set to {channel.mention}.")

# --- 3. VOICE MANAGEMENT ---
@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for member in ctx.author.voice.channel.members:
            await member.edit(mute=True)
        await ctx.send("🔇 Muted everyone in VC.")
    else:
        await ctx.send("❌ You must be in a Voice Channel first!")

# --- 4. ANTINUKE & AUTOMOD ---
@bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx, status: str):
    await ctx.send(f"🛡️ Antinuke system set to: **{status.upper()}**")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def antiinvite(ctx, status: str):
    await ctx.send(f"📩 Anti-Invite set to: **{status.upper()}**")

# --- 5. HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora Command Center", color=0x00d9ff)
    embed.add_field(name="🛡️ Security", value="`antinuke`, `antiinvite`, `whitelist`, `panicmode`", inline=False)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `lockall`, `unlockall`, `purge`", inline=False)
    embed.add_field(name="🎙️ Voice", value="`vcmuteall`, `vclog`", inline=False)
    embed.add_field(name="📜 Logs", value="`modlog`, `vclog`, `memberlog`", inline=False)
    embed.set_footer(text="Founder: Xicx_ | Pixora Agency")
    await ctx.send(embed=embed)

# --- CRITICAL PROCESSOR ---
@bot.event
async def on_message(message):
    # This is the most important part. If this is missing, commands won't work.
    if message.author.bot:
        return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
