from PIL import Image
from datetime import datetime
import discord
import asyncio
import requests
import images2gif as i2g
import os, shutil
import imageio
import sys

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Halo for kids'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!gambit'):
        url = message.attachments[0]['url']
        if url.endswith('gif'):
            folder = 'output'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        if file_path != ('output\.gitignore'):
                            os.unlink(file_path)
                            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
            folder2 = 'final'
            for the_file in os.listdir(folder2):
                file_path = os.path.join(folder2, the_file)
                try:
                    if os.path.isfile(file_path):
                        if file_path != ('final\.gitignore'):
                            os.unlink(file_path)
                            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)

            r = requests.get(url, allow_redirects=True)
            open('source.gif', 'wb').write(r.content)
            im = Image.open('source.gif')
            angle = -10.15
            size = 180, 180
            try:
                while True:
                    dst_im = Image.new('RGBA', (537, 559), (255, 0, 0, 0))
                    new_frame = im.convert('RGBA')
                    rot = new_frame.rotate(angle, expand=1).resize(size)
                    dst_im.paste(rot, (220, 170), rot)
                    dst_im.save('output/foo%02d.png' % im.tell(), 'PNG')
                    im.seek(im.tell()+1)
            except EOFError:
                pass
            gambit = Image.open('gambit.png')
            cont = 0
            png_dir = 'output'
            images = []
            for file in os.listdir(png_dir):
                if file != '.gitignore':
                    imm = Image.open('output/'+file)
                    Image.alpha_composite(imm, gambit).save('final/final%02d.png' % cont, 'PNG')
                    images.append(imageio.imread('final/final%02d.png' % cont))
                    cont += 1
            imageio.mimsave('movie.gif', images, 'GIF-FI')

            await client.send_file(message.channel, 'gambit1.png')
            await client.send_file(message.channel, 'gambit2.png')
            await client.send_file(message.channel, 'movie.gif')
            print('Succesfull gambit')
        else:
            r = requests.get(url, allow_redirects=True)
            open('source.png', 'wb').write(r.content)

            src_im = Image.open("source.png")
            angle = -10.15
            size = 180, 180

            dst_im = Image.new('RGBA', (537, 559), (255, 0, 0, 0))
            im = src_im.convert('RGBA')
            rot = im.rotate(angle, expand=1).resize(size)
            dst_im.paste(rot, (220, 170), rot)

            gambit = Image.open('gambit.png')

            Image.alpha_composite(dst_im, gambit).save("final.png")
            await client.send_file(message.channel, 'gambit1.png')
            await client.send_file(message.channel, 'gambit2.png')
            await client.send_file(message.channel, 'final.png')
            print('Succesfull gambit')

client.run('')