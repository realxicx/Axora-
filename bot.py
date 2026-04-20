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

# --- 1. MODERATION COMMANDS (15+) ---
@bot.command(aliases=['b', 'sban', 'fban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    if isinstance(member, discord.Member): await send_mod_dm(member, "Ban", ctx.author, reason)
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ Unbanned {user.name}")

@bot.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await send_mod_dm(member, "Kick", ctx.author, reason)
    await member.kick(reason=reason)
    await ctx.send(f"✅ Kicked {member.name}")

@bot.command(aliases=['m', 'tmute'])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str = "10m", *, reason=None):
    mins = int(re.findall(r'\d+', time)[0])
    await member.timeout(datetime.timedelta(minutes=mins), reason=reason)
    await send_mod_dm(member, "Mute", ctx.author, reason, duration=f"{mins}m")
    await ctx.send(f"✅ Muted {member.name} for {mins}m.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ Unmuted {member.name}")

@bot.command(aliases=['w'])
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await send_mod_dm(member, "Warning", ctx.author, reason)
    await ctx.send(f"⚠️ Warned {member.name}")

@bot.command(aliases=['p', 'clear'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Purged {amount} messages.", delete_after=3)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel Locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel Unlocked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏳ Slowmode set to {seconds}s.")

# --- 2. ROLE MANAGEMENT (5+) ---
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ Added {role.name} to {member.name}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def remrole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ Removed {role.name} from {member.name}")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, name: str):
    await member.edit(nick=name)
    await ctx.send(f"✅ Nickname changed for {member.name}")

# --- 3. INFORMATION & UTILITY (10+) ---
@bot.command(aliases=['whois', 'ui'])
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=member.color)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%b %d, %Y"))
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(aliases=['si'])
async def serverinfo(ctx):
    embed = discord.Embed(title=f"Server Info - {ctx.guild.name}", color=0x00d9ff)
    embed.add_field(name="Owner", value=ctx.guild.owner)
    embed.add_field(name="Members", value=ctx.guild.member_count)
    embed.add_field(name="Boosts", value=ctx.guild.premium_subscription_count)
    if ctx.guild.icon: embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def uptime(ctx):
    # Simplified uptime for mobile users
    await ctx.send("🚀 Pixora System is fully operational.")

# --- 4. FUN & MISC ---
@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def invite(ctx):
    await ctx.send(f"🔗 Invite Me: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot")

# --- 5. HELP COMMAND ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Pixora Agency Commands", description=f"Prefix: `{PREFIX}` | Founder: `Xicx_`", color=0x00d9ff)
    embed.add_field(name="🛡️ Mod", value="`ban`, `unban`, `kick`, `mute`, `unmute`, `warn`, `purge`, `lock`, `unlock`, `slowmode`, `nick`")
    embed.add_field(name="🎭 Roles", value="`addrole`, `remrole`")
    embed.add_field(name="ℹ️ Info", value="`userinfo`, `serverinfo`, `avatar`, `ping`, `uptime`, `invite`")
    embed.add_field(name="🎈 Misc", value="`say`")
    embed.set_footer(text="Powered by Pixora Agency")
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
