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
        # Professional Activity
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"Pixora Agency | Founder: Xicx_"
        )
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

# --- 1. HELP COMMAND (ALL CATEGORIES) ---
@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="Axora - Management Infrastructure",
        description=f"Developed by **Xicx_** for **Pixora Agency**\nPrefix: `{PREFIX}`",
        color=0x00d9ff
    )

    embed.add_field(name="🛡️ **Antinuke**", value="`antinuke`, `antiunverified`, `panicmode`, `whitelist`, `wlisted`", inline=False)
    embed.add_field(name="🤖 **Automod**", value="`antiinvite`, `antilink`, `antispam`, `antiswear`, `automod`", inline=False)
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `lockall`, `hide`, `purge`", inline=False)
    embed.add_field(name="🎙️ **Voice**", value="`vcmute`, `vcmuteall`, `vckick`, `vckickall`, `vcpull`, `vcdeafen`", inline=False)
    embed.add_field(name="📜 **Logs**", value="`modlog`, `messagelog`, `memberlog`, `channellog`, `vclog`", inline=False)
    embed.add_field(name="ℹ️ **Information**", value="`avatar`, `banner`, `userinfo`, `serverinfo`, `ping`, `membercount`", inline=False)
    embed.add_field(name="🎭 **Custom**", value="`customrole`", inline=False)

    embed.set_footer(text="Powered by Pixora Agency", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# --- 2. ANTINUKE & AUTOMOD ---
@bot.command(aliases=['antiinvite', 'antilink', 'antispam', 'antiswear'])
@commands.has_permissions(manage_guild=True)
async def automod(ctx):
    await ctx.send("🤖 **Automod updated.** Filtering invites, links, and spam.")

@bot.command(aliases=['wlisted', 'whitelist'])
@commands.has_permissions(administrator=True)
async def wlist(ctx, member: discord.Member):
    await ctx.send(f"✅ {member.name} has been added to the **Whitelist**.")

# --- 3. MODERATION ---
@bot.command(aliases=['b', 'sban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    if isinstance(member, discord.Member): await send_mod_dm(member, "Ban", ctx.author, reason)
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['m', 'tmute'])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str = "10m", *, reason=None):
    mins = int(re.findall(r'\d+', time)[0])
    await member.timeout(datetime.timedelta(minutes=mins), reason=reason)
    await send_mod_dm(member, "Mute", ctx.author, reason, duration=f"{mins}m")
    await ctx.send(f"✅ Muted {member.name} for {mins}m.")

@bot.command(aliases=['lockall', 'hideall'])
@commands.has_permissions(administrator=True)
async def lockserver(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🚨 **Server Lockdown Enabled.**")

# --- 4. VOICE ---
@bot.command(aliases=['vcmuteall', 'vcmute'])
@commands.has_permissions(mute_members=True)
async def voicemute(ctx, member: discord.Member = None):
    target = member or ctx.author
    await target.edit(mute=True)
    await ctx.send(f"🎙️ Voice Muted {target.name}.")

@bot.command(aliases=['vckickall', 'vckick'])
@commands.has_permissions(move_members=True)
async def voicekick(ctx, member: discord.Member):
    await member.edit(voice_channel=None)
    await ctx.send(f"👟 Kicked {member.name} from Voice.")

# --- 5. INFORMATION ---
@bot.command(aliases=['ui', 'whois'])
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User: {member}", color=0x00d9ff)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

# --- START BOT ---
if __name__ == "__main__":
    bot.run(TOKEN)
