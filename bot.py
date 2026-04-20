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

# --- CATEGORY COMMAND LISTS ---
MOD_CMDS = "`ban`, `kick`, `mute`, `warn`, `unban`, `softban`, `lock`, `unlock`, `purge`"
SEC_CMDS = "`antinuke`, `automod`, `anti-spam`, `anti-link`, `lockdown`"
UTIL_CMDS = "`ping`, `stats`, `uptime`, `whois`, `userinfo`"

class HelpView(discord.ui.View):
    def __init__(self, original_embed):
        super().__init__(timeout=60)
        self.original_embed = original_embed

    @discord.ui.select(
        placeholder="Choose a Category to view commands",
        options=[
            discord.SelectOption(label="Home", emoji="🏠"),
            discord.SelectOption(label="Security", emoji="🛡️"),
            discord.SelectOption(label="Moderation", emoji="⚖️"),
            discord.SelectOption(label="Utility", emoji="⚙️"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select):
        selection = select.values[0]
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

        await interaction.response.edit_message(embed=new_embed, view=self)

class PixoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        print(f"✅ Pixora System Online: {self.user}")
        # --- PROFESSIONAL ACTIVITY ---
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"Pixora Agency | Founder: Xicx_"
        )
        await self.change_presence(status=discord.Status.online, activity=activity)

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
    cat_text = "> 🛡️ **Security**\n> ⚖️ **Moderation**\n> ⚙️ **Utility**"
    embed.add_field(name="Categories:-", value=cat_text, inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed, view=HelpView(original_embed=embed))

# --- LOCK COMMAND (&lock) ---
@bot.command(name="lock", aliases=['lockdown', 'channel-lock'])
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"🔒 **{channel.name}** has been locked successfully.")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = None # Resets to default
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"🔓 **{channel.name}** has been unlocked.")

# --- MODERATION ---
@bot.command(aliases=['b', 'sban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    if isinstance(member, discord.Member):
        await send_mod_dm(member, "Ban", ctx.author, reason)
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['m', 'tmute'])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str = "10m", *, reason=None):
    mins = int(re.findall(r'\d+', time)[0])
    await member.timeout(datetime.timedelta(minutes=mins), reason=reason)
    await send_mod_dm(member, "Mute", ctx.author, reason, duration=f"{mins} minutes")
    await ctx.send(f"✅ Muted {member.name} for {mins}m.")

# --- START ---
if __name__ == "__main__":
    bot.run(TOKEN)
