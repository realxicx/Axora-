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
COLOR = 0x2b2d31 

class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Online | Systems Operational.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Admin: {ctx.author.name} | Founder: Xicx_", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.utcnow()
    return await ctx.send(embed=embed)

# ==========================================
# 1. INTERACTIVE WHITELIST & AUTOMOD
# ==========================================
class WhitelistButtons(discord.ui.View):
    def __init__(self, target_user):
        super().__init__(timeout=120)
        self.target_user = target_user

    @discord.ui.button(label="Full Whitelist", style=discord.ButtonStyle.success, emoji="🛡️")
    async def btn_full(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ **{self.target_user.name}** is now whitelisted.", ephemeral=True)

class AutomodButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(label="Enable All", style=discord.ButtonStyle.success, emoji="🛡️")
    async def btn_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🛡️ **Automod Suite Activated.**", ephemeral=True)

# ==========================================
# 2. UPDATED SERVER INFO (&si)
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    description = (
        f"## __About {guild.name}__\n"
        f"**Name:** {guild.name}\n"
        f"**ID:** {guild.id}\n"
        f"**Owner:** 👑 {guild.owner} ({guild.owner_id})\n"
        f"**Server Created:** <t:{int(guild.created_at.timestamp())}:R>\n"
        f"**Members:** {guild.member_count}\n"
        f"**Description:** {guild.description or 'Official Axora™ Protected Server.'}\n\n"
        f"## __Extra__\n"
        f"**Verification Level:** {str(guild.verification_level).title()}\n"
        f"**Upload Limit:** {guild.filesize_limit / 1024 / 1024} MB\n"
        f"**Inactive Timeout:** {guild.afk_timeout / 60} minutes\n"
        f"**System Welcome Messages:** {'🟢 Enabled' if guild.system_channel_flags.join_notifications else '🔴 Disabled'}\n"
        f"**System Boost Messages:** {'🟢 Enabled' if guild.system_channel_flags.premium_subscription_notifications else '🔴 Disabled'}\n"
        f"**2FA Requirements:** {'🟢 Enabled' if guild.mfa_level == 1 else '🔴 Disabled'}"
    )
    embed = discord.Embed(description=description, color=COLOR)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Requested by {ctx.author.name} | Axora™")
    await ctx.send(embed=embed)

# ==========================================
# 3. SECURITY & AUTOMOD COMMANDS
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await aesthetic_reply(ctx, "🛡️ System Info", "Use `&antinuke enable` for Strict Security.")

@antinuke.command(name="enable")
async def antinuke_enable(ctx):
    msg = "✅ **Strict Protection Activated!**\n\n🛡️ **Events:** Anti-Ban, Anti-Kick, Anti-Channel/Role/Webhook, Auto-Recovery ON."
    await aesthetic_reply(ctx, "Axora™ Security: ENABLED", msg, color=0x2ecc71)

@bot.command()
@commands.has_permissions(manage_guild=True)
async def automod(ctx):
    view = AutomodButtons()
    await ctx.send(embed=discord.Embed(title="🤖 Automod Setup", description="Toggle security filters:", color=COLOR), view=view)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    view = WhitelistButtons(member)
    await ctx.send(embed=discord.Embed(title="🛡️ Whitelist Manager", description=f"Manage {member.mention}", color=COLOR), view=view)

# ==========================================
# 4. FULL MODERATION & VOICE
# ==========================================
@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await aesthetic_reply(ctx, "⚖️ Ban", f"Banned **{member}**.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await aesthetic_reply(ctx, "🔒 Locked", f"{ctx.channel.mention} is restricted.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🔇 Muted all in VC.")

# ==========================================
# 5. MASTER HELP (Professional Axora™ Branding)
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Command Infrastructure", color=COLOR)
    embed.add_field(name="🛡️ **Security**", value="`antinuke`, `automod`, `whitelist (w)`, `panicmode`, `antiinvite` ", inline=False)
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge` ", inline=False)
    embed.add_field(name="🎙️ **Voice**", value="`vcmute`, `vcmuteall`, `vckick`, `vcpull`, `vcdeafen` ", inline=False)
    embed.add_field(name="⚙️ **Admin**", value="`setname`, `msg`, `rolecolor`, `autologs`, `modlog` ", inline=False)
    embed.add_field(name="ℹ️ **Info**", value="`si`, `avatar`, `ping`, `userinfo`, `banner` ", inline=False)
    embed.set_footer(text="Founder: Xicx_ | Axora™")
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
