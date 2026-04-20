import discord
from discord.ext import commands
import os

# --- CONFIG ---
TOKEN = os.getenv('TOKEN')
PREFIX = "$"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- COMMAND DATA ---
HELP_DATA = {
    "Antinuke": "🛡️ **Antinuke Module**\n`$antinuke enable`, `$antinuke disable`, `$whitelist add`, `$whitelist remove`, `$antinuke logs`",
    "Moderation": "🔨 **Moderation Module**\n`$kick`, `$ban`, `$mute`, `$unmute`, `$clear`, `$nuke`, `$lock`, `$unlock`, `$slowmode`",
    "General": "📊 **General Module**\n`$ping`, `$serverinfo`, `$userinfo`, `$avatar`, `$stats`, `$invite`, `$botinfo`",
    "Music": "🎵 **Music Module**\n`$play`, `$skip`, `$stop`, `$queue`, `$nowplaying`, `$loop`, `$volume`"
}

# --- UI COMPONENTS ---

class ModuleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Select a module to view commands", value="placeholder", emoji="⚙️"),
            discord.SelectOption(label="Antinuke", emoji="🛡️"),
            discord.SelectOption(label="Moderation", emoji="🔨"),
            discord.SelectOption(label="General", emoji="📊"),
            discord.SelectOption(label="Music & Playlists", emoji="🎵"),
        ]
        super().__init__(placeholder="Select a module to view commands", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "placeholder": return
        category = self.values[0]
        if category == "Music & Playlists": category = "Music"
        
        content = HELP_DATA.get(category, "No commands found.")
        embed = discord.Embed(description=content, color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ModuleSelect())
        # The Buttons below the Select Menu
        self.add_item(discord.ui.Button(label="Hosted On", url="https://github.com", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/pixora", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Invite Me", url=f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands" if bot.user else "https://discord.com", style=discord.ButtonStyle.link))

# --- ACTUAL WORKING COMMANDS ---

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        description=(
            "🎁 **Giveaway**\n❌ **Ignore**\n🛡️ **Antinuke**\n🔨 **Moderation**\n📊 **General**\n🎵 **Music**\n\n"
            "🔗 **[Website](https://discord.gg/pixora)**\n\n"
            "👤 **Made By Axora™ Team**"
        ),
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=HelpView())

# --- EXAMPLE COMMANDS TO PROVE THEY WORK ---
@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    new = await ctx.channel.clone()
    await ctx.channel.delete()
    await new.send("☢️ **Channel Nuked.**")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 `{round(bot.latency * 1000)}ms`")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)
