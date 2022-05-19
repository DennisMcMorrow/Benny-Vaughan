import os
import discord
from discord.ext import commands
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

my_secret = os.environ['secret']

url1 = 'https://api.jokes.one/jod?category=knock-knock'
url2 = "https://zenquotes.io/api/random"

sad_words = ["depressed", "unhappy", "sad", "angry", "miserable"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "Nah you're good."]

if "responding" not in db.keys():
    db["responding"] = True

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"] #list of encouragements
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
    
def delete_encouragement(index):
  encouragements = db["encouragements"] #list of encouragements
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def get_joke():
  response = requests.get(url1)
  joke = response.json()['contents']['jokes'][0]['joke']['text']
  return joke


def get_quote():
  response = requests.get(url2)
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


@client.event
async def on_ready():
  print('We have logged in as {0.user}.'
        .format(client))


@client.event
async def on_message(message):
  msg = message.content
  
  if message.author == client.user:
    return

  if msg.startswith('$joke'):
    joke = get_joke()
    await message.channel.send(joke)

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options += db["encouragements"]
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith('$water'):
    await message.channel.send('Here is some water for you @DuckieKing#8210 :cup_with_straw:')


  if msg.startswith("$ls"):
    encouragements = []
    if "encouragements" in db.keys(): 
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
    
  
  if msg.startswith("$new"):
    encouragements = []
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    encouragements = db["encouragements"]
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements) 

keep_alive()
client.run(my_secret)