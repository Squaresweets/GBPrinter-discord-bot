import discord
from PIL import Image
import ImageProcessing
image_types = ["png", "jpeg", "jpg"]

#https://discord.com/api/oauth2/authorize?client_id=926847617474908200&permissions=268471296&scope=bot
TOKEN = "OTI2ODQ3NjE3NDc0OTA4MjAw.YdBoHA.LMEIrEE18txBnx57LEPN59U9CLI"

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
client.run(TOKEN)