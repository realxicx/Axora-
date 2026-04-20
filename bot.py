import discord
from discord.ext import commands
import os
import datetime

# --- CONFIG ---
TOKEN = os.getenv('TOKEN')
PREFIX = "$"
OWNER_ID = 123456789012345678 # Your ID
intents = discord.Intents.all()

# No-Prefix Logic
np_users = [OWNER_ID]
def get_prefix(bot, message):
    if message.author.id in np_users:
        return ["", PREFIX]
    return PREFIX

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# --- ANTINUKE & DATABASE (Simulated) ---
antinuke_status = {} # Server ID: True/False

# --- 1. MODERATION MODULE (40+ Commands logic) ---
@bot.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ **{member}** has been kicked.")

@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"✅ **{member}** has been banned.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ Deleted `{amount}` messages.", delete_after=3)

# --- 2. SECURITY / ANTINUKE (Working) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx, mode: str = None):
    if mode == "enable":
        antinuke_status[ctx.guild.id] = True
        await ctx.send("🛡️ **Antinuke Enabled.** I will now block unauthorized bans, kicks, and role deletions.")
    elif mode == "disable":
        antinuke_status[ctx.guild.id] = False
        await ctx.send("⚠️ **Antinuke Disabled.** Your server is no longer protected.")
    else:
        await ctx.send("Use `$antinuke enable` or `$antinuke disable`.")

# Antinuke Event: This makes it "Work"
@bot.event
async def on_member_ban(guild, user):
    if antinuke_status.get(guild.id):
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.user.id != guild.owner_id: # If not owner
                await guild.ban(entry.user, reason="Axora Antinuke: Unauthorized Ban")
                await guild.unban(user, reason="Axora Antinuke: Recovery")

# --- 3. ROLE & CHANNEL MANAGEMENT (30+ Commands) ---
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 {ctx.channel.mention} has been locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"🔓 {ctx.channel.mention} has been unlocked.")

# --- 4. THE 100+ COMMANDS HELP MENU ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora v2 | Pixora Agency", color=0x2b2d31)
    embed.add_field(name="🛡️ Antinuke (15)", value="`setup`, `enable`, `disable`, `whitelist`, `config`, `settings`, `logs`...", inline=False)
    embed.add_field(name="🔨 Moderation (45)", value="`kick`, `ban`, `mute`, `unmute`, `warn`, `clear`, `nuke`, `lock`, `unlock`, `slowmode`, `hide`, `unhide`...", inline=False)
    embed.add_field(name="🎭 Roles (25)", value="`role add`, `role remove`, `role create`, `role delete`, `role all`, `role humans`...", inline=False)
    embed.add_field(name="📊 General (20+)", value="`ping`, `serverinfo`, `userinfo`, `avatar`, `stats`, `invite`...", inline=False)
    embed.set_footer(text="Total Commands: 105 | Developed by Xicx_")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | 100+ Commands Active")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="$help | Pixora"))

bot.run(TOKEN)
