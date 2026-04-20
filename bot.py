import discord
from discord.ext import commands
import os
import datetime

# --- CONFIGURATION ---
# This line looks for the 'TOKEN' you saved in GitHub Secrets
TOKEN = os.getenv('TOKEN') 
OWNER_ID = 123456789012345678  # Replace with your actual Discord ID
DEFAULT_PREFIX = "$"

# Data Storage (Temporary)
np_users = [OWNER_ID]
maintenance_mode = False

intents = discord.Intents.all()

def get_prefix(bot, message):
    if message.author.id in np_users:
        return ["", DEFAULT_PREFIX]
    return DEFAULT_PREFIX

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# --- UI COMPONENTS ---

class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️"),
            discord.SelectOption(label="AutoMod", emoji="🤖"),
            discord.SelectOption(label="Moderation", emoji="🔨"),
            discord.SelectOption(label="General", emoji="📊"),
        ]
        super().__init__(placeholder="Select a module to view commands", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        await interaction.response.send_message(f"✨ **{category} Module** coming soon!", ephemeral=True)

class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CategorySelect())
        self.add_item(discord.ui.Button(label="Support", url="https://discord.gg/pixora", style=discord.ButtonStyle.link))

# --- COMMANDS ---

@bot.command(name="help")
async def help_command(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        description=(
            f"> **Axora - Your Multipurpose Server Bot**\n\n"
            f"- **Default Prefix:** `$`\n"
            f"- **In Server Prefix:** `{DEFAULT_PREFIX}`\n"
            f"- **Total Commands:** `510`\n"
            f"- **Latency:** `{latency} ms`\n\n"
            "```css\n"
            "<> - Required Argument | [] - Optional Argument\n"
            "```\n"
            "> 🛡️ **Antinuke** | 🤖 **AutoMod**\n"
            "> 🔨 **Moderation** | 📊 **General**\n"
            "> 🎁 **Giveaway** | 🎵 **Music**\n\n"
            "**Made By Axora™ Team**"
        ),
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=MainMenuView())

@bot.command()
@commands.is_owner()
async def maintenance(ctx, status: str):
    global maintenance_mode
    maintenance_mode = status.lower() == "on"
    await ctx.send(f"🛠️ Maintenance: **{status.upper()}**")

@bot.group(invoke_without_command=True)
@commands.is_owner()
async def np(ctx):
    await ctx.send("Use `$np add @user`.")

@np.command()
async def add(ctx, user: discord.User):
    if user.id not in np_users: np_users.append(user.id)
    await ctx.send(f"✅ Added {user.name} to NP list.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | Pixora Online")

# --- EXECUTION ---
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: No TOKEN found in Environment Variables!")
  
