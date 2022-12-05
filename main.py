import discord
from discord.ext import commands
from discord.ext.commands import check
import datetime
import time
import os
import random
from urllib import parse, request
import re
import requests
import json
import flag
import math
import pycountry
from keep_alive import keep_alive
from PIL import Image, ImageFont, ImageDraw
from tabulate import tabulate
from apifunc import *
from formattingfunc import *
from DBqueries import *

#set up the global prefix for bot commands
intents = discord.Intents.default()
intents.members = True

global_prefix = '^'
bot = commands.Bot(
 command_prefix=global_prefix,
 description=
 f"With the prefix {global_prefix} you are able to use following commands \n *optional",
 intents=intents)


#BOT COMMANDS
#the following bot commands are triggered if message sent by a user consists of the prefix followed by the command function name.
# For example, to trigger the serverinfo function, it would be   "   ^serverinfo    "
#some commands can
@bot.command(aliases=['leaderboard'])
async def lb(ctx):
	"""
	Returns server leaderboard: lb
	"""

	#get data from mee6s leaderboard
	URL = 'https://mee6.xyz/api/plugins/levels/leaderboard/739175633673781259'

	res = requests.get(URL)
	for count, item in enumerate(res.json()['players']):
		name = item['username']
		id_user = item['id']
		discriminator = item['discriminator']
		level = item['level']
		msg_count = item['message_count']
		xp = item['xp']

	#Structuring the embed message using the data obtained from mee6s website
	embed = discord.Embed(
	 description="[Leaderboard](https://mee6.xyz/leaderboard/739175633673781259)",
	 timestamp=ctx.message.created_at,
	 color=discord.Color.red())

	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")

	#create fields for the top 10
	for count, item in enumerate(res.json()['players']):
		nickname = item['username']
		discriminator = item['discriminator']
		level = item['level']
		xp = item['xp']
		if count < 10:  #how many ppl the leaderboard shows
			rank = count + 1
			embed.add_field(name=f"#{rank}   {nickname}#{discriminator}",
			                value=f"LEVEL {level}       |        {xp} XP",
			                inline=False)

	await ctx.send(embed=embed)


@bot.command(aliases=['ui'])
async def userinfo(ctx, member: discord.Member = None):
	"""
	Returns information about a user: userinfo *@user
	"""

	if member == None:
		member = ctx.author

	rlist = []  #list of all the roles the user has
	for role in member.roles:
		if role.name != "@everyone":
			rlist.append(role.mention)

	b = " ".join(rlist)  #format the list

	embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

	embed.set_author(icon_url=member.avatar_url,
	                 name=f"{member}   •   {member.id}"),
	embed.set_thumbnail(url=member.avatar_url),
	embed.add_field(name='Name', value=member.mention, inline=True)
	#embed.add_field(name='Booster', value=f'{("Yes" if member.premium_since else "No")}',inline=True)

	try:
		name = remove_hashtag(str(member))
		level, rank, xp, msg_count = get_level(name)

		embed.add_field(name='Level', value=level, inline=True)
		embed.add_field(name='Rank', value=f"#{rank}", inline=True)
		#embed.add_field(name='XP',value=xp,inline=True)
		#embed.add_field(name='Msg Count', value=msg_count,inline=True)
	except Exception as e:
		print(str(e))

	embed.add_field(name=f'Roles ({len(rlist)})',
	                value=''.join([b]),
	                inline=False)
	#embed.add_field(name='Top Role:',value=member.top_role.mention,inline=False)
	embed.add_field(name='Joined',
	                value=f'{str(member.joined_at)[:16]}',
	                inline=True)
	embed.add_field(name='Registered',
	                value=f'{str(member.created_at)[:16]}',
	                inline=True)

	#embed.set_footer(text=f'Requested by - {ctx.author}',
	#icon_url=ctx.author.avatar_url)

	await ctx.send(embed=embed)

@bot.command()
async def oldestmember(ctx, num=3):
	"""
	Returns the oldest members of the server.: oldestmember [number of users]
	"""

	member_list = {}
	for guild in bot.guilds:
		for member in guild.members:
			if not member.bot:
				member_name = str(member.name) + "#" + str(member.discriminator)
				member_register = str(member.joined_at)[:16]
				member_list[member_name] = member_register
	sorted_list = sorted(member_list.items(), key=lambda x: x[1])
	embed = discord.Embed(
	 title='Oldest B40 Members',
	 timestamp=ctx.message.created_at,
	 description="Leaderboard of the discord users with oldest B40 members",
	 color=discord.Color.red())
	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
	for data in sorted_list[:num]:
		embed.add_field(name=data[0], value=data[1], inline=False)
	await ctx.send(embed=embed)


@bot.command()
async def oldestuser(ctx, num=3):
	"""
	Returns the oldest discord users of the server.: oldestuser [number of users]
	"""

	member_list = {}
	for guild in bot.guilds:
		for member in guild.members:
			if not member.bot:
				member_name = str(member.name) + "#" + str(member.discriminator)
				member_register = str(member.created_at)[:16]
				member_list[member_name] = member_register
	sorted_list = sorted(member_list.items(), key=lambda x: x[1])
	embed = discord.Embed(
	 title='B40 Oldest Discord Users',
	 timestamp=ctx.message.created_at,
	 description="Leaderboard of the discord users with oldest registration date",
	 color=discord.Color.red())
	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
	for data in sorted_list[:num]:
		embed.add_field(name=data[0], value=data[1], inline=False)
	await ctx.send(embed=embed)


@bot.command(aliases=['ma'])
async def moveall(ctx: commands.Context):
	if ctx.author.guild_permissions.kick_members:
		for voice_channel in ctx.guild.voice_channels:
			if voice_channel is ctx.author.voice.channel:
				print(voice_channel)
				continue
			for x in voice_channel.members:
				print(x.name)
				await x.move_to(ctx.author.voice.channel)


@bot.command()
async def serverinfo(ctx):
	"""
    Returns information about the server: serverinfo
    """

	guild = ctx.guild
	embed = discord.Embed(title='B40',
	                      description="Community for autistic, depressed people",
	                      timestamp=ctx.message.created_at,
	                      color=discord.Color.red())
	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
	embed.add_field(name="Owner", value="blacky#5204")
	embed.add_field(name="Server ID", value=guild.id)
	embed.add_field(name="Members", value=guild.member_count)
	embed.add_field(name="Channels", value=len(guild.channels))
	embed.add_field(name="Roles", value=len(guild.roles))
	embed.add_field(name="Boosters", value=guild.premium_subscription_count)
	embed.add_field(name="Created on",
	                value=str(guild.created_at.strftime("%b %d, %Y"))[:16])
	embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

	await ctx.send(embed=embed)


@bot.command()
async def quote(ctx):
	"""
	sends a random quote
	"""

	r_quote = get_quote()
	await ctx.send(r_quote)


@bot.command()
async def country(ctx, *, args):
	"""
    Returns extensive stats of a country: country [country name]
    """

	flag_icon, c_name_s, c_name_l, capital, curr_name, currr_symbol, language_list, flag_data, popu_short, area_short, region, region_s = country_api(
	 args)
	shord_field = c_name_s + " " + flag_icon

	embed = discord.Embed(title=c_name_l,
	                      description=f"Country in {region}",
	                      timestamp=ctx.message.created_at,
	                      color=discord.Color.red())
	embed.set_thumbnail(url=flag_data)

	embed.add_field(name="Name:", value=c_name_l)
	embed.add_field(name="Capital:", value=capital)
	embed.add_field(name="Short:", value=shord_field)
	embed.add_field(name="Area:", value=area_short)
	embed.add_field(name="Continent:", value=region_s)
	embed.add_field(name="Population:", value=popu_short)
	embed.add_field(name="Currency:", value=curr_name)
	embed.add_field(name="Symbol:", value=currr_symbol)
	embed.add_field(name="Language(s):", value=language_list)
	embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

	await ctx.send(embed=embed)


@bot.command()
async def weather(ctx, *, args):
	"""
    Returns weather stats of a location: weather [location]
    """

	try:
		weather_icon_url, country_name, country, country_icon, humidity, wind, temp_celsius, temp_fahrenheit, weather_description = weather_api(
		 args)

		country_field = country + " " + country_icon

		embed = discord.Embed(title=args.capitalize(),
		                      description=f"A place in {country_name}",
		                      timestamp=ctx.message.created_at,
		                      color=discord.Color.red())
		embed.set_thumbnail(url=weather_icon_url)

		embed.add_field(name="Country:", value=country_field)
		embed.add_field(name="Humidity:", value=humidity)
		embed.add_field(name="Wind:", value=wind)
		embed.add_field(name="Temp.:", value=temp_celsius)
		embed.add_field(name="Temp.:", value=temp_fahrenheit)
		embed.add_field(name="Weather:", value=weather_description)
		embed.set_footer(text=f"Used by {ctx.author}",
		                 icon_url=ctx.author.avatar_url)

		await ctx.send(embed=embed)
	except:
		pass


@bot.command()
async def word(ctx, *, args):
	"""
    Returns dictionary-entry of a word: word [word]
    """

	word, phonetic, word_type, definition, example, list_of_synonyms = dictionary(
	 args)

	embed = discord.Embed(title=word,
	                      description=definition,
	                      timestamp=ctx.message.created_at,
	                      color=discord.Color.red())
	embed.set_thumbnail(
	 url=
	 "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Flag_of_the_United_Kingdom.svg/640px-Flag_of_the_United_Kingdom.svg.png"
	)

	embed.add_field(name="Type:", value=word_type)
	embed.add_field(name="Phonetic:", value=phonetic)
	embed.add_field(name="Synonyms:", value=list_of_synonyms)
	embed.add_field(name="Example:", value=example)

	embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

	await ctx.send(embed=embed)


@bot.command()
async def omri(ctx):
	"""
	Returns an important piece of information about Omri
	"""

	await ctx.send("Omri is the 4x Consecutive Holder of the "
	               'Funniest Person In B40'
	               " Title.")


@bot.command()
async def hug(ctx, *, user: discord.Member = None):
	"""
	Returns hug gif: hug @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} sends hugs to {user.name}")
	embed.set_image(url=tenor("anime-hugs"))

	await ctx.send(embed=embed)


@bot.command()
async def kiss(ctx, *, user: discord.Member = None):
	"""
	Returns kiss gif: kiss @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} sends kisses to {user.name}")
	embed.set_image(url=tenor("anime-kiss"))

	await ctx.send(embed=embed)


@bot.command()
async def kill(ctx, *, user: discord.Member = None):
	"""
	Returns kill gif: kill @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} kills {user.name}")
	embed.set_image(url=tenor("among-us-kill"))

	await ctx.send(embed=embed)


@bot.command()
async def slap(ctx, *, user: discord.Member = None):
	"""
	Returns slap gif: slap @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} slaps {user.name}")
	embed.set_image(url=tenor("anime-slap"))

	await ctx.send(embed=embed)


@bot.command()
async def cringe(ctx, *, user: discord.Member = None):
	"""
	Returns cringe gif: cringe @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} cringes at {user.name}")
	embed.set_image(url=tenor("cringe"))

	await ctx.send(embed=embed)


@bot.command()
async def punch(ctx, *, user: discord.Member = None):
	"""
	Returns punch gif: punch @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} punches {user.name}")
	embed.set_image(url=tenor("anime-punch"))

	await ctx.send(embed=embed)


@bot.command()
async def kick(ctx, *, user: discord.Member = None):
	"""
	Returns kick gif: kick @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} kicks {user.name}")
	embed.set_image(url=tenor("anime-kick"))

	await ctx.send(embed=embed)


@bot.command()
async def penis(ctx, *, user: discord.Member = None):
	"""
	Returns penis stats of user: penis @user
	"""

	if user.id == 283715405934231552:  #ahzee
		penis = "8==D"
	elif user.id == 126077599465078785:  #omri
		penis = "8======================================D"
	elif user.id == 730601680248242196:  #stromox
		await ctx.send("No Penis Found")
	elif user.id == 121339500482920448:
		embed = discord.Embed(title='B40 PENIS MEASUREMENT',
		                      description="It's... It's unreal 😱",
		                      timestamp=ctx.message.created_at,
		                      color=discord.Color.red())
		embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")

		embed.add_field(name="DICK OF:", value=user.mention)
		embed.add_field(name="LENGTH:", value="∞")
		embed.add_field(name="UNIT:", value="error")
		embed.add_field(name="PENIS DISPLAY:",
		                value="unable to process the sheer amount of data retrieved")
		embed.set_footer(text=f"Used by {ctx.author}",
		                 icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	else:
		penis = "8" + "=" * random.randint(0, 18) + "D"

	if len(penis) > 15:
		penis_info = "DAMN UR PACKING"

	elif len(penis) > 9:
		penis_info = "average boi"

	elif len(penis) > 2:
		penis_info = "lol bozo + ratio + small pp"

	else:
		penis_info = "LOL U ONLY HAVE BALLS AND A TIP"

	embed = discord.Embed(title='B40 PENIS MEASUREMENT',
	                      description=penis_info,
	                      timestamp=ctx.message.created_at,
	                      color=discord.Color.red())
	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")

	embed.add_field(name="DICK OF:", value=user.mention)
	embed.add_field(name="LENGTH:", value=len(penis))
	embed.add_field(name="UNIT:", value="cm")
	embed.add_field(name="PENIS DISPLAY:", value=penis)
	embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

	await ctx.send(embed=embed)


# dont delete this, need this for future reference
#@bot.command()
#async def test(ctx):
#    SENDER_OF_THE_MESSAGE = message.author.mention
#    await ctx.send(SENDER_OF_THE_MESSAGE)

#dont delete this either
#@bot.command()
#async def test2(ctx, *,  user : discord.Member=None):
#    usermention = user.mention

#    await ctx.send(usermention)


@bot.command(aliases=['avt', 'avatar'])
async def av(ctx, member: discord.Member = None):
	"""
	Returns Avatar of user: avatar *@user
	"""

	if member == None:
		member = ctx.author

	embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
	embed.set_author(icon_url=member.avatar_url,
	                 name=f"{member}   •   {member.id}"),
	embed.set_image(url=member.avatar_url)

	await ctx.send(embed=embed)


# Events
@bot.event
async def on_ready():
	print('My Ready is Body')


@bot.listen()
async def on_message(message):
	if "ninja" in message.content.lower():
		with open('pictures/ninja.jpg', 'rb') as f:
			picture = discord.File(f)

			await message.channel.send(file=picture)


@bot.listen()
async def on_message(message):
	if "who asked?" in message.content.lower():
		with open('pictures/SOVAWHOASKED.png', 'rb') as f:
			picture = discord.File(f)

			await message.channel.send(file=picture)


@bot.listen()
async def on_message(message):
	if "blacky?" in message.content.lower():
		with open('pictures/blacky.png', 'rb') as f:
			picture = discord.File(f)

			await message.channel.send('The Prince of Dubai', file=picture)


"""
@bot.listen()
async def on_message(message):
    if "nigga" in message.content.lower():
        with open('pictures/nword.png','rb') as f:
          picture = discord.File(f)

          await message.channel.send(file=picture)"""


@bot.listen()
async def on_message(message):
	if "fadil?" in message.content.lower():
		await message.channel.send('The worst valorant player in B40')


@bot.listen()
async def on_message(message):
	if "threat?" in message.content.lower():
		await message.channel.send('The Sexiest Nugget')


@bot.listen()
async def on_message(message):
	if "3bood?" in message.content.lower():
		await message.channel.send('glory hole beta tester')
	if "tj?" in message.content.lower():
		await message.channel.send('tj u gay')


@bot.listen()
async def on_message(message):
	bad_words = [
	 "nigga", "nigger", "niggger", "ni55er", "ni33er", "nibber", "nibba"
	]
	for word in bad_words:
		if word in message.content.lower():
			time.sleep(0.3)
			await message.delete()


def in_voice_channel():

	def predicate(ctx):
		return ctx.author.voice and ctx.author.voice.channel

	return check(predicate)


@in_voice_channel()
@bot.command()
async def mm(ctx, *, channel: discord.VoiceChannel):
	"""
	Moves every person in the current voice channel to a new channel: mm [channel name]
	"""

	if ctx.author.guild_permissions.move_members:
		for members in ctx.author.voice.channel.members:
			await members.move_to(channel)
	else:
		await ctx.send("You don't have the permission to use this command!")


@bot.command(aliases=['mma'])
async def mmall(ctx, *, channel: discord.VoiceChannel):
	"""
	Moves every member of the server who is in a voice channel to a certain voice channel.: mmall [channel name] 
	"""

	if ctx.author.guild_permissions.move_members:
		for channelz in ctx.guild.voice_channels:
			for members in channelz.members:
				await members.move_to(channel)
	else:
		await ctx.send("You don't have the permission to use this command!")


antibood = False


@bot.command()
async def antibood(ctx, member: discord.Member = None):
	"""
	FUCK BOOD
	"""
	global antibood

	if ctx.author.id != 114152481398718468:
		antibood = not antibood
		await ctx.send("ANTIBOOD!!")


@bot.listen()
async def on_message(message):
	global antibood
	if antibood:
		if message.author.id == 114152481398718468:
			await message.delete()
			ctx = await bot.get_context(message)
			bood_message_length = len(message.clean_content)
			msg = await ctx.send(
			 f"{bood_message_length} char(s) of shit have been removed", delete_after=5)

@bot.listen()
async def on_message(message):
	if not message.author.bot:
		# CONNECT TO DATA BASES SC = SERVERCHAT, UC = USERCHAT
		sc_DB = sqlite3.connect('serverchat.db')
		sc_cursor = sc_DB.cursor()
		uc_DB = sqlite3.connect('userchat.db')
		uc_cursor = uc_DB.cursor()
		# CREATE DATA THAT WILL BE STORED IN DATABASES
		user = str(message.author.id)
		dates = '[' + str(datetime.date.today()) + ']'
		msgs = 1
		chars = len(message.clean_content)
		links = 1 if "http" in message.content.lower() else 0
		files = 1 if len(message.attachments) > 0 else 0
		
		print(msgs, chars, links, files, dates, message.author)

		# SERVERCHAT DB QUERIES
		sc_create_table(sc_cursor)
		sc_data_entry(sc_cursor, sc_DB, dates, msgs, chars, links, files)
		sc_update(sc_cursor, sc_DB, msgs, chars, links, files, dates)
		# USERCHAT DB QUERIES
		uc_create_table(uc_cursor, dates)
		uc_data_entry(uc_cursor, uc_DB, dates, user)
		uc_update(uc_cursor, uc_DB, user, msgs, chars, dates)




my_secret = os.environ['TOKEN']
keep_alive()
bot.run(my_secret)
