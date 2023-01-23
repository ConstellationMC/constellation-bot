# constellation-bot
Bot for the Constellation minecraft server. 

See the Getting started page for more info on how to configure the bot.

---

Available commands
---
**Server**
*These commands are used to interact with the ingame servers*
| Name | Arguments | Description |
| ----------- | ----------- | ----------- |
| ping | None | Pings the servers to check their status/mspt/tps. |
| execute | server*, command* | Executes a command on one of the servers. |
| backup | backupname | Creates a backup of smp. |
| backuplist | None | Shows the list of backups for smp. |
| startsmp | None | Starts smp with chatbridge. |
| startcmp | None | Starts cmp with chatbridge. |
| stop | None | Stops the bot. |
| stat | stype*, stat*, mode*, pname | Checks the stat files for smp and returns a specified statistic. |
| deletefile | directory*, file* | Deletes a file in one of the important directories. |

**To-do**
*These commands are used to manage the todolist for projects*
| Name | Arguments | Description |
| ----------- | ----------- | ----------- |
| addtask | name*, priority*, tag, description, attachment | Pings the servers to check their status/mspt/tps. |
| edittask | task*, priority, tag, description, attachment | Edits the value of a task. |
| todolist | None | Shows the todolist. |
| deletetask | task* | Deletes a task. |
| markdone | task* | Marks a task as done. |
| donelist | None | Shows the list of done tasks. |
| taskinfo | task* | Shows all the info about a task. |

*Bolt network planner + scripting commands not included as they are wip, reffer to the slash commands menu in the discord client if you wish to use them*

**: required*

---
Getting started
---
**Installing the bot**
First, download the package off github. Next, go to the [discord developer portal](https://discord.com/developers/applications) and create an application. Create a bot, and enable the message content privileged intent. **Making the bot private is highly recommended**, as the bot can modify the files on your server. Now you can invite the bot. Open the `main.py` file you downloaded in the first step, and fill out the `bottoken` variable with the token we obtained from the developer portal. Now, you are ready to run the bot (if you want to use features from the server category, you need to complete the steps in the Setting up server functionality section of this article).

**Setting up server functionality**
*If you wish to use the functions outlined in the server category, please follow these steps. Prerequisites: 2 fabric minecraft servers running [carpet mod](https://github.com/gnembon/fabric-carpet), with the proper rcon and main ports accessible from the bots enviroment, a discord server that the bot will be setup in.*
First, create a channel in the discord server you invited the bot to. This channel will be used to broadcast messages from the minecraft servers onto discord. Next, go into the advanced tab in your discord settings and enable developer mode. Now, rightclick the channel you just created, and copy its id, then set the `chatbridgechanid` variable in `main.py` using it. Copy the bots id, and do the same with the `botid` variable. Now, navigate to the folder in which the `world` folder, `fabric-server-launch` file and the `server.properties` file of your smp is located. Spawn a new python shell here, and type `import os`, then do `os.getcwd()`. Now, copy the path and add a backslash after the last character. Take this value and use it to set the `smppath` variable. Repeat this process for the cmp server/`cmppath` var. Now navigate back to where we got the path for smp, and open the `server.properties` file. Locate the `rcon.password` and `rcon.port` values, and set them accordingly. Now, set the `smprconpass` and `smprconport` to the same values as you did for the variables in `server.properties`. Repeat for cmp. All thats left is just to fill in the ips of the servers and start the bot. Once you do so, make sure both servers are off, and that the bot can access the channel you set as the chatbridge channel. Start the servers using /startsmp and /startcmp. After a few moments, you should get a bunch of messages in the channel saying the servers have successfully started. You can try out the /ping command or /execute command too to make sure rcon is working correctly. Congratulations! Chabridge is now working.

---
Planned features
---
*Pasted from discord*

**planner**
- [ ] get gnome to finish mst algo
- [ ] finish the subnet thing, tho i have to consult gnome on this (also do clustering)

**scoreboard**
- [ ] finish/fix scoreboard and name mode

**applications**
- [ ] add ticketing capabilities, make it auto create tickets from form
- [ ] make it automatically create a vote

**chatbridge**
- [ ] add reply in mc feature

**scripting**
- [ ] add command for creating scripts, adding lines to scripts, deleting lines from scripts, deleting scripts, running scripts, listing scripts, adding descriptions, showing script info

**others**
- [ ] help command
- [ ] "n days since someone broke the constellation bot" status
- [ ] mqtt nugg chatbridge
- [ ] docker container based stdout and server control 

---
User defined variables
---
Before you can start using the bot, you need to fill these variables (only fill out the one you need, provided you wont use the other functions):

> **bottoken** = "*random string of symbols you get from the developer portal*" ***required***
**botid** = *the user id of the bot, example: 1027583573378736128* ***required for chatbridge***
**chatbridgechanid** = *the id of the channel you want messages from the mc servers to be sent to, example: 1051774768518549545* ***required for mc to discord chatbridge***
**smppath** = *the path in which the fabric server executable and the world file for the smp server can be found, example: r"/home/ubuntu/servers/smp"* ***required for smp out chatbridge, stat command***
**cmppath** = *the path in which the fabric server executable and the world file for the cmp server can be found, example: r"/home/ubuntu/servers/cmp* ***required for cmp out chatbridge***
**smprconpass** = "*the rcon.password variable value in the server.properties file of the smp server*" ***required for smp in chatbridge, execute smp command, ping command***
**cmprconpass** = "*the rcon.password variable value in the server.properties file of the cmp server*" ***required for cmp in chatbridge, execute cmp command, ping command***
**smpip** = *the ip adress of the smp server, example: "129.145.186.215"* ***required for smp in chatbridge, execute smp command, ping command***
**cmpip** = *the ip adress of the cmp server, example: "129.147.196.215"* ***required for cmp in chatbridge, execute cmp command, ping command***
**smprconport** = *the rcon.port variable value in the server.properties file of the smp server, example: 25575* ***required for smp in chatbridge, execute cmp command, ping command***
**cmprconport** = *the rcon.port variable value in the server.properties file of the cmp server, example: 25575* ***required for cmp in chatbridge, execute cmp command, ping command***
