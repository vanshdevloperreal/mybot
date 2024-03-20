import discord
from discord.ext import commands
import requests
import pyjokes
import random
import os
import asyncio
from datetime import timedelta
from io import BytesIO  # Add this line to fix the error
import openai
from discord.ui import Button, View
import aiohttp

intents = discord.Intents.all()
#intents.typing = False
#intents.presences = False
# ticket bot setup broo

# make a token varualbe
Token = 'MTE5NDM2Nzc4Nzg2NzU4NjU5MA.GQwFe0.sXavrMHMpzoJzl24sbxn7jvmrdlJu78D_5wZZs'
bot = commands.Bot(command_prefix='v.', intents=intents)



@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  await bot.change_presence(
      activity=discord.Game(name="Prefix v. || v.Nhelp || Dm - v.i_bot, for invite bot for your server || v.Nhelp you get all command list"),
      status=discord.Status.dnd)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("****This command does not exist. Please try again.****")

@bot.command()
async def jatin(ctx):
  await ctx.send("jatin is a good boy")

@bot.command()
async def invite(ctx, *, link: str):
    link_text = "Invite NotVanshz"
    formatted_link = f"[{link_text}]('https://dsc.gg/notvanshzoffical')"
    await ctx.send(formatted_link)
  
@bot.command()
async def image(ctx, *, prompt: str):
  """Generate an image based on the provided prompt."""

  await ctx.send('Generating image...')

  try:
    response = openai.Image.create(prompt=prompt, n=1, size='1024x1024')

    image_url = response['data'][0]['url']
    image_bytes = requests.get(image_url).content
    image = discord.File(BytesIO(image_bytes), 'generated_image.png')

    await ctx.send(file=image)

  except Exception as e:
    await ctx.send(f'Error generating image: {e}')


@bot.command()
async def joke(ctx):
  try:
    # Generate a random joke using pyjokes
    joke = pyjokes.get_joke()

    # Send the joke to the Discord channel
    embed = discord.Embed(title='Random Joke',
                          description=joke,
                          color=0xe74c3c)
    await ctx.send(embed=embed)

  except Exception as e:
    print(f"Error generating joke: {e}")
    await ctx.send("Oops! Something went wrong while generating the joke.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'{member} has been banned for {reason}')


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user):
  banned_users = ctx.guild.bans()
  for ban_entry in banned_users:
    user = ban_entry.user
    if user.name == user or user.discriminator == user:
      await ctx.guild.unban(user)
      await ctx.send(f'{user} has been unbanned')
      return
  await ctx.send("User not found")


@bot.command()
async def Nhelp(ctx):
  embed = discord.Embed(title="Help",
                        description="List of commands",
                        color=0xe74c3c)
  embed.add_field(name="v.ban @user {reason}",
                  value="Ban a user from the server.",
                  inline=False)
  embed.add_field(name="v.unban @user",
                  value="Unban a user from the server.",
                  inline=False)
  embed.add_field(name="v.kick @user {reason}",
                  value="Kick a user from the server.",
                  inline=False)
  embed.add_field(name="v.timeout @user {duration}",
                  value="Timeout a user for a specified duration.",
                  inline=False)
  embed.add_field(name="v.remove_timeout @user",
                  value="Remove timeout from a user.",
                  inline=False)
  embed.add_field(name="v.image",
                  value="Generate an image based on the provided prompt.",
                  inline=False)
  embed.add_field(name="v.generate_joke",
                  value="Generate a random joke.",
                  inline=False)
  embed.add_field(name="v.avatar @user",
  value="Get Your Avatar And Your Tag User Avatar",
  inline=False)
  embed.add_field(name="v.i_bot",
  value="use for invite your bot in your server",
  inline=False)
  
  embed.add_field(name="v.nuke",
  value="****Note:- if u use missuse this command so you got ban from this bot|| This Bot Use For Clear Full Messages From Text Channel****",
  inline=False)

  embed.add_field(name="v.purge {message-value} || Like , v.purge 1",
  value="****Note:- if u use missuse this command so you got ban from this bot|| This Bot Use For Clear Jo apne jitne likhe hai Messages From Text Channel****",
  inline=False)
  embed.add_field(name="v.change_nickname @user {NickName}",
  value="# Use For Change NickName",
  inline=False)
  
  embed.add_field(name="v.Nhelp", value="Show this message.", inline=False)
  embed.add_field(name="More Feature", value="Comming Soon", inline=True)
  await ctx.send(embed=embed)

  await ctx.author.send(
      "Hello! This is a list of commands that you can use in this server:")
  await ctx.author.send(embed=embed)


@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
  # Check if the author has the Administrator permission
  if not ctx.author.guild_permissions.administrator:
    # If not, send a message and return
    await ctx.send(
        "Sorry, you need the Administrator permission to use this command.")
    return
  # Add the role to the member
  await member.add_roles(role)
  # Send a confirmation message
  await ctx.send(f"{member.mention} has been given the {role.name} role.")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  if not ctx.author.guild_permissions.kick_members and ctx.author.top_role < member.top_role:
    await ctx.send(
        f'{ctx.author.display_name}, you do not have the required permission to kick this member.'
    )
    return

  await member.kick(reason=reason)
  await ctx.send(f'{member.display_name} has been kicked.')


#make a bot author checking function

# unmute
# end unmute
# end


#1st greetings for the user| sukmadik
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mutess(ctx, user: discord.Member, duration: int, *, reason=None):
    """Times out a member from the server."""
    if not (ctx.author.permissions_in(ctx.channel) & discord.Permissions.manage_messages):
        await ctx.send("You do not have permission to use this command.")
        return

    await user.timeout(until=ctx.message.created_at + timedelta(seconds=duration), reason=reason)
    await ctx.send(f"{user.mention} has been timed out for {duration} seconds.")

@mutess.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide a user and a duration for the timeout.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Please provide a valid user.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to use this command.')

#2nd greetings for the user| NotVanshz
# add avtar
@bot.command()
async def avatar(ctx, user: discord.Member = None):
    if user is None:
      user = ctx.author
      await ctx.send("You must tag a user to get their avatar.")
    avatar_url = user.avatar.url
    download_link = f"[{user.name}'s Avatar]({avatar_url})"
    await ctx.send(download_link)
# avatar code done broo....

@bot.command()
async def i_bot(ctx):
    invite_url = "https://dsc.gg/notvanshzoffical"
    embed = discord.Embed(
        title="NotVanshz Official Bot",
        description="A powerful and feature-rich Discord bot for your server!",
        color=discord.Color.red()
    )
    embed.add_field(name="Invite Link", value=f"[Click here to invite the bot]({invite_url})", inline=False)
    embed.add_field(name="Features", value="""
        * Moderation commands
        * And much more!
        """, inline=False)
    embed.set_footer(text="Made by NotVanshz..")
    await ctx.send(embed=embed)


@bot.command()
async def nuke(ctx):
    if not isinstance(ctx.channel, discord.TextChannel):
        return await ctx.send("This command can only be used in a text channel.")

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("You do not have the required permissions to use this command.")

    await ctx.channel.purge(limit=None)
    await asyncio.sleep(1)
    await ctx.send(f"****Nuke successful!**** This command was used by {ctx.author.display_name}.")

@bot.command()
async def purge(ctx, amount: int):
    if not isinstance(ctx.channel, discord.TextChannel):
        return await ctx.send("This command can only be used in a text channel.")

    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send("You do not have the required permissions to use this command.")

    if amount > 100:
        return await ctx.send("The maximum number of messages that can be deleted at once is 100.")

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {len(deleted)} message(s).")
# giveaway code
@bot.command()
@commands.guild_only()
@commands.check(lambda ctx: ctx.author.id == ctx.guild.owner.id)
async def nuke_owner(ctx):
    for channel in ctx.guild.channels:
        await channel.delete()

    await ctx.send('Server has been nuked by the owner.')

@nuke_owner.error
async def nuke_owner_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('****You need to be the server owner to execute this command.****')


@bot.command()
async def change_nickname(ctx, member: discord.Member, *, new_nickname: str):
    if ctx.author.guild_permissions.manage_nicknames:
        try:
            await member.edit(nick=new_nickname)
            await ctx.send(f'Nickname changed for {member.mention}')
        except discord.Forbidden:
            await ctx.send('I do not have permission to change that user\'s nickname')
    else:
        await ctx.send('You do not have permission to change nicknames')



bot.run(Token)
