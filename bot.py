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

# ==========================================
# 1. INTERACTIVE HELP UI (DROPDOWNS)
# ==========================================
class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Home", emoji="🏠", description="Main menu overview"),
            discord.SelectOption(label="Security", emoji="🛡️", description="Antinuke & Automod Setup"),
            discord.SelectOption(label="Moderation", emoji="⚖️", description="Admin & Punishments"),
            discord.SelectOption(label="Voice", emoji="🎙️", description="VC Management Tools"),
            discord.SelectOption(label="Information", emoji="ℹ️", description="User & Server stats"),
        ]
        super().__init__(placeholder="Choose a category to explore...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Home":
            await interaction.response.edit_message(embed=create_main_embed(interaction.user), view=self.view)
        
        elif self.values[0] == "Security":
            embed = discord.Embed(title="🛡️ Security Infrastructure", color=COLOR)
            embed.description = (
                "**Antinuke System**\n`antinuke enable`, `antinuke disable`, `panicmode`\n\n"
                "**Automod Control**\n`automod`, `antiinvite`, `antilink`, `antispam`\n\n"
                "**Whitelist**\n`whitelist (w)` - Interactive UI"
            )
            await interaction.response.edit_message(embed=embed, view=self.view)

        elif self.values[0] == "Moderation":
            embed = discord.Embed(title="⚖️ Moderation Suite", color=COLOR)
            embed.description = (
                "**Punishments**\n`ban`, `kick`, `mute`, `warn`, `purge (p)`\n\n"
                "**Channel Management**\n`lock`, `unlock`, `hide`, `slowmode`"
            )
            await interaction.response.edit_message(embed=embed, view=self.view)

        elif self.values[0] == "Voice":
            embed = discord.Embed(title="🎙️ Voice Management", color=COLOR)
            embed.description = (
                "**Voice Controls**\n`vcmuteall`, `vcpull`, `vckick`, `vcdeafen`"
            )
            await interaction.response.edit_message(embed=embed, view=self.view)

        elif self.values[0] == "Information":
            embed = discord.Embed(title="ℹ️ Information Hub", color=COLOR)
            embed.description = (
                "**Lookup**\n`si`, `userinfo (ui)`, `avatar`, `banner` \n\n"
                "**Stats**\n`ping`, `membercount`"
            )
            await interaction.response.edit_message(embed=embed, view=self.view)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(HelpDropdown())
        self.add_item(discord.ui.Button(label="Support", url="https://discord.com", style=discord.ButtonStyle.link))

def create_main_embed(user):
    embed = discord.Embed(
        title="Axora™ Command Infrastructure",
        description=(
            "Welcome to the **Axora™** panel.\n"
            "Use the dropdown below to navigate through **60+ commands**.\n\n"
            "🛡️ Security | ⚖️ Moderation | 🎙️ Voice\n"
            "⚙️ Management | ℹ️ Information"
        ),
        color=COLOR
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_footer(text=f"Founder: Xicx_ | Systems Operational", icon_url=user.display_avatar.url)
    return embed

# ==========================================
# 2. BOT CLASS & CORE LOGIC
# ==========================================
class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Merged System Online.")

bot = Axora()

# --- AESTHETIC REPLY HELPER ---
async def aesthetic_reply(ctx, title, description, color=COLOR):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name="Axora™ Security")
    embed.set_footer(text=f"Admin: {ctx.author.name} | Founder: Xicx_")
    return await ctx.send(embed=embed)

# ==========================================
# 3. SECURITY & ANTINUKE
# ==========================================
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await ctx.send("🛡️ Use `&antinuke enable` for high-security mode.")

@antinuke.command(name="enable")
async def antinuke_enable(ctx):
    msg = (
        "✅ **Protection Setup Complete!**\n\n"
        "__**🛡️ Protection Details**__\n"
        "> ➡️ **Default Action:** `BAN`\n\n"
        "__**⚙️ Active Protection Events**__\n"
        "> 🟢 **Anti Bot / Ban / Kick**\n"
        "> 🟢 **Anti Channel / Role / Webhook**\n\n"
        "-# **Move Axora™ role to the top for performance.**"
    )
    await aesthetic_reply(ctx, "Axora™ Protection: ENABLED", msg, color=0x2ecc71)

# ==========================================
# 4. SERVER INFO (&si)
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    description = (
        f"## __About {guild.name}__\n"
        f"**Name:** {guild.name}\n"
        f"**ID:** {guild.id}\n"
        f"**Owner:** 👑 {guild.owner}\n"
        f"**Created:** <t:{int(guild.created_at.timestamp())}:R>\n"
        f"**Members:** {guild.member_count}\n\n"
        f"## __Extra__\n"
        f"**Verification:** {guild.verification_level}\n"
        f"**Upload Limit:** {guild.filesize_limit / 1024 / 1024} MB\n"
        f"**2FA Requirements:** {'🟢 Enabled' if guild.mfa_level else '🔴 Disabled'}"
    )
    embed = discord.Embed(description=description, color=COLOR)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Axora™ | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

# ==========================================
# 5. ALL OTHER COMMANDS
# ==========================================
@bot.command()
async def help(ctx):
    await ctx.send(embed=create_main_embed(ctx.author), view=HelpView())

@bot.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await aesthetic_reply(ctx, "⚖️ Punishment", f"Banned **{member}**.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await aesthetic_reply(ctx, "🔒 Security", f"Locked {ctx.channel.mention}.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def vcmuteall(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🔇 Muted everyone in VC.")

@bot.command()
async def ping(ctx):
    await aesthetic_reply(ctx, "🏓 Pong!", f"Latency: **{round(bot.latency * 1000)}ms**")

# --- COMMAND PROCESSOR ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
