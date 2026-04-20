import discord
from discord.ext import commands
import datetime
import os
import re

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN') 
PREFIX = '&'
INTENTS = discord.Intents.all()

# --- CATEGORY COMMAND LISTS ---
# Add your 322 commands into these strings below
MOD_CMDS = "`ban`, `kick`, `mute`, `warn`, `unban`, `softban`, `tempban`, `massban`, `idban`, `forceban`, `hackban`, `pban`, `fban`, `vban`, `banreason`, `banlist`, `unbanall`"
SEC_CMDS = "`antinuke`, `automod`, `anti-spam`, `anti-link`, `anti-invite`, `anti-raid`, `lockdown`, `unlockdown`"
UTIL_CMDS = "`ping`, `stats`, `uptime`, `whois`, `userinfo`, `avatar`, `banner`, `server-info`"
WELC_CMDS = "`set-welcomer`, `welcomer-test`, `welcomer-msg`, `welcomer-channel`"

class HelpView(discord.ui.View):
    def __init__(self, original_embed):
        super().__init__(timeout=None)
        self.original_embed = original_embed
        # Buttons
        self.add_item(discord.ui.Button(label="Home", style=discord.ButtonStyle.secondary, emoji="🏠", custom_id="home"))
        self.add_item(discord.ui.Button(label="Support", style=discord.ButtonStyle.link, url="https://discord.gg/XKP2Qm2He3"))

    @discord.ui.select(
        placeholder="Choose a Category to view commands",
        options=[
            discord.SelectOption(label="Home", emoji="🏠", description="Back to main menu"),
            discord.SelectOption(label="Security", emoji="🛡️", description="Antinuke & Protection"),
            discord.SelectOption(label="Moderation", emoji="⚖️", description="Punishment commands"),
            discord.SelectOption(label="Utility", emoji="⚙️", description="General tools"),
            discord.SelectOption(label="Welcomer", emoji="👋", description="Welcome settings"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select):
        selection = select.values[0]
        
        # Create a new embed based on selection
        new_embed = discord.Embed(color=0x2b2d31)
        new_embed.set_footer(text=f"Pixora Agency | Category: {selection}")

        if selection == "Home":
            await interaction.response.edit_message(embed=self.original_embed, view=self)
            return
        elif selection == "Security":
            new_embed.title = "🛡️ Security Commands"
            new_embed.description = SEC_CMDS
        elif selection == "Moderation":
            new_embed.title = "⚖️ Moderation Commands"
            new_embed.description = MOD_CMDS
        elif selection == "Utility":
            new_embed.title = "⚙️ Utility Commands"
            new_embed.description = UTIL_CMDS
        elif selection == "Welcomer":
            new_embed.title = "👋 Welcomer Commands"
            new_embed.description = WELC_CMDS

        await interaction.response.edit_message(embed=new_embed, view=self)

class PixoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        print(f"✅ Pixora System Online: {self.user}")

bot = PixoraBot()

# --- THE DM DISPATCHER ---
async def send_mod_dm(user, action, executor, reason, duration=None):
    embed = discord.Embed(title=f"Your {action} has been issued/removed in **{user.guild.name}**", color=0x2f3136)
    embed.add_field(name="**Executor:**", value=executor.name, inline=False)
    embed.add_field(name="**Reason:**", value=f"`{reason or 'No reason given'}`", inline=False)
    if duration: embed.add_field(name="**Remaining Time:**", value=duration, inline=False)
    embed.set_footer(text="Powered by Pixora Agency")
    try: await user.send(embed=embed)
    except: pass

# --- HELP COMMAND ---
@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        description=f"`{PREFIX}help [command/category]` - View specific category.\nTotal Commands: `322`", 
        color=0x2b2d31
    )
    embed.add_field(name="\u200b", value="```ml\n<> - Required Argument | () - Optional Argument```", inline=False)
    
    cat_text = (
        "> 🛡️ **[Security](https://discord.gg/XKP2Qm2He3)**\n"
        "> ⚖️ **[Moderation](https://discord.gg/XKP2Qm2He3)**\n"
        "> ⚙️ **[Utility](https://discord.gg/XKP2Qm2He3)**\n"
        "> 👋 **[Welcomer](https://discord.gg/XKP2Qm2He3)**"
    )
    embed.add_field(name="Categories:-", value=cat_text, inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed, view=HelpView(original_embed=embed))

# --- CORE MODERATION LOGIC (Ensuring these actually work) ---

@bot.command(aliases=['b', 'sban', 'pban', 'fban', 'hb', 'forceban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    if isinstance(member, discord.Member):
        await send_mod_dm(member, "Ban", ctx.author, reason)
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['tmute', 'm', 'timeout', 'tm'])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str = "10m", *, reason=None):
    # Regex to find numbers in the time string (e.g., '10m' -> 10)
    mins = int(re.findall(r'\d+', time)[0])
    duration = datetime.timedelta(minutes=mins)
    await member.timeout(duration, reason=reason)
    await send_mod_dm(member, "Mute", ctx.author, reason, duration=f"{mins} minutes")
    await ctx.send(f"✅ Muted {member.name} for {mins}m.")

@bot.command(aliases=['w', 'strike'])
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await send_mod_dm(member, "Warning", ctx.author, reason)
    await ctx.send(f"⚠️ Warned {member.name}")

@bot.command(aliases=['clear', 'p'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Purged {amount} messages.", delete_after=3)

# --- START ---
if __name__ == "__main__":
    bot.run(TOKEN)
