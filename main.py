import loguru
from discord.ext.commands import Bot
from discord import Intents
from configparser import ConfigParser
import time

c = ConfigParser()
file = open("settings.ini", "r")
text = file.read()
file.close()
del file

#money_cathced = 0

#client = Bot(["Catcher", "catcher"], self_bot=True, intents=Intents.all())

class getLogger():
	def __init__(self):
		self.log = loguru.logger
		self.log.add("logs/log_{time}.log")

	def get(self):
		return self.log

logger = getLogger().get()

if text == "":
	logger.info("Enter user token for connecting to your account.")
	token = input("Token: ")

	logger.info("Good. Now enter guild id where you want farm some money.")
	guildID = int(input("Guild ID: "))

	logger.info("Good. Now enter channel id where you can send command")
	channelID = int(input("Channel ID: "))

	logger.info("Enter command for work (Default: !work)")
	command = input("Command (Default: !work): ")
	if command == "":
		command = "!work"
		logger.info("Default command")

	logger.info("Enter SECONDS. This is enterval of sending commands.")
	seconds = int(input("Seconds: "))

	c["settings"] = {
	"token": token, # 0
	"guild": guildID, # 1
	"channel": channelID, # 2
	"command": command, # 3
	"interval": seconds # 4
	}
	with open("settings.ini", "w") as w:
		c.write(w)
		#w.close()

	logger.info("Done, restart the bot...")
	input()
	exit(0)

client = Bot(["Catcher", "catcher"], self_bot=True, intents=Intents.all())
config = c.read("settings.ini")

@client.event
async def on_ready():
	logger.info("Bot logged")

	while True:
		channel = None
		#guild = None

		try:
			channel = client.get_guild(int(c.get("settings", "guild"))).get_channel(int(c.get("settings", "channel")))
		except Exception as error:
			logger.fatal("Can't get channel! Log: " + error)
			logger.fatal("Shutdowning! Press ENTER for close.")
			input()
			exit(0)

		await channel.send(str(c.get("settings", "command")))
		logger.info("Command sent.")
		time.sleep(int(c.get("settings", "interval")))


client.run(str(c.get("settings", "token")), bot=False)

