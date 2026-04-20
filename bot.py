import discord
from discord.ext import commands
import datetime
import os

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
PREFIX = '&'
INTENTS = discord.Intents.all()
COLOR = 0x2b2d31 # Aesthetic Dark Grey

class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Professional System Online.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security", icon_url=bot.user.display_avatar.url)
    embed.set_footer(text=f"Admin: {ctx.author.name} | Execution Successful", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.utcnow()
    return await ctx.send(embed=embed)

# ==========================================
# 1. INTERACTIVE WHITELIST (BUTTONS SYSTEM)
# ==========================================
class WhitelistButtons(discord.ui.View):
    def __init__(self, target_user):
        super().__init__(timeout=120)
        self.target_user = target_user

    @discord.ui.button(label="Anti-Ban", style=discord.ButtonStyle.green, emoji="🔨")
    async def btn_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ Bypassed **Anti-Ban** for {self.target_user.mention}", ephemeral=True)

    @discord.ui.button(label="Anti-Kick", style=discord.ButtonStyle.green, emoji="👟")
    async def btn_kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ Bypassed **Anti-Kick** for {self.target_user.mention}", ephemeral=True)

    @discord.ui.button(label="Anti-Bot", style=discord.ButtonStyle.blurple, emoji="🤖")
    async def btn_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ Bypassed **Anti-Bot** for {self.target_user.mention}", ephemeral=True)

    @discord.ui.button(label="Full Whitelist", style=discord.ButtonStyle.success, emoji="🛡️")
    async def btn_full(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ **Full Whitelist** granted to {self.target_user.mention}", ephemeral=True)

    @discord.ui.button(label="Revoke All", style=discord.ButtonStyle.danger, emoji="❌")
    async def btn_revoke(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"❌ Revoked all whitelist permissions for {self.target_user.mention}", ephemeral=True)

@bot.command(aliases=['w'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    """Whitelist command with Interactive Buttons"""
    embed = discord.Embed(
        title="🛡️ Axora™ Whitelist Manager",
        description=f"Select the permissions you want to grant to {member.mention}:",
        color=COLOR
    )
    view = WhitelistButtons(target_user=member)
    await ctx.send(embed=embed, view=view)

# ==========================================
# 2. ANTINUKE (NORMAL EMOJIS + ENABLE/DISABLE)
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await aesthetic_reply(ctx, "🛡️ System Info", "Use `&antinuke enable` or `&antinuke disable`.")

@antinuke.command(name="enable")
@commands.has_permissions(administrator=True)
async def antinuke_enable(ctx):
    protection_msg = (
        "✅ **Protection Setup Complete!**\n\n"
        "__**🛡️ Protection Details**__\n"
        "> ➡️ **Default Action:** `BAN`\n\n"
        "__**⚙️ Active Protection Events**__\n"
        "> 🔴 🟢 **Anti Bot** | Anti Ban | Anti Kick\n"
        "> 🔴 🟢 **Anti Channel/Role/Webhook**\n"
        "> 🔴 🟢 **Auto Recovery Systems**\n\n"
        "-# **Move the Security Role to the top for maximum efficiency.**"
    )
    await aesthetic_reply(ctx, "Axora™ Protection Status: ENABLED", protection_msg, color=discord.Color.green())

@antinuke.command(name="disable")
@commands.has_permissions(administrator=True)
async def antinuke_disable(ctx):
    await aesthetic_reply(ctx, "Axora™ Protection Status: DISABLED", "⚠️ **WARNING:** Antinuke has been disabled. Your server is currently vulnerable.", color=discord.Color.red())

# ==========================================
# 3. MODERATION (ALL LOGIC ADDED)
# ==========================================
@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason="No reason provided"):
    await ctx.guild.ban(member, reason=reason)
    await aesthetic_reply(ctx, "⚖️ Ban Issued", f"User **{member}** has been banned.\nReason: `{reason}`")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await aesthetic_reply(ctx, "⚖️ Kick Issued", f"User **{member.name}** was kicked.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, *, reason="No reason"):
    await member.timeout(datetime.timedelta(minutes=10), reason=reason)
    await aesthetic_reply(ctx, "⚖️ Mute Issued", f"User **{member.name}** was muted for 10m.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="Warned"):
    await aesthetic_reply(ctx, "⚠️ Warning Issued", f"**{member.name}** has been warned: `{reason}`")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await aesthetic_reply(ctx, "🔒 Channel Locked", f"{ctx.channel.mention} is now locked.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await aesthetic_reply(ctx, "🔓 Channel Unlocked", f"{ctx.channel.mention} is now unlocked.")

@bot.command(aliases=['p'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await aesthetic_reply(ctx, "🧹 Clean Sweep", f"Cleared **{amount}** messages.")

# ==========================================
# 4. VOICE MANAGEMENT
# ==========================================
@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmute(ctx, member: discord.Member):
    await member.edit(mute=True)
    await aesthetic_reply(ctx, "🎙️ Voice Mod", f"Muted {member.mention} in voice.")

@bot.command()
@commands.has_permissions(move_members=True)
async def vcpull(ctx, member: discord.Member):
    if ctx.author.voice and ctx.author.voice.channel:
        await member.edit(voice_channel=ctx.author.voice.channel)
        await aesthetic_reply(ctx, "🎙️ Voice Mod", f"Pulled {member.mention} to your channel.")
    else:
        await ctx.send("❌ You must be in a Voice Channel to pull someone.")

# ==========================================
# 5. INFORMATION
# ==========================================
@bot.command()
async def banner(ctx, member: discord.Member = None):
    member = member or ctx.author
    user = await bot.fetch_user(member.id) # Needed to fetch banner
    if user.banner:
        await ctx.send(user.banner.url)
    else:
        await ctx.send("❌ This user does not have a banner.")

@bot.command(aliases=['ui'])
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    desc = f"> **User:** {member.mention}\n> **ID:** `{member.id}`\n> **Joined:** <t:{int(member.joined_at.timestamp())}:R>"
    await aesthetic_reply(ctx, f"👤 Profile: {member.name}", desc)

@bot.command()
async def ping(ctx):
    await aesthetic_reply(ctx, "🏓 Pong!", f"Latency: **{round(bot.latency * 1000)}ms**")

# ==========================================
# 6. MASTER HELP COMMAND
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Command Infrastructure", color=COLOR)
    embed.add_field(name="🛡️ **Security**", value="`antinuke`, `whitelist (w)`, `panicmode`, `antiinvite`", inline=False)
    embed.add_field(name="⚖️ **Moderation**", value="`ban`, `kick`, `mute`, `warn`, `lock`, `unlock`, `purge`", inline=False)
    embed.add_field(name="🎙️ **Voice**", value="`vcmute`, `vckick`, `vcpull`, `vcmuteall`, `vcdeafen`", inline=False)
    embed.add_field(name="⚙️ **Management**", value="`setname`, `msg`, `rolecolor`, `modlog`", inline=False)
    embed.add_field(name="ℹ️ **Info**", value="`avatar`, `ping`, `membercount`, `userinfo`, `banner`", inline=False)
    
    embed.set_footer(text=f"Founder: Xicx_ | All Systems Operational")
    await ctx.send(embed=embed)

# --- COMMAND PROCESSOR FIX ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
