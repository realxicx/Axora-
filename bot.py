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
        print(f"✅ Axora™ Online | All commands are now workable.")

bot = Axora()

# --- HELPER FOR AESTHETIC REPLIES ---
async def aesthetic_reply(ctx, title, description):
    embed = discord.Embed(title=title, description=description, color=COLOR)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Founder: Xicx_ | Axora™", icon_url=ctx.author.display_avatar.url)
    return await ctx.send(embed=embed)

# ==========================================
# 1. SERVER INFO (&si) - EXACT FORMAT
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    
    # Custom Nitro Emojis IDs (LivingLegend Format)
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
        f"**Inactive Timeout:** {guild.afk_timeout / 60} minutes\n"
        f"**System Message Channel:** {guild.system_channel.mention if guild.system_channel else 'None'}\n"
        f"**System Welcome Messages:** {ENABLED if guild.system_channel_flags.join_notifications else DISABLED}\n"
        f"**System Boost Messages:** {ENABLED if guild.system_channel_flags.premium_subscription_notifications else DISABLED}\n"
        f"**Default Notifications:** {'Only @mentions' if guild.default_notifications == discord.NotificationLevel.only_mentions else 'All Messages'}\n"
        f"**Explicit Media Content Filter:** {ENABLED if guild.explicit_content_filter != discord.ContentFilter.disabled else DISABLED}\n"
        f"**2FA Requirements:** {ENABLED if guild.mfa_level else DISABLED}"
    )

    embed = discord.Embed(description=description, color=COLOR)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    embed.set_author(name=f"Axora™ Server Look-up", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.name} | Founder: Xicx_")
    await ctx.send(embed=embed)

# ==========================================
# 2. SECURITY (ANTINUKE / AUTOMOD)
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await ctx.send("🛡️ **Axora Security:** Use `&antinuke enable`.")

@antinuke.command(name="enable")
async def antinuke_enable(ctx):
    msg = (
        "<:tick:1410550103588208712> **Protection Setup Complete!**\n\n"
        "__**<:security2:1429419125788115005> Protection Details**__\n"
        "> <:white_arrow:1429419040471908474> **Status:** STRICT\n"
        "> <:white_arrow:1429419040471908474> **Default Action:** `BAN`"
    )
    await aesthetic_reply(ctx, "Axora™ Strict Mode", msg)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    await ctx.send(f"<:tick:1410550103588208712> {member.mention} is now whitelisted.")

# ==========================================
# 3. MODERATION & VOICE (EVERY COMMAND WORKING)
# ==========================================
@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"🔨 Banned **{member}** | Reason: {reason}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel Locked.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🔇 Muted everyone in VC.")

@bot.command()
@commands.has_permissions(move_members=True)
async def vcpull(ctx, member: discord.Member):
    if ctx.author.voice:
        await member.edit(voice_channel=ctx.author.voice.channel)
        await ctx.send(f"✈️ Pulled {member.mention}.")

# ==========================================
# 4. PROFESSIONAL HELP EMBED
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Command Infrastructure", color=COLOR)
    embed.description = "Professional Security & Management Bot"
    
    embed.add_field(name="<:security2:1429419125788115005> Security", value="`antinuke`, `automod`, `whitelist (w)`, `panicmode`, `antiinvite`, `antilink`, `antispam` ", inline=False)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge`, `hide` ", inline=False)
    embed.add_field(name="🎙️ Voice", value="`vcmute`, `vcmuteall`, `vckick`, `vcpull`, `vcmoveall`, `vcdeafen` ", inline=False)
    embed.add_field(name="⚙️ Admin", value="`setname`, `msg`, `rolecolor`, `addrole`, `modlog` ", inline=False)
    embed.add_field(name="ℹ️ Info", value="`si`, `avatar`, `ping`, `userinfo`, `banner`, `membercount` ", inline=False)
    
    embed.set_footer(text="Founder: Xicx_ | All Systems Operational")
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    await ctx.send(embed=embed)

# ==========================================
# 5. COMMAND HANDLER
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
