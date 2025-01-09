from dotenv import load_dotenv 
import os
import discord
import database_control
from creatures import Dinosaur
import random

dinoNames = ["Velociraptor", "T-rex", "Triceratops", "Allosaurus", "Stegosaurus", "Parasaurolophus", "Dilophosaurus"]
waitingToCatch = {}

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    database_control.create_table()
    print("Database initialized")

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith("dq!"):
        messageText = message.content.removeprefix("dq!")

        match messageText:
            case "join":
                userID = message.author.id
                users = database_control.get_users()
                if not str(userID) in users:
                    database_control.add_user(userID)
                    await message.channel.send(f'Welcome to Dino Quest, {message.author.mention}!')
                else:
                    await message.channel.send(f'You have already started this adventure, {message.author.mention}')

            case "dinos":
                await message.channel.send(f'{message.author.mention}\'s dinos: \n ' + database_control.get_inventory_string(message.author.id))
            
            case "bait":
                species = dinoNames[random.randrange(0, len(dinoNames))]
                level = random.randrange(2,7)
                dinoSpawn = Dinosaur(species, level)

                waitingToCatch[message.author.id] = dinoSpawn
                await message.channel.send(f'{message.author.mention} A wild level {dinoSpawn.level} {dinoSpawn.species} has appeared')
            
            case "catch":
                caughtDino = waitingToCatch[message.author.id]
                database_control.add_dino(message.author.id, caughtDino)
                await message.channel.send(f'{message.author.mention} just caught a level {caughtDino.level} {caughtDino.species}!')
                del waitingToCatch[message.author.id]

client.run(token)