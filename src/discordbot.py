import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import api.players

load_dotenv()
BOT_CHANNEL_ID = 1007151995351740526 # your discord channel id here
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!i ')

@bot.command(name='add', help='Add player ID')
async def add(ctx, account_id):
    print("add...")
    player = api.players.getPlayer(account_id)
    personaname = player['profile']['personaname']
    response = f"{personaname} added."
    await ctx.send(response)

@bot.command(name='update', help='Add player ID')
async def update(ctx):
    print("updating...")
    api.players.updateThread(1)
    response = "Updated."
    await ctx.send(response)

@bot.command(name='medals', help='Show all players medals.')
async def medals(ctx):
    print("medals...")
    medals = api.players.medalScores()
    medals_str = ""
    for medal in medals:
        medals_str += f"{medal['personaname']}: {medal['medal']}\n"

    response = medals_str
    await ctx.send(response)

print("Done.")

@tasks.loop(minutes = 60) # repeat after every x time
async def myLoop():

    api.players.updateThread(1)
    all_account_id = api.players.players.keys()
    posted_matches_id = []

    for i, match_id in enumerate(api.players.unposted_matches.keys()):
        match = api.players.unposted_matches[match_id]
        names = ""
        heroes = ""
        kda = ""
        all_personaname_in_match = []
        last_player_i = 0
        for i, account_id in enumerate(match['players']):
            if i == 0:
                names += "**RADIANT**" + (" **won**" if match['radiant_win'] else "") + "\n"
                heroes += "**HERO**\n"
                kda += "**KDA**\n"
            if i == 5:
                names += "\n"
                heroes += "\n"
                kda += "\n"

                names += "**DIRE**" + (" **won**" if not match['radiant_win'] else "") + "\n"
                heroes += "**HERO**\n"
                kda += "**KDA**\n"

            player = match['players'][account_id]
            personaname = f"{api.players.players[account_id]['profile']['personaname']}" if account_id in all_account_id else "desconhecido"
            if personaname != "desconhecido":
                last_player_i = i
                all_personaname_in_match.append(personaname)
            names += personaname + '\n'
            heroes += api.players.heroes[str(player['hero_id'])] +'\n'
            kda += (f"{player['kills']}/{player['deaths']}/{player['assists']}") + '\n'
        posted_matches_id.append(match_id)
        
        personanames_str = ""
        for name in all_personaname_in_match:
            personanames_str += f"{name}, "

        embed=discord.Embed(
            url=f"https://stratz.com/matches/{match_id}",
            title=f"Match of {personanames_str}",
            color=(discord.Color.green() if last_player_i < 5 and match['radiant_win'] or last_player_i >= 5 and not match['radiant_win'] else discord.Color.red())
        )
        duration = match['duration'] // 60
        embed.add_field(name="-", value=names, inline=True)
        embed.add_field(name="-", value=heroes, inline=True)
        embed.add_field(name=f"{duration}min", value=kda, inline=True)
        
        channel = bot.get_channel(BOT_CHANNEL_ID)
        await channel.send(embed=embed)
        # await channel.send(reponse_str)
        
    for match_id in posted_matches_id:
        del api.players.unposted_matches[match_id]
    
    

@bot.event
async def on_ready():
    myLoop.start()
    print(f'Bot connected as {bot.user}')

bot.run(TOKEN)
