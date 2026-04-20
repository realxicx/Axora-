import discord
from discord.ext import commands
import os
import asyncio
import datetime

# --- CONFIG ---
TOKEN = os.getenv('TOKEN')
PREFIX = "$"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- 1. MODERATION COMMANDS (Logic Added) ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ **{member}** kicked | Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"✅ **{member}** banned | Reason: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ Deleted `{amount}` messages.", delete_after=3)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 {ctx.channel.mention} Locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"🔓 {ctx.channel.mention} Unlocked.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 10):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration)
    await ctx.send(f"🔇 {member} muted for {minutes}m.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member} unmuted.")

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    channel_info = [ctx.channel.name, ctx.channel.category, ctx.channel.position]
    await ctx.channel.delete()
    new_ch = await channel_info[1].create_text_channel(name=channel_info[0], position=channel_info[2])
    await new_ch.send("☢️ **Channel Nuked Successfully!**")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏳ Slowmode set to `{seconds}`s.")

# --- 2. ROLE MANAGEMENT ---
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

# --- 3. UTILITY & INFO ---
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

@bot.command()
async def serverinfo(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0x2b2d31)
    embed.add_field(name="Members", value=ctx.guild.member_count)
    embed.add_field(name="Owner", value=ctx.guild.owner)
    await ctx.send(embed=embed)

# --- 4. HELP MENU UI ---
class ModuleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Moderation", emoji="🔨"),
            discord.SelectOption(label="Antinuke", emoji="🛡️"),
            discord.SelectOption(label="Utility", emoji="📊")
        ]
        super().__init__(placeholder="Select Module", options=options)

    async def callback(self, interaction: discord.Interaction):
        cat = self.values[0]
        if cat == "Moderation":
            desc = "`kick`, `ban`, `mute`, `unmute`, `clear`, `nuke`, `lock`, `unlock`, `slowmode`, `hide`, `unhide`, `nick`"
        elif cat == "Antinuke":
            desc = "`antinuke enable`, `antinuke disable`, `whitelist add`, `whitelist remove`, `logs setup`"
        else:
            desc = "`ping`, `serverinfo`, `userinfo`, `avatar`, `stats`, `invite`, `uptime`, `botinfo`"
        
        embed = discord.Embed(title=f"{cat} Commands", description=desc, color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ModuleSelect())
        self.add_item(discord.ui.Button(label="Invite Me", url="https://discord.gg/pixora", style=discord.ButtonStyle.link))

@bot.command()
async def help(ctx):
    embed = discord.Embed(description="🛡️ **Antinuke**\n🔨 **Moderation**\n📊 **Utility**\n\n👤 **Made By Axora™ Team**", color=0x2b2d31)
    await ctx.send(embed=embed, view=HelpView())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)
