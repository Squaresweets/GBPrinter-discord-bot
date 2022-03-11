import discord
from PIL import Image
import ImageProcessing
import serialCommunication
import os
from dotenv import load_dotenv
image_types = ["png", "jpeg", "jpg"]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            await attachment.save("image.png")
            ImageProcessing.process_image('image.png')
            await message.channel.send(file=discord.File(r"dithered.png"))
            serialCommunication.printImage()
client.run(TOKEN)