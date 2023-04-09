import discord
import openai
import json
import os
from discord.ext import commands
import config


INTRO_CHANNEL_ID = config.INTRO_CHANNEL_ID
MESSAGE_LOG_FILE = config.MESSAGE_LOG_FILE
INTRO_CHANNEL_LOG_FILE = config.INTRO_CHANNEL_LOG_FILE
USER_INFO_FILE = config.USER_INFO_FILE
init_messages = config.init_messages

INTRODUCTION_CHANNEL_ID = config.INTRODUCTION_CHANNEL_ID
ROLE_NAME = config.ROLE_NAME

openai.api_key = config.OPENAI_API_KEY
# intents_client = openai.IntentsClient()

intents = discord.Intents.all()
# intents.message_content = True
# intents.members = True  # enable member intents
# intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(INTRODUCTION_CHANNEL_ID)
    await channel.send(f"Welcome {member.mention}! Please introduce yourself to the AI.")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(INTRODUCTION_CHANNEL_ID)
    await channel.send(f"{member.mention} has left the server.")
    


@bot.event
async def on_message(message):
    if message.channel.id == INTRO_CHANNEL_ID:
        message_data = {
            "role": message.author.name,
            "content": message.content
        }

        # If the message log file doesn't exist yet, create a new list with the first message
        if not os.path.exists(MESSAGE_LOG_FILE):
            with open(MESSAGE_LOG_FILE, 'w') as f:
                json.dump([message_data], f, indent=2)
                print(f"Created new message log file: {MESSAGE_LOG_FILE}")

        # If the message log file already exists, load the existing messages and add the new message to the list
        else:
            with open(MESSAGE_LOG_FILE, 'r') as f:
                logs = json.load(f)

            logs.append(message_data)
            print(f"Added new message to log file: {MESSAGE_LOG_FILE}")

            with open(MESSAGE_LOG_FILE, 'w') as f:
                json.dump(logs, f, indent=2)
        
        # let AI read the message and respond
        
        with open(MESSAGE_LOG_FILE, 'r') as f:
            intro_messages = json.load(f)
            
        
        latest_message = str(intro_messages[-1])
        
        if not os.path.exists(INTRO_CHANNEL_LOG_FILE):
            with open(INTRO_CHANNEL_LOG_FILE, 'w') as f:
                json.dump(init_messages, f, indent=2)
                print(f"Created new message log file: {INTRO_CHANNEL_LOG_FILE}")
                
        else:
            with open(INTRO_CHANNEL_LOG_FILE, 'r') as f:
                
        
        print(all_messages[-1]['role'])
        if all_messages[-1]['role'] == 'user':
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages = all_messages
                )
            
            generated_response = response.choices[0].message.content
            all_messages.append({"role": "assistant", "content" : generated_response})
            await message.channel.send(generated_response)
        
        

bot.run(config.DISCORD_TOKEN)
