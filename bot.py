import discord
from discord.ext import tasks
import requests
import io
import os
bot = discord.Client(intents=discord.Intents.all())
bot.dc = {}
bot.key = os.getenv("API_KEY")
bot.gname = os.getenv("GUILD_NAME")
bot.log_channel = int(os.getenv("LOG_CHANNEL"))
bot.role = int(os.getenv("GUILD_ROLE"))
@tasks.loop(hours=12)
async def loop():
    role = bot.guilds[0].get_role(bot.role)
    print("https://api.hypixel.net/guild?name={bot.gname.replace(' ','%20'}&key=0dcc1cec-f88c-44f2-877b-b173cb78bac0")
    a = requests.get("https://api.hypixel.net/guild?name={bot.gname.replace(' ','%20'}&key=0dcc1cec-f88c-44f2-877b-b173cb78bac0").json()
    file = []
    for i in a['guild']['members']:
        b = i['uuid']
        c = requests.get(f"https://api.hypixel.net/player?uuid={b}&key={bot.key}").json()["player"]
        try:
            social_media = c['socialMedia']['links']['DISCORD']
        
        except:
            try:
                print(c["displayname"]+": "+"Unlinked Discord")
                file+=[c["displayname"]+": "+"Unlinked Discord"]
            except:
                print(b+": API off?")
                file+=[b+": API off?"]
            continue
        if not discord.utils.get(bot.guilds[0].members,name=social_media.split('#')[0],discriminator=social_media.split('#')[1]):
            try:
                print(c["displayname"]+": "+"Not in discord server! Linked Acc is "+social_media)
                file+=[c["displayname"]+": "+"Not in discord server! Linked Acc is "+social_media]
            except:
                print(b+": Can't fetch display name? That's odd")
                file+=[b+": Can't fetch display name? That's odd"]
                
            continue
        await discord.utils.get(bot.guilds[0].members,name=social_media.split('#')[0],discriminator=social_media.split('#')[1]).add_roles(role)
        bot.dc[c["displayname"]]=social_media
    file+=["\n\n=== DATA FOUND ==="]
    for i in bot.dc.keys():
        file+=[i + ": " + bot.dc[i]]
    
    file = discord.File(io.BytesIO(bytes("\n".join(file),encoding="utf-8")),filename="output.log")
    await bot.get_channel(bot.log_channel).send(file=file)
@bot.event
async def on_ready():
    try:
        loop.start()
    except Exception:
        pass
    
bot.run(os.getenv("TOKEN"))
    
