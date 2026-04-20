import discord
from discord.ext import commands
import os
import datetime

# --- CONFIG ---
TOKEN = os.getenv('TOKEN')
PREFIX = "$"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- COMMAND DATA ---
HELP_DATA = {
    "Antinuke": "🛡️ **Antinuke Module**\n`$antinuke enable`, `$antinuke disable`, `$whitelist add`, `$antinuke logs`",
    "Moderation": "🔨 **Moderation Module**\n`$kick`, `$ban`, `$mute`, `$unmute`, `$clear`, `$nuke`, `$lock`, `$unlock`, `$slowmode`",
    "General": "📊 **General Module**\n`$ping`, `$serverinfo`, `$userinfo`, `$avatar`, `$stats`, `$invite`"
}

# --- UI COMPONENTS ---

class ModuleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️"),
            discord.SelectOption(label="Moderation", emoji="🔨"),
            discord.SelectOption(label="General", emoji="📊"),
        ]
        super().__init__(placeholder="Select a module to view commands", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        content = HELP_DATA.get(category, "No commands found.")
        embed = discord.Embed(description=content, color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ModuleSelect())
        self.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/pixora", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Invite Me", url="https://discord.com/api/oauth2/authorize?client_id=1230154030616182815&permissions=8&scope=bot", style=discord.ButtonStyle.link))

# --- ACTUAL WORKING LOGIC ---

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        description=(
            "🛡️ **Antinuke**\n🔨 **Moderation**\n📊 **General**\n\n"
            "👤 **Made By Axora™ Team**"
        ),
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=HelpView())

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ **{member}** has been kicked.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"✅ **{member}** has been banned.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ Deleted `{amount}` messages.", delete_after=3)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 {ctx.channel.mention} is now locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"🔓 {ctx.channel.mention} is now unlocked.")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Latency: `{round(bot.latency * 1000)}ms`")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)
