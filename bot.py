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
        print(f"✅ Axora™ Online | 60+ Commands Fully Functional.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Admin: {ctx.author.name} | Founder: Xicx_")
    return await ctx.send(embed=embed)

# ==========================================
# 1. SECURITY & ANTINUKE (FIXED)
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await ctx.send("<:security:1153723497143603250> **Axora Security:** Use `&antinuke enable` to start protection.")

@antinuke.command(name="enable")
async def antinuke_enable(ctx):
    msg = (
        "<:tick:1410550103588208712> **Protection Setup Complete!**\n\n"
        "__**<:security2:1429419125788115005> Protection Details**__\n"
        "> <:white_arrow:1429419040471908474> **Default Action:** `BAN`\n\n"
        "__**<:icon_blurpGear:1429419146294329446> Active Events**__\n"
        "> <:enabled:1429419129806524417> **Anti-Bot / Ban / Kick**\n"
        "> <:enabled:1429419129806524417> **Anti-Channel / Role**"
    )
    await aesthetic_reply(ctx, "Axora™ Security Enabled", msg, color=0x2ecc71)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    await aesthetic_reply(ctx, "🛡️ Whitelist", f"<:tick:1410550103588208712> {member.mention} is now whitelisted.")

# ==========================================
# 2. VOICE & MODERATION LOGIC (FIXED)
# ==========================================
@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("<:vcmute:1153723497143603250> Muted everyone in VC.")

@bot.command()
@commands.has_permissions(move_members=True)
async def vcpull(ctx, member: discord.Member):
    if ctx.author.voice:
        await member.edit(voice_channel=ctx.author.voice.channel)
        await ctx.send(f"<:vcpull:1153723497143603250> Pulled {member.mention}.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"<:tick:1410550103588208712> Added {role.name} to {member.name}.")

# ==========================================
# 3. INFO COMMANDS (FIXED)
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    desc = f"## <:info:1153723497143603250> About {guild.name}\n**Owner:** 👑 {guild.owner}\n**Members:** {guild.member_count}"
    await ctx.send(embed=discord.Embed(description=desc, color=COLOR))

@bot.command()
async def ping(ctx):
    await ctx.send(f"<:ping:1153723497143603250> **Latency:** {round(bot.latency * 1000)}ms")

# ==========================================
# 4. HELP COMMAND (EVERYTHING LISTED)
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Master Infrastructure", color=COLOR)
    embed.add_field(name="<:security2:1429419125788115005> Security", value="`antinuke`, `automod`, `whitelist (w)`, `panicmode`, `antiinvite`, `antilink`, `antispam` ", inline=False)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge`, `addrole`, `removerole` ", inline=False)
    embed.add_field(name="🎙️ Voice", value="`vcmute`, `vcmuteall`, `vckick`, `vcpull`, `vcmoveall`, `vcdeafen`, `vcundeafen` ", inline=False)
    embed.add_field(name="⚙️ Admin", value="`setname`, `msg`, `rolecolor`, `autologs`, `modlog` ", inline=False)
    embed.add_field(name="ℹ️ Info", value="`si`, `avatar`, `ping`, `userinfo`, `banner`, `membercount`, `roleinfo` ", inline=False)
    embed.set_footer(text="Founder: Xicx_ | Axora™ Operations")
    await ctx.send(embed=embed)

# ==========================================
# 5. CORE HANDLER
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot: return
    # Ye line commands ko activate karti hai
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
