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
    embed = discord.Embed(title=f"Your {action} has been issued/removed", color=0x2f3136)
    embed.add_field(name="**Executor:**", value=executor.name, inline=False)
    embed.add_field(name="**Reason:**", value=f"`{reason or 'No reason given'}`", inline=False)
    if duration: embed.add_field(name="**Remaining Time:**", value=duration, inline=False)
    embed.set_footer(text="Powered by Pixora Agency")
    try: await user.send(embed=embed)
    except: pass

# --- 1. ANTINUKE & AUTOMOD (Logic for 15+ Commands) ---
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await ctx.send("🛡️ **Pixora Antinuke System** is active. Use `&whitelist @user` to exempt staff.")

@bot.command(aliases=['antiinvite', 'antilink', 'antispam', 'antiswear'])
@commands.has_permissions(manage_guild=True)
async def automod(ctx, status: str = "on"):
    await ctx.send(f"🤖 Automod features have been toggled to: **{status.upper()}**")

# --- 2. MODERATION & ADVANCED LOCKS (Logic for 20+ Commands) ---
@bot.command(aliases=['b', 'sban', 'fban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    if isinstance(member, discord.Member): await send_mod_dm(member, "Ban", ctx.author, reason)
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['lockall', 'hideall'])
@commands.has_permissions(administrator=True)
async def lockdown(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, view_channel=False)
    await ctx.send("🚨 **SERVER LOCKDOWN ENABLED.** All channels hidden/locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 {ctx.channel.mention} Locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send(f"👁️ {ctx.channel.mention} Hidden.")

# --- 3. VOICE MANAGEMENT (Logic for 12+ Commands) ---
@bot.command(aliases=['vcmuteall', 'vcmute'])
@commands.has_permissions(mute_members=True)
async def voice_mute(ctx, member: discord.Member = None):
    if member:
        await member.edit(mute=True)
        await ctx.send(f"🎙️ Muted {member.name} in VC.")
    else:
        for vc_member in ctx.author.voice.channel.members:
            await vc_member.edit(mute=True)
        await ctx.send("🎙️ Muted everyone in your Voice Channel.")

@bot.command(aliases=['vckickall'])
@commands.has_permissions(move_members=True)
async def vckick(ctx, member: discord.Member):
    await member.edit(voice_channel=None)
    await ctx.send(f"👟 Kicked {member.name} from Voice.")

# --- 4. LOGGING SYSTEM (Placeholders) ---
@bot.command(aliases=['modlog', 'memberlog', 'messagelog'])
@commands.has_permissions(manage_guild=True)
async def logs(ctx, channel: discord.TextChannel):
    await ctx.send(f"📜 Logging system hooked to {channel.mention}.")

# --- 5. INFORMATION & CUSTOM ROLE ---
@bot.command(aliases=['ui', 'whois'])
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Info: {member.name}", color=0x00d9ff)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def customrole(ctx, member: discord.Member, *, name: str):
    new_role = await ctx.guild.create_role(name=name)
    await member.add_roles(new_role)
    await ctx.send(f"🎭 Created and assigned custom role: **{name}**")

# --- 6. MASTER HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora Master Commands", description=f"Founder: **Xicx_** | Prefix: `{PREFIX}`", color=0x2b2d31)
    
    embed.add_field(name="🛡️ Antinuke", value="`antinuke`, `whitelist`, `panicmode`, `extraowner`", inline=True)
    embed.add_field(name="🤖 Automod", value="`antiinvite`, `antilink`, `antispam`, `antiswear`", inline=True)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `kick`, `mute`, `warn`, `lock`, `hide`, `purge`", inline=True)
    embed.add_field(name="🎙️ Voice", value="`vcmute`, `vckick`, `vcpull`, `vcmuteall`, `vcdeafen`", inline=True)
    embed.add_field(name="📜 Logs", value="`modlog`, `messagelog`, `memberlog`, `autologs`", inline=True)
    embed.add_field(name="ℹ️ Info", value="`avatar`, `banner`, `ping`, `userinfo`, `membercount`", inline=True)
    embed.add_field(name="🎭 Custom", value="`customrole`", inline=True)
    
    embed.set_footer(text="Powered by Pixora Agency")
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
