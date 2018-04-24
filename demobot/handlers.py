from random import randint
import os
import pickle
from demobot.utils import *
from datetime import date
from shutil import copyfile

print("Begin Handler Initialization")

message_handlers = {}
private_message_handlers = {}

print("\tBegin Loading Files")



print("\tLoaded files")

persistent_variables = {}

if not os.path.exists("data/data_backup/"):
    os.makedirs("data/data_backup/")

server_data = {}
if os.path.isfile("data/settings.txt"):
    with open("data/settings.txt", "rb") as f:
        server_data = pickle.load(f)
    copyfile("data/settings.txt", "data/data_backup/settings.txt")

def add_message_handler(handler, keyword):
    message_handlers[keyword] = handler
def add_private_message_handler(handler, keyword):
    private_message_handlers[keyword] = handler
def update_user_data(channelid, obj, val, addon=False):
    if channelid in server_data:
        if addon:
            if obj in server_data[channelid]:
                server_data[channelid][obj] += val
                return
        server_data[channelid][obj] = val
    else:
        server_data[channelid] = {obj:val}

print("Handler initialized")
print("Begin Command Initialization")
# Add modules here
from commands import *
import discord
print("Command Initialization Finished")

import asyncio
import re

whitespace = [' ', '\t', '\n']

@asyncio.coroutine
def on_message(Demobot, msg):
    if not msg.author.bot:
        try:
            if msg.channel.is_private:
                yield from Demobot.send_message(msg.channel, "Demobot doesn't work in private channels")
            for a in message_handlers:
                reg = re.compile(a, re.I).search(msg.content)
                if reg:
                    yield from message_handlers[a](Demobot, msg, reg)
        except IndexError:
            em = discord.Embed(title="Missing Inputs", description="Not enough inputs provided.", colour=0xd32323)
            yield from send_embed(Demobot, msg, em)
        except (TypeError, ValueError):
            em = discord.Embed(title="Invalid Inputs", description="Invalid inputs provided.", colour=0xd32323)
            yield from send_embed(Demobot, msg, em)
        except discord.Forbidden:
            em = discord.Embed(title="Missing Permissions", description="Demobot is missing permissions to perform this task.", colour=0xd32323)
            yield from send_embed(Demobot, msg, em)
        except Exception as e:
            em = discord.Embed(title="Unknown Error", description="An unknown error occurred. Trace:\n%s" % e, colour=0xd32323)
            yield from send_embed(Demobot, msg, em)
