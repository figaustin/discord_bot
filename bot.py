from urllib import response
import discord
import random
import requests
import json
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

client = discord.Client()
load_dotenv()
tenor_api_key = os.getenv('tenor_key')
open_weather_key = os.getenv('open_weather_key')


eight_ball_answers = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes definitely.',  'You may rely on it.', 'Most likely.', 'Ask again later...', 'Better not tell you now...', "Don't count on it.", 'My reply is no.', 'My sources say no.', 'Outlook not so good.']

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('hello' or 'Hello'):
        await message.channel.send('Hello, ' + message.author.mention)
    
    elif message.content.startswith('$8ball'):
        await message.channel.send(message.author.mention + ' ' + random.choice(eight_ball_answers))

    elif message.content.startswith('$ping'):
        await message.channel.send('Pong!')

    elif message.content.startswith('$rolld20'):
        roll = random.randrange(1,21,1)
        if roll == 20:
            await message.channel.send(f'{message.author.mention}, Your roll is **{roll}**! Wow, Nice roll!')
        elif roll == 1:
            await message.channel.send(f'{message.author.mention}, Your roll is **{roll}**... Better luck next time!')
        else:
            await message.channel.send(f'{message.author.mention}, Your roll is **{roll}**!')

    elif message.content.startswith('$anime'):
        gif_url = get_gif('anime') 
        
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)

    elif message.content.startswith('$cat'):
        gif_url = get_gif('cat') 
        
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)
    
    elif message.content.startswith('$slap'):
        await message.channel.send(f'{message.author.mention}, **slapped** {message.content.lower()[6:]} **!**')

    elif message.content.startswith('$weather'):
        await message.channel.send(f'{message.author.mention}, The current weather in __{message.content.lower()[8:].upper().strip()}__ is **{get_weather(message.content.lower()[8:])[0]} °F** and **{get_weather(message.content.lower()[8:])[1].upper()}**.')


# Function to get a gif using Tenor API
def get_gif(searchTerm): 
    response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=50".format(searchTerm, tenor_api_key))
    data = response.json()
    
    #Return a random gif within the search range of the specified search term
    return data['results'][random.randrange(0,50,1)]['media'][0]['gif']['url']

# Retrieve weather data for specified CITY 
def get_weather(city):
    # Get latitude and longitude from specified CITY and store in variables to be able to use in API response
    response = requests.get("http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=1&appid=%s" % (city, open_weather_key))
    data = json.loads(response.text)
    lat = data[0]['lat']
    lon = data[0]['lon']

    # Retrieve weather data from previous variables
    weather_response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&units=imperial&exclude=minutely,hourly,daily,alerts&appid=%s" % (lat, lon, open_weather_key))
    weather_data = json.loads(weather_response.text)
    current_temp = weather_data["current"]["temp"]
    current_weather = weather_data["current"]["weather"][0]["description"]

    return current_temp, current_weather

# Run bot
client.run(os.getenv('bot_key'))
