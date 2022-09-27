import os
import time

import discord
import discord.ext
from LCU import CreateParty, InfoMatchMaking, QuitParty, SelectRoles, StartMatchMaking
from Definitions import Roles, Modes

intents = discord.Intents.all()
from time import sleep
import interactions
from Definitions import Roles, Modes
from LCU import CreateParty, InfoMatchMaking, QuitParty, SelectRoles, StopMatchMaking, StartMatchMaking
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")
bot = interactions.Client(token=token)

@bot.command(
    name="quit-party", 
    description="Quits current party"
)
async def hep(ctx):
    l = await ctx.send(content="quitting party...")
    try:
        response = QuitParty()
    except:
        await l.edit(content="League Is closed")
    if response.ok :
        await l.edit(content="Party Exited successfully")
    else:
        await l.edit(content="An error occurred")



@bot.command(name="start-matchmaking", description="Starts Matchmaking")
async def  delp(ctx: interactions.CommandContext):
        response = "siummico"
        try:
            StartMatchMaking()
        except:
            await ctx.send(content="An error occurred")    
        image = "https://media.discordapp.net/attachments/942431947068698644/1021858512411836496/unknown.png"
        await ctx.send(content="Start match")
        embed=interactions.Embed(title="Searching a match...", description=f"Time in queue = <t:{round(time.time())}:R>", color=0xff0000)
        embed.set_thumbnail(url=image)
        embed.add_field(name="First Preference", value="MIDDLE", inline=True)
        embed.add_field(name="Second Preference", value="TOP", inline=True)
        embed.set_footer(text="let's do the last one  -league addict")
        await ctx.send(embeds=embed)
        try:
            response = InfoMatchMaking()    
            print(response)
        except:
            pass
        while response != "siummico":
            time.sleep(0.33)
            if response[0]["searchState"] != "Searching":
                await ctx.send(content="Match found")    
                break
            else:
                print(response[0]["searchState"])    
            response = InfoMatchMaking()    
        # print("1")


@bot.command(
    name="select-roles", 
    description="Selects the roles for draft pick", 
    options= [
        interactions.Option(
            name="firstpreference",
            description="Select first preference",
            type=interactions.OptionType.STRING,
            required=True,
            choices=[
                interactions.Choice(name="Top", value=Roles.TOP), interactions.Choice(name="Jungle", value=Roles.JUNGLE), interactions.Choice(name="Middle", value=Roles.MIDDLE), interactions.Choice(name="Ad carry", value=Roles.ADC), interactions.Choice(name="Support", value=Roles.SUPPORT), 
            ], 
        ),
                interactions.Option(
            name="secondpreference",
            description="Select second preference",
            type=interactions.OptionType.STRING,
            required=True,
            choices=[
                interactions.Choice(name="Top", value=Roles.TOP), interactions.Choice(name="Jungle", value=Roles.JUNGLE), interactions.Choice(name="Middle", value=Roles.MIDDLE), interactions.Choice(name="Ad carry", value=Roles.ADC), interactions.Choice(name="Support", value=Roles.SUPPORT), 
            ], 
        ),
    ],
)
async def cmd(ctx: interactions.CommandContext, secondpreference: str, firstpreference: str):
    l = await ctx.send(f"```First Role: {firstpreference}\nSecond Role: {secondpreference}```")
    try:
        SelectRoles(firstpreference, secondpreference)   
    except:
        await l.edit(content="League Is closed")


@bot.command(
    name="create-party", 
    description="Creates a party", 
    options= [
        interactions.Option(
            name="mode",
            description="Select first preference",
            type=interactions.OptionType.INTEGER,
            required=True,
            choices=[
                interactions.Choice(name="Draft", value=Modes.DraftPick),
                interactions.Choice(name="SoloQ", value=Modes.SoloDuo), 
                interactions.Choice(name="Blind", value=Modes.BlindPick),
                interactions.Choice(name="ARAM", value=Modes.ARAM),
            ], 
        ),
    ],
)
async def cmd(ctx: interactions.CommandContext, mode: str):
    names = {Modes.DraftPick : "Draft", Modes.SoloDuo: "SoloQ", Modes.BlindPick: "Blind pick", Modes.ARAM : "ARAM"}
    l = await ctx.send(f"```Selected mode: {names[mode]}```")
    try:
        CreateParty(mode)
    except:
        await l.edit(content="League Is closed")





@bot.event
async def on_ready():
        print("Bot online") #will print "bot online" in the console when the bot is online
        await bot.change_presence(
        interactions.ClientPresence(
            status=interactions.StatusType.DND,
            activities=[
                interactions.PresenceActivity(name="Waiting for League", type=interactions.PresenceActivityType.GAME)
                ]
            )
        )



bot.start()
	



