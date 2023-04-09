import discord
import time
import json
import io
#from discord import app_commands
import interactions
#from discord.ext import commands
#from discord_slash import commands, SlashCommand, SlashContext
import asyncio
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pyvirtualdisplay import Display 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from discord import ButtonStyle, ActionRow, Button
#from discord import SlashCommand
import os
from discord.ext import commands
from discord import Color
import pyperclip

with open('C:/Users/modib/Documents/kali/py/SensConvertBOT/config.json') as f:
   data = json.load(f)

# region variables 
TOKEN = data["TOKEN"]
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(client)
PREFIX = "&"
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
options = Options()
driver = webdriver.Chrome(options=options)
UNSNITISEDCHARS = '\'!?^~`:;{[}]+='
#endregion

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Al adan"))

def SanitiseLink(args):
    n = ""
    for i in args:
        if i not in UNSNITISEDCHARS:
            n += i
    args.lower()
    return n

@client.event
async def on_message(message:discord.Message):
    if message.author.bot or not(str(message.content).startswith(PREFIX)):
        return
    args = message.content.split(" ")
    args[0] = args[0][1::]
    print(args)
    if args[0] == 'Convert' :
        d = SanitiseLink(args = args[1])
        S = SanitiseLink(args = args[2])
        driver.get('https://armorygaminggear.com/sensitivity-converter/' + d.lower() + '-convert-to-' + S.lower())
        sensVal = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="converter-page"]/div[3]/div[2]/input'))
        sensVal.click()
        sensVal.send_keys(args[3])
        sensFinal = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//*[@id="converter-page"]/div[6]/div/div[1]/div[2]'))
        mbd = discord.Embed(title='Sensitivity Converter :', color = Color.red())
        mbd.add_field(name = args[1].capitalize(), value = args[3])
        mbd.add_field(name = args[2].capitalize(), value = sensFinal.text)
        mbd.set_footer(text= 'Data taken from : https://armorygaminggear.com/')
        await message.channel.send(embed = mbd)

client.run(TOKEN)