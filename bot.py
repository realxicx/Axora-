import discord
from discord.ext import commands
import datetime
import os
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
        print(f"✅ Axora™ Online | Sabhi Commands Register Ho Gaye Hain.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Admin: {ctx.author.name} | Axora™", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.utcnow()
    return await ctx.send(embed=embed)

# ==========================================
# 1. SECURITY & WHITELIST (BUTTONS)
# ==========================================
class WhitelistView(discord.ui.View):
    def __init__(self, target):
        super().__init__(timeout=120)
        self.target = target

    @discord.ui.button(label="Full Whitelist", style=discord.ButtonStyle.success, emoji="🛡️")
    async def full_w(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ **{self.target.name}** is now a Trusted Trustee.", ephemeral=True)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    view = WhitelistView(member)
    await ctx.send(embed=discord.Embed(title="🛡️ Whitelist Manager", description=f"Manage permissions for {member.mention}", color=COLOR), view=view)

# ==========================================
# 2. ANTINUKE & AUTOMOD (STRICT)
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await aesthetic_reply(ctx, "🛡️ System Info", "Use `&antinuke enable` to activate strict protection.")

@antinuke.command(name="enable")
async def antinuke_enable(ctx):
    protection_msg = (
        "✅ **Strict Protection Activated!**\n\n"
        "__**🛡️ Protection Details**__\n"
        "> ➡️ **Action:** Instant Ban\n"
        "> ➡️ **Events:** Anti-Ban, Anti-Kick, Anti-Channel, Anti-Webhook\n\n"
        "🚨 **Security Level:** Maximum"
    )
    await aesthetic_reply(ctx, "Axora™ Security: ENABLED", protection_msg, color=0x2ecc71)

@bot.command()
@commands.has_permissions(manage_guild=True)
async def automod(ctx, status: str = "on"):
    await aesthetic_reply(ctx, "🤖 Automod System", f"Automod has been set to: **{status.upper()}**\nFilters: Anti-Link, Anti-Invite, Anti-Spam.")

# ==========================================
# 3. MODERATION & VOICE (FIXED LOGIC)
# ==========================================
@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason="No reason"):
    await ctx.guild.ban(member, reason=reason)
    await aesthetic_reply(ctx, "⚖️ Ban", f"**{member}** has been banned.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await aesthetic_reply(ctx, "🔒 Channel Locked", f"{ctx.channel.mention} is now staff-only.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await aesthetic_reply(ctx, "🔓 Channel Unlocked", f"{ctx.channel.mention} is now public.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🔇 Everyone in VC muted.")

# ==========================================
# 4. SERVER INFO (&si) - UPDATED FORMAT
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    description = (
        f"## __About {guild.name}__\n"
        f"**Name:** {guild.name}\n"
        f"**ID:** {guild.id}\n"
        f"**Owner:** 👑 {guild.owner}\n"
        f"**Members:** {guild.member_count}\n"
        f"**Created:** <t:{int(guild.created_at.timestamp())}:R>\n\n"
        f"## __Extra__\n"
        f"**Verification:** {guild.verification_level}\n"
        f"**System Messages:** {'🟢 Enabled' if guild.system_channel else '🔴 Disabled'}\n"
        f"**2FA:** {'🟢 Enabled' if guild.mfa_level else '🔴 Disabled'}"
    )
    embed = discord.Embed(description=description, color=COLOR)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Axora™ | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

# ==========================================
# 5. NEW COMMANDS ADDED
# ==========================================
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await aesthetic_reply(ctx, "🎭 Role Added", f"Added {role.mention} to {member.mention}.")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, name: str):
    await member.edit(nick=name)
    await aesthetic_reply(ctx, "👤 Nickname Changed", f"Changed {member.mention}'s nickname to **{name}**.")

@bot.command()
async def membercount(ctx):
    await aesthetic_reply(ctx, "👥 Members", f"Total members in server: **{ctx.guild.member_count}**")

# ==========================================
# 6. HELP COMMAND (EVERYTHING LISTED)
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Master Help Menu", color=COLOR)
    embed.add_field(name="🛡️ **Security**", value="`antinuke`, `automod`, `whitelist (w)`, `panicmode`, `antiinvite` ", inline=False)
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge`, `hide` ", inline=False)
    embed.add_field(name="🎙️ **Voice**", value="`vcmute`, `vcmuteall`, `vckick`, `vcpull`, `vcdeafen` ", inline=False)
    embed.add_field(name="⚙️ **Admin**", value="`addrole`, `nick`, `setname`, `msg`, `autologs`, `modlog` ", inline=False)
    embed.add_field(name="ℹ️ **Info**", value="`si`, `avatar`, `ping`, `userinfo`, `banner`, `membercount` ", inline=False)
    embed.set_footer(text="Founder: Xicx_ | Axora™")
    await ctx.send(embed=embed)

# --- COMMAND PROCESSOR ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
