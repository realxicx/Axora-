import discord
from discord.ext import commands
import datetime
import os
import re
from discord import app_commands

# --- CONFIGURATION ---
TOKEN = os.getenv('DISCORD_TOKEN') # Pulled from GitHub Secrets
PREFIX = '&'
INTENTS = discord.Intents.all()

class PixoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

bot = PixoraBot()

# --- BUTTONS & DROPDOWN VIEW ---
class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Adding the Buttons from your image
        self.add_item(discord.ui.Button(label="Home", style=discord.ButtonStyle.secondary, emoji="🏠", custom_id="home"))
        self.add_item(discord.ui.Button(label="Commands List", style=discord.ButtonStyle.secondary, emoji="📊", custom_id="cmds"))
        self.add_item(discord.ui.Button(label="Buttons Menu", style=discord.ButtonStyle.secondary, emoji="🎛️", custom_id="buttons"))

    @discord.ui.select(
        placeholder="Choose a Category",
        options=[
            discord.SelectOption(label="Security", emoji="🛡️"),
            discord.SelectOption(label="Moderation", emoji="⚖️"),
            discord.SelectOption(label="Utility", emoji="⚙️"),
            discord.SelectOption(label="Welcomer", emoji="👋"),
        ]
    )
    async def select_callback(self, interaction, select):
        await interaction.response.send_message(f"You selected {select.values[0]}! This menu would show the specific commands for that category.", ephemeral=True)

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
    description = (
        f"`{PREFIX}help [command/category]` - View specific command/category.\n"
        "Click on the dropdown for more information.\n"
        "Total Commands: `322`" # Updated to your total
    )
    
    embed = discord.Embed(description=description, color=0x2b2d31)
    
    # ML block for arguments
    embed.add_field(name="\u200b", value="```ml\n<> - Required Argument | () - Optional Argument```", inline=False)
    
    # Categories Layout
    cat_text = (
        "> 🛡️ **[Security](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🤖 **[Automod](https://discord.gg/XKP2Qm2He3)**\n"
        "> ⚖️ **[Moderation](https://discord.gg/XKP2Qm2He3)**\n"
        "> 📜 **[Logs](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🎭 **[Customrole](https://discord.gg/XKP2Qm2He3)**\n"
        "> ⚙️ **[Utility](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🎉 **[Giveaways](https://discord.gg/XKP2Qm2He3)**\n"
        "> ⚡ **[Autoresponder](https://discord.gg/XKP2Qm2He3)**\n\n"
        "> 👋 **[Welcomer](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🔊 **[Voicemaster](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🎫 **[Ticket](https://discord.gg/XKP2Qm2He3)**\n"
        "> 📌 **[Sticky](https://discord.gg/XKP2Qm2He3)**\n"
        "> 👤 **[Selfrole](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🖼️ **[Media](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🏷️ **[Autonick](https://discord.gg/XKP2Qm2He3)**\n"
        "> 🎈 **[Fun](https://discord.gg/XKP2Qm2He3)**"
    )
    embed.add_field(name="Categories:-", value=cat_text, inline=False)
    
    # Links Section
    embed.add_field(name="🔗 Links:", value="[Support Server](https://discord.gg/XKP2Qm2He3) | [Invite Me](https://discord.gg/XKP2Qm2He3)\n[Privacy Policy](https://discord.gg/XKP2Qm2He3) | [Terms of Service](https://discord.gg/XKP2Qm2He3)", inline=False)
    
    # Footer with Requester Info
    embed.set_footer(text=f"Requested by {ctx.author} | Today at {datetime.datetime.now().strftime('%I:%M %p')}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed, view=HelpView())

# --- 322 MODERATION COMMANDS (ALIASES) ---
@bot.command(aliases=['sban', 'softban', 'b', 'hb', 'fban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    if isinstance(member, discord.Member):
        await send_mod_dm(member, "Ban", ctx.author, reason)
        await member.ban(reason=reason)
    else: await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['tmute', 'timeout', 'm', 'tm'])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str = "10m", *, reason=None):
    mins = int(re.findall(r'\d+', time)[0])
    await member.timeout(datetime.timedelta(minutes=mins), reason=reason)
    await send_mod_dm(member, "Mute", ctx.author, reason, duration=f"{mins} minutes")
    await ctx.send(f"✅ Muted {member.name}")

@bot.command(aliases=['w', 'strike'])
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await send_mod_dm(member, "Warning", ctx.author, reason)
    await ctx.send(f"⚠️ Warned {member.name}")

@bot.command(aliases=['clear', 'p'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)

# --- RUNNING ON GITHUB ---
if __name__ == "__main__":
    bot.run(TOKEN)
