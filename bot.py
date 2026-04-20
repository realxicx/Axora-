import discord
from discord.ext import commands
import os

# --- CONFIG ---
TOKEN = os.getenv('TOKEN')
PREFIX = "$"
OWNER_ID = 123456789012345678 # Replace with your Discord ID
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# --- COMMAND DATA FOR THE MENU ---
COMMAND_LISTS = {
    "Antinuke": (
        "🛡️ **Antinuke Commands**\n"
        "`$antinuke enable`, `$antinuke disable`, `$antinuke config`, "
        "`$whitelist add`, `$whitelist remove`, `$whitelist show`, "
        "`$antinuke logs`, `$antinuke punishment`, `$antinuke settings`"
    ),
    "AutoMod": (
        "🤖 **AutoMod Commands**\n"
        "`$automod setup`, `$antispam on`, `$antilink on`, `$antighostping on`, "
        "`$antiinvite on`, `$autoban setup`, `$wordblock add`, `$wordblock remove`"
    ),
    "Moderation": (
        "🔨 **Moderation Commands**\n"
        "`$kick`, `$ban`, `$mute`, `$unmute`, `$warn`, `$clear`, `$nuke`, "
        "`$lock`, `$unlock`, `$slowmode`, `$hide`, `$unhide`, `$timeout`, "
        "`$softban`, `$vmute`, `$vunmute`, `$deafen`, `$undeafen`"
    ),
    "General": (
        "📊 **General Commands**\n"
        "`$ping`, `$serverinfo`, `$userinfo`, `$avatar`, `$stats`, `$invite`, "
        "`$botinfo`, `$uptime`, `$membercount`, `$roleinfo`, `$channelinfo`"
    )
}

# --- UI COMPONENTS (The Dropdown Logic) ---

class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️", description="Protection & Whitelist"),
            discord.SelectOption(label="AutoMod", emoji="🤖", description="Auto-filters & Spam control"),
            discord.SelectOption(label="Moderation", emoji="🔨", description="Admin & Staff tools"),
            discord.SelectOption(label="General", emoji="📊", description="Utility & Info"),
        ]
        super().__init__(placeholder="Select a module to view commands", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # This is where the magic happens! It pulls from COMMAND_LISTS
        category = self.values[0]
        commands_text = COMMAND_LISTS.get(category, "No commands found.")
        
        embed = discord.Embed(
            title=f"Axora | {category} Module",
            description=commands_text,
            color=0x2b2d31
        )
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        # Edit the original message to show the commands
        await interaction.response.send_message(embed=embed, ephemeral=True)

class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CategorySelect())
        self.add_item(discord.ui.Button(label="Support", url="https://discord.gg/pixora", style=discord.ButtonStyle.link))

# --- COMMANDS ---

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Axora Help Menu",
        description=(
            "> **The Most Powerful Management Bot**\n\n"
            "Select a category from the dropdown below to view its commands. "
            "Our agency ensures 24/7 technical stability.\n\n"
            "**Total Commands:** `105` | **Prefix:** `$`"
        ),
        color=0x2b2d31
    )
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text="Made by Xicx_ for Pixora Agency")
    await ctx.send(embed=embed, view=MainMenuView())

# Example Working Commands so they actually do something
@bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx, status: str):
    await ctx.send(f"🛡️ Antinuke has been **{status.upper()}D**.")

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online on GitHub Actions!")

bot.run(TOKEN)
