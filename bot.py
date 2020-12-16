from youtubesearchpython import SearchVideos
import discord
from discord.ext import commands
from discord.ext.commands import Bot, guild_only
from discord import User
import discord.utils
import wolframalpha 
import requests
import praw
import random
import asyncio
import datetime
import os
import json
import wikipedia
import aiohttp
import time
import youtube_dl

search = ("AIzaSyCPgBJXR3moe7iHV6CJLLFZdrPmD8I8AdM")	
app_id = '4RPXT4-4VYAXX3Q6G'
wolf = wolframalpha.Client(app_id)  
client = commands.Bot(command_prefix=".")
client.remove_command("help")

f = open("rules.txt","r")
rules = f.readlines()


reddit = praw.Reddit(client_id = "2UWi15bh86-cnw",
	                 client_secret = "MA4B2xmKqEYdt8uGlA5BzK0lHp2ttQ",
	                 username = "adal01672",
	                 password = "adal016724",
	                 user_agent = "adal016723")


filtered_words = ["fuck","FUCK","Fuck","shit","SHIT","Shit","stfu","STFU","Stfu","fuck you","FUCK YOU","swear","SWEAR","Swear","porn","PORN","Porn","hentai","HENTAI","Hentai","nude","NUDE","Nude","sex","SEX","Sex","pussy","PUSSY","Pussy","dick","DICK","Dick","ASS","ass","Ass","boobs","BOOBS","Boobs","bitch","BITCH","Bitch","sh!t","p0rn","s3x"," fak","dic"]
@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content.lower():
            await msg.delete()
            await msg.channel.send("Don't use such language :speak_no_evil: \nAbusing or bullying is also included in so")
    await client.process_commands(msg)



@client.command(aliases=['memes'])
async def meme(ctx):
    embed = discord.Embed(title="Meme", description=None, color= discord.Colour.blue())

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 10)]['data']['url'])
            await ctx.send(embed=embed, content=None)

@client.command()
async def calc(ctx,*,ques):
    res = wolf.query(ques) 
    answer = next(res.results).text 
    em = discord.Embed(title = f"question ="+ ques +"❓",
    	              description = f"answer ="+ answer+ "❗",
                      color= discord.Colour.blue())
    await ctx.send(embed = em)
    	              

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"watching {len(client.guilds)} servers"))
    print("Bot is ready!")

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

@client.command()
async def sup(ctx):
    await ctx.send(":robot:i am doing some work in your server,thanks for asking btw")

@client.command()
async def rule(ctx,*,number):
    embed=discord.Embed(title= "rules", description=(rules[int(number)-1]), color= discord.Colour.blue())
    await ctx.send(embed=embed)

@client.command()
async def cmd(ctx):
    embed = discord.Embed(title = "Hype bot commands\n prefix: **.** " , description = "**mod cmds**\n 1.kick: kicks an member from the server\n 2.ban:  bans an member from the server\n 3.unban: unbans an member\n 4.clear:clears msg from server(.clear2 or 3 or 4 or more like this\n 5.mute: mutes an member from the entire server.\n 6.unmute:unmutes an member from the entire server.\n 7. whois: utilization .whois <@name>\n **hype bot commands**\n 1. hello: replies with hi\n 2. sup  : replies with :robot:i am doing some work in your server,thanks for asking btw\n 3. rule(1-10) : command like this  .rule <number>\n 4. cmd       : shows this message\n 5. afk: asigns a afk nickname for you utilization .afk <no.mins><reason>\n **fun cmds**\n 1.meme:finds memes from reddit for you\n **search cmds**\n 1.yo or youtube: for searching on youtube and finding result.\n 2.calc: is for basically searching in wolframalpha and finding result\n 3.invite: sends an invite link for the bot to join ur server\n 4.wiki: it sends u whatever u search from wikipedia.org it works like .wiki <search>", color = discord.Colour.blue())
    await ctx.send(embed=embed) 

        
    
@client.command()
async def wiki( ctx, word:str):
   definition = wikipedia.summary(word, sentences=1000, chars=10000)
   embed= discord.Embed(title = "wikipedia", description=definition, color= discord.Colour.blue() )
   await ctx.send(embed=embed)
 


@client.command(aliaces=['c'])
@discord.ext.commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit=amount)

@client.command(aliases=['k'])
@discord.ext.commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
    await member.send("you have been kicked from the server,because:"+reason)
    await member.kick(reason=reason)
    await ctx.send(member.name + "have been kicked successfully,because:" + reason)
    

@client.command(aliases = ['b'])
@commands.has_permissions(administrator = True)
async def ban(ctx ,member : discord.Member, *, reason = 'No reason Provided'):
    await ctx.send(member.name + ' have been Banned from the server \nReason : '+reason)
    try:
        await member.send('You have been Banned from the server \nReason : '+reason)
    except Exception as e:
        pass
    await member.ban(reason=reason)
@client.command(aliases = ['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx ,*,member):
    banned = await ctx.guild.bans()
    member_nam ,member_dis = member.split('#')

    for banned_entry in banned:
        user = banned_entry.user

        if(user.name ,user.discriminator) == (member_nam,member_dis):
            await ctx.guild.unban(user)
            await ctx.send(member_nam+" Has been unbanned !!!")
            return

        await ctx.send(member + ' was not found')


@client.command(aliases =['yo'])
async def youtube(ctx,*,msg):
    try:
        a = discord.Embed(title ="**Top Results for ** your search :", color = discord.Color.green()    )  
        await ctx.send(embed = a)          
        results = SearchVideos(msg,mode="dict",max_results =1)
        print(results.result())
        d = discord.Embed(title ='**'+results.result()['search_result'][0]['title']+'**'+'\n'+"Channel : "+results.result()['search_result'][0]['channel']+'\n'+'Duration : '+str(results.result()['search_result'][0]['duration'])+'\n'+'Views : '+str(results.result()['search_result'][0]['views'])+'\n'+"Publish Time : " +str(results.result()['search_result'][0]['publishTime'])+'\n',color = discord.Color.blue())
        await ctx.send(embed = d)
        await ctx.send('Link : '+results.result()['search_result'][0]['link']) 
    except Exception as e:
        print(e)
        c = discord.Embed(title ="No results found :sob:",color = discord.Color.red()    )
        await ctx.send(embed = c)

@client.command(aliases =['m'])
@discord.ext.commands.has_permissions(kick_members=True)
async def mute(ctx,member:discord.Member):
	muted_role = ctx.guild.get_role(721301805451182081)
	
	await member.add_roles(muted_role)

	await ctx.send(member.mention + "has been muted")

@client.command(aliases =['um'])
@discord.ext.commands.has_permissions(kick_members=True)
async def unmute(ctx,member:discord.Member):
	muted_role = ctx.guild.get_role(721301805451182081)
	
	await member.remove_roles(muted_role)

	await ctx.send(member.mention + "has been unmuted")
@client.command()
async def invite(ctx):
    em = discord.Embed(title ="invite me:grinning:",
    	              url = 'https://discord.com/api/oauth2/authorize?client_id=770689593066258483&permissions=8&scope=bot')
    await ctx.send(embed = em)

@client.command(aliases= ["afkset", "setafk"])
async def afk(ctx, mins, *, reason = "No reason Provided"):
    current_nick = ctx.author.nick
    await ctx.message.delete()
    afk_role = ctx.guild.get_role(787217714627608596)
    try:
        mins = float(mins)
    except:
        ad = discord.Embed(title = "Time should be a Integer or Float \nType  `.help` or `.more_help` for more info",color = discord.Color.red())
        await ctx.send(embed = ad)
    if isinstance(mins,float)==True:
        afk1= discord.Embed(title= ":zzz: Member AFK!", description= f"{ctx.author.mention} Has Gone AFK!", color = ctx.author.color)
        afk1.set_thumbnail(url= ctx.author.avatar_url)
        afk1.add_field(name= "For Time Being:", value= f"{mins} Min/s")
        afk1.add_field(name= "AFK Note:", value= f"{reason}")
        afk1.set_footer(icon_url= ctx.guild.icon_url, text= f"Hype bot")
        await ctx.send(embed=afk1)
        try:
            await ctx.author.add_roles(afk_role)
        except:
            pass
        try:
            await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
        except :
            ab = discord.Embed(description = f"Can't change {ctx.author.mention} nickname  :sob:",color = discord.Color.red())
            await ctx.send(embed = ab)
    
    abc = mins * 60
    await asyncio.sleep(abc)
    afk2= discord.Embed(title= ":wave: Member No Longer AFK!", description= f"{ctx.author.mention} IS NO LONGER AFK!", color = ctx.author.color)
    afk2.set_thumbnail(url= ctx.author.avatar_url)
    afk2.set_footer(icon_url= ctx.guild.icon_url, text= f"Hype bot")
    await ctx.send(embed=afk2)
    try:
        await ctx.author.remove_roles(afk_role)
    except:
        pass
    try:
        await ctx.author.edit(nick=current_nick)
    except:
        pass
colour_choices= [1752220,3066993,3447003,10181046,15844367,15105570,15158332,16580705] 
@client.command(aliases=["whois"])
async def profile(ctx, *, member: discord.Member):   
    if member == None:
        member = ctx.author

    roles = member.roles
    embed = discord.Embed(
            title=f"{member.display_name}#{member.discriminator}", color = random.choice(colour_choices))
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="User ID:", value=member.id, inline=False)
    embed.add_field(
            name="Created at:",
            value=member.created_at.strftime(
                '%a, %#d %B %Y, %I:%M %p GMT'),
            inline=True)
    embed.add_field(
            name="Joined server at:",
            value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p GMT'),
            inline=True)
    embed.add_field(name="Status:", value=f"{member.status}", inline=False)     
    embed.add_field(
            name=f"Roles ( {len(member.roles)} )",
            value=" ".join([role.mention for role in roles]),
            inline=False)
    embed.add_field(name="Top role", value=member.top_role)        
    await ctx.send(embed=embed)




		








	
	

client.run('NzcwNjg5NTkzMDY2MjU4NDgz.X5hOnQ.D7UXLyMZIoGAJ7M4_o3YE2agrDU')

