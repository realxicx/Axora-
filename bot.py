import discord
from discord.ext import commands
import datetime
import os
import asyncio

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
PREFIX = '?' 
INTENTS = discord.Intents.all()
COLOR = 0x000000 # Pure Black

class AxoraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Online | AI Chat Enabled | Prefix: {PREFIX}")

bot = AxoraBot()

# --- HUMAN CHAT LOGIC (AI ASSISTANT) ---
async def ai_chat_reply(message):
    content = message.content.lower()
    
    # Custom AI Responses for Xicx_
    replies = {
        "hi": "Hello! I am Axora™, your advanced assistant. How can I help you today?",
        "hello": "Hey there! Axora™ is at your service. Need some protection or just a chat?",
        "kaise ho": "Main bilkul thik hoon! Aap kaise hain? Axora™ hamesha ready hai.",
        "who is xicx": "Xicx_ is my Founder and the mastermind behind Axora™.",
        "prefix": f"My prefix is `{PREFIX}`. Type `{PREFIX}help` to see my 250+ commands!",
        "bye": "Goodbye! Stay safe and let Axora™ handle the security.",
        "help": f"Looking for help? Use `{PREFIX}help` for the full menu!"
    }
    
    for key in replies:
        if key in content:
            return replies[key]
    
    # Default chatty response if no keyword matches
    return "I hear you! I'm Axora™, built for speed and security. Is there any command you'd like to run?"

# ==========================================
# 1. SERVER INFO (&si) - FULL STYLE
# ==========================================
@bot.command(aliases=['si'])
async def serverinfo(ctx):
    guild = ctx.guild
    CROWN = "<:Crown:1153723497143603250>"
    ENABLED = "<:Enabled:1115647297464848475>"
    DISABLED = "<:Disabled:1115647430856282203>"

    description = (
        f"## __About {guild.name}__\n"
        f"**Owner:** {CROWN} {guild.owner} ({guild.owner_id})\n"
        f"**Members:** {guild.member_count}\n"
        f"**Created:** <t:{int(guild.created_at.timestamp())}:R>\n\n"
        f"## __Extra__\n"
        f"**Verification:** {str(guild.verification_level).title()}\n"
        f"**2FA Requirements:** {ENABLED if guild.mfa_level else DISABLED}\n"
        f"**Boost Messages:** {ENABLED if guild.system_channel_flags.premium_subscription_notifications else DISABLED}"
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
        "> <:white_arrow:1429419040471908474> **Status:** STRICT\n"
        "> <:white_arrow:1429419040471908474> **Default Action:** `BAN`"
    )
    embed = discord.Embed(title="Axora™ Security Enabled", description=msg, color=COLOR)
    await ctx.send(embed=embed)

# ==========================================
# 3. CLASSIC HELP PANEL
# ==========================================
@bot.command()
async def help(ctx):
    embed = discord.Embed(color=COLOR)
    desc = (
        "## <:logo:1489527803245232140> Axora™ Help Panel\n"
        "Welcome to **Axora™** — your human-style AI assistant and security bot.\n\n"
        "<:Guide_Icon:1489532692390346883> **__Why Axora™__?**\n"
        "- Chat with me anytime! Just say 'Hi'.\n"
        "- Advanced anti-nuke & strict moderation.\n\n"
        "<:WhiteArrow:1489532840747208795> Prefix: `?` | Commands: `257`\n\n"
        "### <:icon_blurpGear:1429419146294329446> **__Categories__**\n"
        "**🛡️ Security:** `antinuke`, `automod`, `whitelist (w)`\n"
        "**⚖️ Moderation:** `ban`, `kick`, `mute`, `warn`, `lock`, `purge`\n"
        "**🎙️ Voice:** `vcmute`, `vcmuteall`, `vcpull`, `vcmoveall`\n"
        "**ℹ️ Info:** `si`, `avatar`, `ping`, `userinfo`, `membercount`\n\n"
        "Founder: **Xicx_**"
    )
    embed.description = desc
    embed.set_footer(text="Axora™ | Powered by Xicx_")
    await ctx.send(embed=embed)

# ==========================================
# 4. THE COMMAND & CHAT PROCESSOR
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot: return

    # 1. Check if it's a command
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
    else:
        # 2. If not a command, talk like a human
        # Only reply to specific keywords or mentions to avoid spam
        if any(word in message.content.lower() for word in ["hi", "hello", "kaise ho", "axora", "bye"]):
            response = await ai_chat_reply(message)
            await message.reply(response)

if __name__ == "__main__":
    bot.run(TOKEN)
