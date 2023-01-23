from doctest import OutputChecker
import time, discord, socket, platform, subprocess, json, os, shutil, csv, random, typing, asyncio, mojang
from mcrcon import MCRcon
from discord import *
from discord.ext import commands
from discord.utils import get
from mcstatus import JavaServer
from discord.ui import Button, View
import matplotlib.pyplot as plt

workdir = os.getcwd()
if '/' in workdir:
    workdir = workdir + r"/"
else:
    workdir = workdir + r"\\"

bottoken = "" #required
botid =  #required for chatbridge
chatbridgechanid =  #required for mc to discord chatbridge
smppath = r"" #required for smp out chatbridge, stat command
cmppath = r"" #required for cmp out chatbridge
smprconpass = "" #required for smp in chatbridge, execute smp command, ping command
cmprconpass = "" #required for cmp in chatbridge, execute cmp command, ping command
smpip = "" #required for smp in chatbridge, execute smp command, ping command
cmpip = "" #required for cmp in chatbridge, execute cmp command, ping command
smprconport =  #required for smp in chatbridge, execute cmp command, ping command
cmprconport =  #required for cmp in chatbridge, execute cmp command, ping command

plt.style.use('dark_background')
plt.title('Bolt Network Plan')
plt.xlabel('x')
plt.ylabel('z')

def random_color():
    levels = range(32,256,32)
    r,g,b =  tuple(random.choice(levels) for _ in range(3))
    return ('#{:X}{:X}{:X}').format(r, g, b)
random_color()

def Sorted_Grouper(stations):  
  substaitions = []
  lastsub = 0
  temp = []
  for i in stations:
    if i[2] != lastsub:
      lastsub = i[2]
      substaitions.append(temp)
      temp = []
    if i[2] == lastsub:
      temp.append(i)
  substaitions.append(temp)
  return substaitions

def Grouped_Ploter(grouped_stations):
  for i in grouped_stations:
    new_color = random_color()
    for j in i:
      plt.plot(j[0],j[1],'o',color = new_color)
  plt.savefig('plan.png', transparent=True)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 1003365626825408604))
            self.synced = True
        activity = discord.Game(name="managing apes", type=3)
        await client.change_presence(status=discord.Status.online, activity=activity)
        print(f"Logged in as {self.user}")
        global chan
        chan = client.get_channel(chatbridgechanid) 

client = aclient()
tree = app_commands.CommandTree(client)

#Guild = client.get_guild(id: 1003365626825408604, /) -> (Guild | None):
#trial_member = utils.get(Guild.roles, name="Trial-Member")

async def cbsend(msg):
   await chan.send(msg) 

@tree.command(name = "test", description = "test", guild = discord.Object(id = 1003365626825408604))
@app_commands.describe(names = "Names of random ppl.")
@app_commands.choices(names = [
    discord.app_commands.Choice(name="Catniped", value=1),
    discord.app_commands.Choice(name="Sorriahn", value=2),
    discord.app_commands.Choice(name="Gnome", value=3),
])
async def self(interaction: discord.Interaction, names: typing.Optional[discord.app_commands.Choice[int]] = None) -> None:
    trial_member = interaction.guild.get_role(1007725484219568168)
    if interaction.user.top_role >= trial_member:
        await interaction.response.send_message(f"{names.name}s testicles")

def ping2(host,port,timeout=2):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
       sock.connect((host,port))
    except:
       return False
    else:
       sock.close()
       return True

#planner

@tree.command(name = "addstation", description = "Adds a station to the bolt network planner.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, station: str, x: str, z: str, subnet: typing.Optional[str] = None) -> None:
    if subnet == None:
        subnet = -1
    stationi = [f"{station}", f"{x}", f"{z}", f"{subnet}"]
    with open('stations.csv', 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(stationi)
    embedVar = discord.Embed(title="Success!", description=f"**Successfully added station `{station}`!** ", color=0x34EB86)
    await interaction.response.send_message(embed=embedVar) # , view=view

@tree.command(name = "stationlist", description = "Shows a list of added stations.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    msg = ""
    with open('stations.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                msg = msg + f"{row[0]} ({row[1]}, {row[2]}; {row[3]})\n"
                line_count += 1
    embedVar = discord.Embed(title="Station list", description=f"`{msg}`", color=0x0095FF)
    await interaction.followup.send(embed=embedVar)
    csv_file.close()

@tree.command(name = "deletestation", description = "Deletes a station.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, station: str):
    await interaction.response.defer()
    with open('stations.csv', 'r') as inp, open('stationsout.csv', 'w') as out:
        writer = csv.writer(out, lineterminator="\n")
        for row in csv.reader(inp):
            if row[0] != station:
                writer.writerow(row)
    os.remove("stations.csv")
    os.rename(fr"{workdir}stationsout.csv", fr"{workdir}stations.csv")
    embedVar = discord.Embed(title="Success!", description=f"**Successfully deleted station `{station}`!**", color=0x34EB86)
    await interaction.followup.send(embed=embedVar)

@tree.command(name = "setsubnet", description = "Sets a stations subnet.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, station: str, subnet: str):
    await interaction.response.defer()
    with open('stations.csv', 'r') as inp, open('stationsout.csv', 'w') as out:
        writer = csv.writer(out, lineterminator="\n")
        for row in csv.reader(inp):
            if row[0] != station:
                writer.writerow(row)
            else:
                row[3] = subnet
                writer.writerow(row)
    os.remove("stations.csv")
    os.rename(fr"{workdir}stationsout.csv", fr"{workdir}stations.csv")
    embedVar = discord.Embed(title="Success!", description=f"**Successfully changed the subnet of `{station}` to `{subnet}`!** ", color=0x34EB86)
    await interaction.followup.send(embed=embedVar)

@tree.command(name = "resetsubnet", description = "Resets a stations subnet. ", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, station: str):
    await interaction.response.defer()
    with open('stations.csv', 'r') as inp, open('stationsout.csv', 'w') as out:
        writer = csv.writer(out, lineterminator="\n")
        for row in csv.reader(inp):
            if row[0] != station:
                writer.writerow(row)
            else:
                row[3] = -1
                writer.writerow(row)
    os.remove("stations.csv")
    os.rename(fr"{workdir}stationsout.csv", fr"{workdir}stations.csv")
    embedVar = discord.Embed(title="Success!", description=f"**Successfully reset the subnet of `{station}`!** ", color=0x34EB86)
    await interaction.followup.send(embed=embedVar)

@tree.command(name = "resetallsubnets", description = "Resets every stations subnet. ", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    with open('stations.csv', 'r') as inp, open('stationsout.csv', 'w') as out:
        writer = csv.writer(out, lineterminator="\n")
        for row in csv.reader(inp):
            row[3] = -1
            writer.writerow(row)
    os.remove("stations.csv")
    os.rename(fr"{workdir}stationsout.csv", fr"{workdir}stations.csv")
    embedVar = discord.Embed(title="Success!", description=f"**Successfully reset the subnets of all stations!** ", color=0x34EB86)
    await interaction.followup.send(embed=embedVar)

@tree.command(name = "addsubnet", description = "*wip* Adds a subnet to the bolt network planner.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, name: str, colour: str):
    embedVar = discord.Embed(title="Success! (this does not actually do anything)", description=f"**Successfully added subnet `{name}`!** ", color=colour)
    await interaction.response.send_message(embed=embedVar)

@tree.command(name = "plan", description = "Generates a plan of the bolt network.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    sorted_stations = []
    with open('stations.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
                sorted_stations.append([row[1],row[2],row[3]])
    Grouped_Ploter(Sorted_Grouper(sorted_stations))
    await interaction.followup.send(file=discord.File(fr'{workdir}plan.png'))

#todolist

@tree.command(name = "addtask", description = "Adds a task to the todo list.", guild = discord.Object(id = 1003365626825408604))
@app_commands.describe(priority = "The priority of the task.")
@app_commands.choices(priority = [
    discord.app_commands.Choice(name="high", value=1),
    discord.app_commands.Choice(name="medium", value=2),
    discord.app_commands.Choice(name="low", value=3),
])
async def self(interaction: discord.Interaction, name: str, priority: discord.app_commands.Choice[int],  tag: typing.Optional[str] = None, description: typing.Optional[str] = None, attachment: typing.Optional[discord.Attachment] = None) -> None:
    todoi = [f"{name}", f"{tag}", f"{priority.name}", f"{description}"]
    if attachment is not None:
        await attachment.save(f"{name}_{attachment.filename}")
    with open('todo.csv', 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(todoi)
    embedVar = discord.Embed(title="Success!", description=f"**Successfully added task `{name}`!** ", color=0x34EB86)
    await interaction.response.send_message(embed=embedVar)

@tree.command(name = "edittask", description = "Edits a task on the todo list.", guild = discord.Object(id = 1003365626825408604))
@app_commands.describe(priority = "The priority of the task.")
@app_commands.choices(priority = [
    discord.app_commands.Choice(name="high", value=1),
    discord.app_commands.Choice(name="medium", value=2),
    discord.app_commands.Choice(name="low", value=3),
])
async def self(interaction: discord.Interaction, task: str, tag: typing.Optional[str] = None, priority: typing.Optional[discord.app_commands.Choice[int]] = None, desc: typing.Optional[str] = None, attachment: typing.Optional[discord.Attachment] = None) -> None:
    await interaction.response.defer()
    with open('todo.csv', 'r') as inp, open('todoout.csv', 'w') as out:
        writer = csv.writer(out, lineterminator="\n")
        for row in csv.reader(inp):
            if row[0] != task:
                writer.writerow(row)
            else:
                if tag != None:
                    row[1] = tag
                    writer.writerow(row)
                elif priority != None:
                    row[2] = priority.name
                    writer.writerow(row)
                elif desc != None:
                    row[3] = desc
                    writer.writerow(row)
                else:
                    writer.writerow(row)
    os.remove("todo.csv")
    os.rename(fr"{workdir}todoout.csv", fr"{workdir}todo.csv")
    if attachment is not None:
        await attachment.save(f"{task}_{attachment.filename}")
    embedVar = discord.Embed(title="Success!", description=f"**Successfully applied edits to task `{task}`!** ", color=0x34EB86)
    await interaction.followup.send(embed=embedVar)

@tree.command(name = "todolist", description = "Shows the todolist.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    hmsg = ""
    mmsg = ""
    lmsg = ""
    umsg = ""
    with open('todo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[2] == "high":
                    hmsg = hmsg + f"{row[0]} ({row[1]})\n"
                elif row[2] == "medium":
                    mmsg = mmsg + f"{row[0]} ({row[1]})\n"
                elif row[2] == "low":
                    lmsg = lmsg + f"{row[0]} ({row[1]})\n"
                else:
                    umsg = umsg + f"{row[0]} ({row[1]})\n"
                line_count += 1
    embedVar = discord.Embed(title="TODO list", description=f"`Tasks:`", color=0xDA42F5)
    if hmsg != "":
        embedVar.add_field(name="High Priority", value=f"`{hmsg}`", inline=False)
    if mmsg != "":
        embedVar.add_field(name="Medium Priority", value=f"`{mmsg}`", inline=False)
    if lmsg != "":
        embedVar.add_field(name="Low Priority", value=f"`{lmsg}`", inline=False)
    if umsg != "":
        embedVar.add_field(name="Unspecified Priority", value=f"`{umsg}`", inline=False)
    await interaction.followup.send(embed=embedVar)
    csv_file.close()

@tree.command(name = "deletetask", description = "Deletes a todo task (use /markdone to mark tasks as done).", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, task: str):
    await interaction.response.defer()
    with open('todo.csv', 'r') as inp, open('todoout.csv', 'w') as out:
        writer = csv.writer(out, lineterminator="\n")
        for row in csv.reader(inp):
            if row[0] != task:
                writer.writerow(row)
    os.remove("todo.csv")
    os.rename(fr"{workdir}todoout.csv", fr"{workdir}todo.csv")
    filelist = os.listdir(workdir)
    for x in filelist:
        if x.startswith(task):
            os.remove(x)
    embedVar = discord.Embed(title="Success!", description=f"**Successfully deleted task `{task}`!**", color=0x34EB86)
    await interaction.followup.send(embed=embedVar)

@tree.command(name = "markdone", description = "Marks a todo task as done.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, task: str):
    await interaction.response.defer()
    out2 = open('tododone.csv', 'a')
    writer2 = csv.writer(out2, lineterminator="\n")
    with open('todo.csv', 'r') as inp, open('todoout.csv', 'w') as out:
        writer = csv.writer(out, lineterminator="\n")
        for row in csv.reader(inp):
            if row[0] != task:
                writer.writerow(row)
            else:
                writer2.writerow(row)
    os.remove("todo.csv")
    os.rename(fr"{workdir}todoout.csv", fr"{workdir}todo.csv")
    out2.close()
    filelist = os.listdir(workdir)
    for x in filelist:
        if x.startswith(task):
            os.remove(x)
    embedVar = discord.Embed(title="Success!", description=f"**Successfully marked task `{task}` as done!**", color=0x34EB86)
    await interaction.followup.send(embed=embedVar)

@tree.command(name = "donelist", description = "Shows the list of done todo tasks.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    msg = ""
    with open('tododone.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                msg = msg + f"{row[0]} ({row[1]})\n"
                line_count += 1
    embedVar = discord.Embed(title="TODO marked as done list", description=f"`{msg}`", color=0xDA42F5)
    await interaction.followup.send(embed=embedVar)
    csv_file.close()

@tree.command(name = "taskinfo", description = "Shows the additional info about a todo task.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction, task: str):
    await interaction.response.defer()
    msg = ""
    with open('todo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[0] == task:
                    embedVar = discord.Embed(title=f"{row[0]}", description=f"**Priority:** `{row[2]}`\n**Tag:** `{row[1]}`", color=0xDA42F5)
                    embedVar.add_field(name="Description", value=f"{row[3]}", inline=False)
                line_count += 1
        filelist = os.listdir(workdir)
        filelist2 = []
        for x in filelist:
            if x.startswith(task):
                file2 = str(x)
                filelist2.append(discord.File(workdir + file2))
    if filelist2 is not None:
        await interaction.followup.send(embed=embedVar, files=filelist2)
    else:
        await interaction.followup.send(embed=embedVar)

#server

@tree.command(name = "ping", description = "Pings the servers to check their status.", guild = discord.Object(id = 1003365626825408604))
async def self(interaction: discord.Interaction):
        await interaction.response.defer()
        embedVar = discord.Embed(title="Ping information", description=f"", color=0xF56C42)
        try:
            smp2 = JavaServer.lookup("129.146.186.215:25565")
            smpstatus = smp2.status()
            smpquery = smp2.query()
            with MCRcon(smpip, smprconpass, port=smprconport) as mcr:
                resp1 = mcr.command("script run reduce(system_info('server_last_tick_times'), _a+_, 0)/100")
                a = resp1.split()
                if float(a[1]) <= 50.0:
                    tps1 = 20.0
                else:
                    tps1 = 1000.0 / float(a[1])
            embedVar.add_field(name="SMP", value=f"SMP is `online ({round(float(a[1]), 2)} mspt, {round(tps1, 2)} tps)`\nThere are currently `{smpstatus.players.online}` players online `({', '.join(smpquery.players.names)})`", inline=False)
        except ConnectionRefusedError:
            embedVar.add_field(name="SMP", value=f"SMP is `offline`", inline=False)
        try:
            cmp2 = JavaServer.lookup("129.146.186.215:25566")
            cmpstatus = cmp2.status()
            cmpquery = cmp2.query()
            with MCRcon(cmpip, cmprconpass, port=cmprconport) as mcr:
                resp2 = mcr.command("script run reduce(system_info('server_last_tick_times'), _a+_, 0)/100")
                b = resp2.split()
                if float(b[1]) <= 50.0:
                    tps2 = 20.0
                else:
                    tps2 = 1000.0 / float(b[1])
            embedVar.add_field(name="CMP", value=f"CMP is `online ({round(float(b[1]), 2)} mspt, {round(tps2, 2)} tps)`\nThere are currently `{cmpstatus.players.online}` players online `({', '.join(cmpquery.players.names)})`", inline=False)
        except ConnectionRefusedError: 
            embedVar.add_field(name="CMP", value=f"CMP is `offline`", inline=False)
        await interaction.followup.send(embed=embedVar)

@tree.command(name = "execute", description = "Executes a command on one of the servers.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(administrator = True)
@app_commands.describe(server = "The server to execute the command on.")
@app_commands.choices(server = [
    discord.app_commands.Choice(name="smp", value=1),
    discord.app_commands.Choice(name="cmp", value=2),
])
async def self(interaction: discord.Interaction, server: discord.app_commands.Choice[int], command: str):
    await interaction.response.defer()
    try:
        if server.name == "cmp":
            server2 = cmprconport
            rconpass = cmprconpass
        elif server.name == "smp":
            server2 = smprconport
            rconpass = smprconpass
        with MCRcon("129.146.186.215", f"{rconpass}", port=server2) as mcr:
            resp = mcr.command(f"{command}")
        embedVar1 = discord.Embed(title="Command executed", description=f"Successfully executed `{command}` on `{server.name}`\n`{resp}`", color=0xFF0068)
        await interaction.followup.send(embed=embedVar1)
    except:
        embedVar2 = discord.Embed(title="Command failed", description=f"Failed to execute command `{command}` on `{server.name}`", color=0xFF0037)
        await interaction.followup.send(embed=embedVar2)

@tree.command(name = "backup", description = "Creates a backup of smp.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(manage_messages = True)
async def self(interaction: discord.Interaction, backupname: typing.Optional[str] = None) -> None:
    await interaction.response.defer()
    if backupname is not None:
        await asyncio.create_subprocess_shell(f"zip -r {backupname}.zip world", cwd=smppath)
    else:
        proc = await asyncio.create_subprocess_shell(f"zip -r backup.zip world", cwd=smppath)
    embedVar1 = discord.Embed(title="Starting backup...", description=f"Started a backup of smp!", color=0xFF0068)
    await interaction.followup.send(embed=embedVar1)
    await proc.wait()
    embedVar2 = discord.Embed(title="Backup made", description=f"Successfully created a backup of smp", color=0x34EB86)
    await interaction.followup.send(embed=embedVar2)

@tree.command(name = "backuplist", description = "Shows the list of backups for smp.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(manage_messages = True)
async def self(interaction: discord.Interaction):
    resp = ""
    await interaction.response.defer()
    for file in os.listdir(smppath):
        if file.endswith(".zip"):
            resp += f"{file}, "
    resp2 = resp.strip(", ")
    embedVar1 = discord.Embed(title="Backup list", description=f"`{resp2}`", color=0xFF0068)
    await interaction.followup.send(embed=embedVar1)

paths = [workdir, smppath, cmppath]

@tree.command(name = "deletefile", description = "Deletes a file in one of the directories", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(administrator = True)
@app_commands.describe(directory = "The directory to delete a file in.")
@app_commands.choices(directory = [
    discord.app_commands.Choice(name="bot", value=0),
    discord.app_commands.Choice(name="smp", value=1),
    discord.app_commands.Choice(name="cmp", value=2),
])
async def self(interaction: discord.Interaction, file: str, directory: discord.app_commands.Choice[int]):
    await interaction.response.defer()
    path1 = paths[directory.value]
    if os.path.exists(f"{path1}/{file}"):
        os.remove(f"{path1}/{file}")
        embedVar1 = discord.Embed(title="Success!", description=f"Successfully removed file `{path1}/{file}`", color=0x34EB86)
    else:
        embedVar1 = discord.Embed(title="Error", description=f"File `{path1}/{file}` doesnt exist.", color=0xFF0037)
    await interaction.followup.send(embed=embedVar1)

@tree.command(name = "startcmp", description = "Starts CMP.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(manage_messages = True)
async def self(interaction: discord.Interaction):
    embedVar1 = discord.Embed(title="Starting...", description=f"Startup of cmp initialized!", color=0xFF0068)
    await interaction.response.send_message(embed=embedVar1)
    await startcmpm()

@tree.command(name = "stopcmp", description = "Stops CMP.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(manage_messages = True)
async def self(interaction: discord.Interaction):
    embedVar1 = discord.Embed(title="Stopping...", description=f"Startup of cmp initialized!", color=0xFF0068)
    await interaction.response.send_message(embed=embedVar1)
    cmps.terminate()

@tree.command(name = "startsmp", description = "Starts SMP.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(manage_messages = True)
async def self(interaction: discord.Interaction):
    embedVar1 = discord.Embed(title="Starting...", description=f"Startup of smp initialized!", color=0xFF0068)
    await interaction.response.send_message(embed=embedVar1)
    await startsmpm()

@tree.command(name = "stopsmp", description = "Stops SMP.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(manage_messages = True)
async def self(interaction: discord.Interaction):
    embedVar1 = discord.Embed(title="Stopping...", description=f"Startup of smp initialized!", color=0xFF0068)
    await interaction.response.send_message(embed=embedVar1)
    smps.terminate()

@tree.command(name = "stop", description = "Stops the bot.", guild = discord.Object(id = 1003365626825408604))
@app_commands.default_permissions(administrator = True)
async def self(interaction: discord.Interaction):
    try:
        cmps.terminate()
        smps.terminate()
    except:
        pass
    await interaction.response.send_message("**Stopping!**", ephemeral=True)
    exit()

@client.event
async def on_message(message: discord.Message):
    if message.channel == chan:
        if message.author.id != botid:
            outdc = "/tellraw @a [\"\",{\"text\":\"[Discord]\",\"color\":\"dark_gray\"},{\"text\":\" " + message.author.name + ": \",\"bold\":true,\"color\":\"blue\"},{\"text\":\"" + message.content + "\",\"color\":\"gray\"}]"
            await smpcomm(outdc)
            await cmpcomm(outdc)

sep = " "
async def startcmpm():
    cmpready = False
    startupcmp = str(f"java -Xmx6G -jar {cmppath}fabric-server-launch.jar nogui")
    global cmps
    cmps = await asyncio.create_subprocess_shell(startupcmp, cwd=cmppath, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
    try:
        while True:
            data = await cmps.stdout.readline()
            try:
                line = data.decode('ascii').rstrip()
            except:
                cmps.terminate()
                break
            if line != "":
                cmdline = line.split()
                if len(cmdline) >= 3:
                    if cmdline[1] + cmdline[2] == "[Serverthread/INFO]:":
                        msg = "[CMP] " + sep.join(cmdline[3::])
                        if msg.startswith(("[CMP] Starting minecraft server version", "[CMP] Loading properties", "[CMP] Default game type:", "[CMP] Generating keypair", "[CMP] Starting Minecraft server on", "[CMP] Using epoll channel type", "[CMP] Preparing level", "[CMP] [", "[CMP] Preparing start region for dimension", "[CMP] Starting GS4 status listener", "[CMP] Thread Query Listener started", "[CMP] Starting remote control listener", "[CMP] Thread RCON Listener started", "[CMP] RCON running on 0.0.0.0:25567", "[CMP] Saving chunks for level", "[CMP] ThreadedAnvilChunkStorage", "[CMP] com.mojang.authlib.GameProfile", "[CMP] /")):
                            pass
                        elif "logged in with entity id" in msg:
                            pass
                        else:
                            if cmpready is False:
                                cmpready = True
                            await cbsend(msg)
                            try:
                                outdc = "/tellraw @a [\"\",{\"text\":\"[CMP]\",\"color\":\"dark_gray\"},{\"text\":\" " + sep.join(cmdline[3::]) + "\",\"color\":\"gray\"}]"
                                await smpcomm(outdc)
                            except:
                                pass
    except KeyboardInterrupt:
        cmps.terminate()

async def cmpcomm(inp):
    with MCRcon(cmpip, cmprconpass, port=cmprconport) as mcr:
        mcr.command(f"{inp}")

async def startsmpm():
    smpready = False
    startupsmp = str(f"java -Xmx6G -jar {smppath}fabric-server-launch.jar nogui")
    global smps
    smps = await asyncio.create_subprocess_shell(startupsmp, cwd=smppath, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
    try:
        while True:
            data = await smps.stdout.readline()
            try:
                line = data.decode().rstrip()
            except:
                smps.terminate()
                break
            if line != "":
                cmdline = line.split()
                if len(cmdline) >= 3:
                    if cmdline[1] + cmdline[2] == "[Serverthread/INFO]:":
                        msg = "[SMP] " + sep.join(cmdline[3::])
                        if msg.startswith(("[SMP] Starting minecraft server version", "[SMP] Loading properties", "[SMP] Default game type:", "[SMP] Generating keypair", "[SMP] Starting Minecraft server on", "[SMP] Using epoll channel type", "[SMP] Preparing level", "[SMP] [", "[SMP] Preparing start region for dimension", "[SMP] Starting GS4 status listener", "[SMP] Thread Query Listener started", "[SMP] Starting remote control listener", "[SMP] Thread RCON Listener started", "[SMP] RCON running on", "[SMP] com.mojang.authlib.GameProfile", "[SMP] /")):
                            pass
                        elif "logged in with entity id" in msg:
                            pass
                        else:
                            if smpready is False:
                                smpready = True
                            await cbsend(msg)
                            try:
                                outdc = "/tellraw @a [\"\",{\"text\":\"[SMP]\",\"color\":\"dark_gray\"},{\"text\":\" " + sep.join(cmdline[3::]) + "\",\"color\":\"gray\"}]"
                                await cmpcomm(outdc)
                            except:
                                pass
    except KeyboardInterrupt:
        smps.terminate()

async def smpcomm(inp):
    with MCRcon(smpip, smprconpass, port=smprconport) as mcr:
        resp = mcr.command(f"{inp}")
        print(resp)

@tree.command(name = "stat", description = "Shows some stats from smp.", guild = discord.Object(id = 1003365626825408604))
@app_commands.describe(mode = "Stat display mode.")
@app_commands.choices(mode = [
    discord.app_commands.Choice(name="Total", value=1),
    discord.app_commands.Choice(name="Scoreboard", value=2),
    discord.app_commands.Choice(name="Name", value=3),
])
async def self(interaction: discord.Interaction, stype: str, stat: str, mode: discord.app_commands.Choice[int], pname: typing.Optional[str] = None) -> None:
    await interaction.response.defer()
    if mode.name == "Total":
        counter = 0
        pcounter = 0
        dirlist = os.listdir(path=f"{smppath}world/stats")
        for x in dirlist:
            if x.endswith(".json"):
                pcounter = pcounter+1
                with open(f"{smppath}world/stats/{x}", 'r') as f:
                    jsn = json.load(f)
                    try:
                        counter = counter + jsn["stats"][f"minecraft:{stype}"][f"minecraft:{stat}"]
                    except:
                        pass
        embedVar1 = discord.Embed(title=f"Stat `{stype}:{stat}`", description=f"Total count from `{pcounter}` players:", color=0xFF0068)
        embedVar1.add_field(name=f"`minecraft:{stype}:minecraft:{stat}`", value=f"`{counter}`", inline=False)
    elif mode.name == "Scoreboard":
        embedVar1 = discord.Embed(title=f"Stat scoreboard", description=f"`{stype}:{stat}` THIS IS WIP", color=0xFF0068)
    elif mode.name == "Name":
        embedVar1 = discord.Embed(title=f"Stat scoreboard", description=f"`{stype}:{stat}` THIS IS WIP", color=0xFF0068)
        """ dirlist = os.listdir(path="/home/ubuntu/servers/smp/world/stats")
        for x in dirlist:
            if mojang.get_name(x[:len(x) - 5]) == pname:
                with open(f"/home/ubuntu/servers/smp/world/stats/{x}", 'r') as f:
                    jsn = json.load(f)
                    try:
                        score = jsn["stats"][f"minecraft:{type}"][f"minecraft:{stat}"]
                    except:
                        pass
        embedVar1 = discord.Embed(title=f"Stat for player `{pname}`", description=f"`{stype}:{stat}`: `{score}`", color=0xFF0068) """
    await interaction.followup.send(embed = embedVar1)



"""         embedVar1 = discord.Embed(title=f"Stat scoreboard", description=f"`{stype}:{stat}`", color=0xFF0068)
        scoredict = {}
        dirlist = os.listdir(path="/home/ubuntu/servers/smp/world/stats")
        for x in dirlist:
            if x.endswith(".json"):
                with open(f"/home/ubuntu/servers/smp/world/stats/{x}", 'r') as f:
                    jsn = json.load(f)
                    try:
                        score = jsn["stats"][f"minecraft:{type}"][f"minecraft:{stat}"]
                        scoredict.update({f"{mojang.get_name(x)}": f"{score}"})
                    except:
                        pass
        print(scoredict)
        sscoredict = sorted(scoredict.items(), key=lambda x: x[1], reverse=True)
        print(sscoredict)
        print(type(sscoredict[0]))
 """    
    
client.run(bottoken)
