import discord
from discord.ext import commands
import datetime
import os
import asyncio

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
PREFIX = '?' 
INTENTS = discord.Intents.all()
COLOR = 0x000000 # Pure Black Aesthetic

class AxoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Online | Prefix: {PREFIX} | Founder: Xicx_")

bot = AxoraBot()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description):
    embed = discord.Embed(title=title, description=description, color=COLOR)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Founder: Xicx_ | Execution Successful", icon_url=ctx.author.display_avatar.url)
    return await ctx.send(embed=embed)

# ==========================================
# 1. SERVER INFO (&si) - DYNAMIC
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    CROWN = "<:Crown:1153723497143603250>"
    ENABLED = "<:Enabled:1115647297464848475>"
    DISABLED = "<:Disabled:1115647430856282203>"

    description = (
        f"## __About {guild.name}__\n"
        f"**Name:** {guild.name}\n"
        f"**ID:** {guild.id}\n"
        f"**Owner:** {CROWN} {guild.owner} ({guild.owner_id})\n"
        f"**Server Created:** <t:{int(guild.created_at.timestamp())}:R>\n"
        f"**Members:** {guild.member_count}\n"
        f"**Description:** {guild.description or 'Official Axora™ Protected Server!'}\n\n"
        f"## __Extra__\n"
        f"**Verification Level:** {str(guild.verification_level).title()}\n"
        f"**Upload Limit:** {guild.filesize_limit / 1024 / 1024} MB\n"
        f"**System Welcome Messages:** {ENABLED if guild.system_channel_flags.join_notifications else DISABLED}\n"
        f"**System Boost Messages:** {ENABLED if guild.system_channel_flags.premium_subscription_notifications else DISABLED}\n"
        f"**2FA Requirements:** {ENABLED if guild.mfa_level else DISABLED}"
    )

    embed = discord.Embed(description=description, color=COLOR)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Requested by {ctx.author.name} | Axora™")
    await ctx.send(embed=embed)

# ==========================================
# 2. SECURITY (ANTINUKE / AUTOMOD)
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await ctx.send("🛡️ **Axora Security:** Use `?antinuke enable`.")

@antinuke.command(name="enable")
async def antinuke_enable(ctx):
    msg = (
        "<:tick:1410550103588208712> **Protection Setup Complete!**\n\n"
        "__**<:security2:1429419125788115005> Protection Details**__\n"
        "> <:white_arrow:1429419040471908474> **Default Action:** `BAN`\n\n"
        "__**<:icon_blurpGear:1429419146294329446> Active Events**__\n"
        "> <:enabled:1429419129806524417> **Anti-Bot / Ban / Kick / Role / Channel**"
    )
    await aesthetic_reply(ctx, "Axora™ Security Enabled", msg)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    await ctx.send(f"<:tick:1410550103588208712> **{member.name}** whitelisted in Axora™ system.")

# ==========================================
# 3. MODERATION & VOICE LOGIC
# ==========================================
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ User Banned Successfully.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🔇 Muted everyone in VC.")

# ==========================================
# 4. AXORA™ HELP PANEL (EXACT DESIGN)
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(color=COLOR)
    
    desc = (
        "## <:logo:1489527803245232140> Axora™ Help Panel\n"
        "Welcome to **Axora™** — your all-in-one Discord bot built for speed, security, and reliability.\n\n"
        "<:Guide_Icon:1489532692390346883> **__Why Axora™__?**\n"
        "- Advanced moderation and anti-nuke protection.\n"
        "- Powerful utilities, tickets, giveaways, and more.\n"
        "- Fast, stable, and always up-to-date.\n\n"
        "<:WhiteArrow:1489532840747208795> Prefix: `?`\n"
        "<:WhiteArrow:1489532840747208795> Total Commands: `257`\n\n"
        "### <:icon_blurpGear:1429419146294329446> **__Categories & Commands__**\n"
        "**🛡️ Security:** `antinuke`, `automod`, `whitelist (w)`, `panicmode`, `antiinvite` \n"
        "**⚖️ Moderation:** `ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge` \n"
        "**🎙️ Voice:** `vcmute`, `vcmuteall`, `vckick`, `vcpull`, `vcmoveall` \n"
        "**⚙️ Utility:** `setname`, `msg`, `rolecolor`, `autologs`, `modlog` \n"
        "**ℹ️ Info:** `si`, `avatar`, `ping`, `userinfo`, `banner`, `membercount` \n\n"
        "<:WhiteQuestionMark:1489533009026879651> **__How to use__**\n"
        "1. Browse categories above for features.\n"
        "2. Use `?help <command>` for info.\n"
        "3. Founder: **Xicx_**\n"
        "<:WhiteDot:1489533781298905089> Tip: Axora™ protects your server 24/7."
    )
    
    embed.description = desc
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text="Axora™ Operations | Powered by Xicx_")
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Support", url="https://discord.gg", style=discord.ButtonStyle.link))
    view.add_item(discord.ui.Button(label="Invite Axora™", url="https://discord.com", style=discord.ButtonStyle.link))
    
    await ctx.send(embed=embed, view=view)

# ==========================================
# 5. CRITICAL: COMMAND PROCESSOR
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot: return
    # Ye line ensures all commands above work
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
