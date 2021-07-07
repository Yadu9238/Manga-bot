import discord
import asyncio
import re
import requests
import json
from bs4 import BeautifulSoup
#from urlextract import URLExtract 

from datetime import datetime
import os
import urllib.request
#import pprint

TOKEN = 'YOUR BOT TOKEN'
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return

    if message.content.startswith('!manga'):
      name = message.content.split()
      name = " ".join(name[1:])
      url = 'https://kitsu.io/api/edge/manga?filter[text]=${'+name+'}'
      headers = {'content-type':'application/vnd.api+json','Accept':'application/vnd.api+json'}
      
      #embed.set_image(url = data['data'][0]['attributes']['posterImage']['large'])

      r = requests.get(url,headers = headers)
      data = r.json()
      embed = discord.Embed(title =data['data'][0]['attributes']['canonicalTitle'],description =data['data'][0]['attributes']['synopsis'][:750]+"...",color = discord.Color.blue()  )
      embed.set_thumbnail(url = data['data'][0]['attributes']['posterImage']['large'])
      #img = await message.channel.send(embed = embed)
      genre = []
      genre_data = requests.get(data['data'][0]['relationships']['categories']['links']['related'])
      genre_data = genre_data.json()
      for i in range(genre_data['meta']['count']):
      	genre.append(genre_data['data'][i]['attributes']['title'])

      final = ",".join(genre)
      embed.add_field(name = "Genre",value = final,inline = False)
      await message.channel.send(embed = embed)
      #await message.channel.send("Title:"+data['data'][0]['attributes']['canonicalTitle'])
      #await message.channel.send("Description:"+data['data'][0]['attributes']['synopsis'][:750]+"...")

      
      #print(genre)

#for local testing
@client.event           
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)