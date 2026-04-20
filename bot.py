import discord
from discord.ext import commands
import os

# --- CONFIG ---
TOKEN = os.getenv('TOKEN')
PREFIX = "$"
OWNER_ID = 123456789012345678 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- COMMAND DATA ---
COMMANDS_MAP = {
    "Antinuke": "🛡️ **Antinuke Module**\n`setup`, `enable`, `disable`, `whitelist`, `config`, `settings`, `logs`, `punishment`, `trust`, `untrust`...",
    "AutoMod": "🤖 **AutoMod Module**\n`automod setup`, `antispam on`, `antilink on`, `antighostping on`, `antiinvite on`, `autoban`, `wordblock`...",
    "Moderation": "🔨 **Moderation Module**\n`kick`, `ban`, `mute`, `unmute`, `warn`, `clear`, `nuke`, `lock`, `unlock`, `slowmode`, `hide`, `unhide`...",
    "General": "📊 **General Module**\n`ping`, `serverinfo`, `userinfo`, `avatar`, `stats`, `invite`, `botinfo`, `uptime`, `membercount`..."
}

# --- UI COMPONENTS ---

class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️"),
            discord.SelectOption(label="AutoMod", emoji="🤖"),
            discord.SelectOption(label="Moderation", emoji="🔨"),
            discord.SelectOption(label="General", emoji="📊"),
        ]
        super().__init__(placeholder="Click here to view commands...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # This replaces the "commands are being loaded" message with the real list
        category = self.values[0]
        cmd_text = COMMANDS_MAP.get(category)
        
        embed = discord.Embed(description=cmd_text, color=0x2b2d31)
        embed.set_author(name=f"{category} Commands", icon_url=interaction.user.display_avatar.url)
        
        # This sends a clean, private message with the commands
        await interaction.response.send_message(embed=embed, ephemeral=True)

class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CategorySelect())
        self.add_item(discord.ui.Button(label="Support", url="https://discord.gg/pixora", style=discord.ButtonStyle.link))

# --- HELP COMMAND ---

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Axora v2 | Pixora Agency",
        description=(
            "Welcome to the official **Axora** management interface.\n"
            "Use the dropdown below to explore our **100+ commands**.\n\n"
            "**Total Commands:** `105` | **Prefix:** `$`"
        ),
        color=0x2b2d31
    )
    embed.set_footer(text="Developed by Xicx_ • Pixora 2026")
    await ctx.send(embed=embed, view=MainMenuView())

# --- EVENTS ---

@bot.event
async def on_ready():
    print(f"Axora is running on GitHub Actions!")
    await bot.change_presence(activity=discord.Game(name="$help | Xicx_"))

bot.run(TOKEN)
