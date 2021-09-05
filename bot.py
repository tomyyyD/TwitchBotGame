'''
COPYRIGHT INFO
--------------
Some code in this file is licensed under the Apache License, Version 2.0.
http://aws.amazon.com/apache2.0/
'''

from irc.bot import SingleServerIRCBot
from requests import get
import socket
import threading


NAME = "MediaBot"
OWNER = "tommyyyyyd"


class Bot(SingleServerIRCBot):
    def __init__(self):
        # all of the stuff that bot needs to log in
        self.HOST = 'irc.chat.twitch.tv'
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = 'de0kkmveoe7es54066bmibvv9lmymi'
        self.TOKEN = "9t1f06ut5ldl1xv7gi1j3fpj72wc2t"
        self.CHANNEL = f"#{OWNER}"
        self.PREFIX = '!'
        self.HEADERSIZE = 10

        # tracked variables
        self.pogCount = 0

        # creates server connection
        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.bind((socket.gethostname(), 1024))
        # self.s.listen(5)

        # bot actually logging in
        url = f'https://api.twitch.tv/kraken/users?login={self.USERNAME}'
        headers = {'Client-ID': self.CLIENT_ID,
                   'Accept': 'application/vnd.twitchtv.v5+json'}
        r = get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']
        super().__init__(
            [(self.HOST, self.PORT, f'oauth:{self.TOKEN}')], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        # feddback for when the bot is live
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        # joins channel chat
        cxn.join(self.CHANNEL)
        self.send_message("now online.")

    def on_pubmsg(self, cxn, event):
        # for every message in chat, get the message content and user data
        tags = {kvpair["key"]: kvpair["value"]
                for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        # gets the message content
        message = event.arguments[0]

        # print(f"message from {user['name']}: {message}")

        # checks to see if the message starts with the bot prefix
        if (message.startswith(self.PREFIX)):
            # strips prefix off of message
            fullText = message.lstrip(self.PREFIX)
            # self.send_message(fullText)

            # splits command and message in an array
            splitText = fullText.split(' ')
            command = splitText[0]
            # print(command)
            self.checkCommand(command)

    def send_message(self, message):
        # sends a message in chat
        self.connection.privmsg(self.CHANNEL, message)

    def checkCommand(self, inCommand):
        command = inCommand.lower()
        # print(command)
        if (command == 'poggers' or command == "pog" or command == "poggies"):
            self.pogCount += 1
            self.sendToServer(self.pogCount)

        # game controls
        elif (command == 'left'):
            self.sendToServer('a')
        elif (command == 'right'):
            self.sendToServer('d')
        elif (command == 'up'):
            self.sendToServer("w")
        elif(command == 'down'):
            self.sendToServer('s')

    def sendToServer(self, msg):
        # connects to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 1024))
        s.send(bytes(str(msg), 'utf-8'))
        s.close()

    # def sendToServer(self, msg):
    #     clt, adr = self.s.accept()
    #     print(f"connection to {adr} established")
    #     count = str(msg)
    #     clt.send(bytes(count, "utf-8"))
    #     clt.close()


if __name__ == "__main__":
    bot = Bot()
    bot.start()
