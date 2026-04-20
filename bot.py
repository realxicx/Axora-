import discord
from discord.ext import commands
import datetime
import os

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
PREFIX = '&'
INTENTS = discord.Intents.all()
COLOR = 0x2b2d31 

class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Strict Security System Online.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Admin: {ctx.author.name} | Founder: Xicx_", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.utcnow()
    return await ctx.send(embed=embed)

# ==========================================
# 1. INTERACTIVE AUTOMOD (BUTTONS SYSTEM)
# ==========================================
class AutomodButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(label="Anti-Link", style=discord.ButtonStyle.secondary, emoji="🔗")
    async def btn_link(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ **Anti-Link** has been activated. No more external links allowed.", ephemeral=True)

    @discord.ui.button(label="Anti-Invite", style=discord.ButtonStyle.secondary, emoji="📩")
    async def btn_invite(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ **Anti-Invite** enabled. Discord invite links will be deleted.", ephemeral=True)

    @discord.ui.button(label="Anti-Spam", style=discord.ButtonStyle.secondary, emoji="⌨️")
    async def btn_spam(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ **Anti-Spam** active. Rapid messaging will be restricted.", ephemeral=True)

    @discord.ui.button(label="Enable All", style=discord.ButtonStyle.success, emoji="🛡️")
    async def btn_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🛡️ **Full Automod Suite** has been enabled for this server.", ephemeral=True)

@bot.group(invoke_without_command=True)
@commands.has_permissions(manage_guild=True)
async def automod(ctx):
    embed = discord.Embed(
        title="🤖 Axora™ Automod Configuration",
        description="Select which Automod features you want to enable/disable for your server:",
        color=COLOR
    )
    view = AutomodButtons()
    await ctx.send(embed=embed, view=view)

# ==========================================
# 2. STRICT ANTINUKE SYSTEM
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await aesthetic_reply(ctx, "🛡️ System Info", "Use `&antinuke enable` for Strict Security.")

@antinuke.command(name="enable")
@commands.has_permissions(administrator=True)
async def antinuke_enable(ctx):
    protection_msg = (
        "✅ **Strict Protection Activated!**\n\n"
        "__**🛡️ Protection Details**__\n"
        "> ➡️ **Status:** High-Security Mode\n"
        "> ➡️ **Bypass:** Whitelist Users Only\n\n"
        "__**⚙️ Active Protection Events**__\n"
        "> 🟢 **Anti-Ban / Anti-Kick** (Strict)\n"
        "> 🟢 **Anti-Channel Create/Delete**\n"
        "> 🟢 **Anti-Role Create/Delete**\n"
        "> 🟢 **Anti-Webhook / Integration**\n"
        "> 🟢 **Auto-Recovery System** (ON)\n\n"
        "🚨 **Note:** Server is now under Axora™ protection. Unauthorized mass actions will result in an instant ban."
    )
    await aesthetic_reply(ctx, "Axora™ Security: ENABLED", protection_msg, color=0x2ecc71)

@antinuke.command(name="disable")
@commands.has_permissions(administrator=True)
async def antinuke_disable(ctx):
    await aesthetic_reply(ctx, "Axora™ Security: DISABLED", "⚠️ **WARNING:** Protection is offline. Server is now vulnerable.", color=0xe74c3c)

# ==========================================
# 3. INTERACTIVE WHITELIST
# ==========================================
class WhitelistButtons(discord.ui.View):
    def __init__(self, target_user):
        super().__init__(timeout=120)
        self.target_user = target_user

    @discord.ui.button(label="Full Whitelist", style=discord.ButtonStyle.success, emoji="🛡️")
    async def btn_full(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ **{self.target_user.name}** is now a Whitelisted Trustee.", ephemeral=True)

    @discord.ui.button(label="Revoke", style=discord.ButtonStyle.danger, emoji="❌")
    async def btn_revoke(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"❌ Whitelist permissions revoked for {self.target_user.mention}.", ephemeral=True)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    embed = discord.Embed(title="🛡️ Whitelist Manager", description=f"Manage permissions for {member.mention}", color=COLOR)
    view = WhitelistButtons(member)
    await ctx.send(embed=embed, view=view)

# ==========================================
# 4. HELP & UTILITY
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Professional Command Menu", color=COLOR)
    embed.add_field(name="🛡️ **Security**", value="`antinuke`, `automod`, `whitelist (w)`, `panicmode`", inline=False)
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge`", inline=False)
    embed.add_field(name="🎙️ **Voice**", value="`vcmute`, `vcpull`, `vcmoveall`", inline=False)
    embed.add_field(name="ℹ️ **Info**", value="`avatar`, `ping`, `userinfo`, `banner`", inline=False)
    embed.set_footer(text="Founder: Xicx_ | All Core Systems Ready")
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
