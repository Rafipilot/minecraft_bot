from javascript import require, On, Once, AsyncTask, once, off
from simple_chalk import chalk
from random import randint

mineflayer = require("mineflayer")
vec3 = require("vec3")

server_host = "localhost" #Note: we can change to server later
server_port = 3000
reconnect = True
bot_name = "aolabs"


def vec3_to_str(v):
    return f"x: {v['x']:.3f}, y: {v['y']:.3f}, z: {v['z']:.3f}"


class Bot:
    def __init__(self):
        self.bot_args = {
            "host": server_host,
            "port": server_port,
            "username": bot_name,
            "hideErrors": False,
        }
        self.reconnect = reconnect
        self.bot_name = bot_name
        self.start_bot()

    def log(self, message):
        print(self.bot.username, message)

        # Start mineflayer bot
    def start_bot(self):
        self.bot = mineflayer.createBot(self.bot_args)

        self.start_events()

    def start_events(self):

        @On(self.bot, "login")
        def login(this):
            # Displays which server you are currently connected to
            self.bot_socket = self.bot._client.socket
            self.log(
                chalk.green(
                    f"Logged in to {self.bot_socket.server if self.bot_socket.server else self.bot_socket._host }"
                )
            )

                # Spawn event: Triggers on bot entity spawn
        @On(self.bot, "spawn")
        def spawn(this):
            self.bot.chat("Hi!")

                # Kicked event: Triggers on kick from server
        @On(self.bot, "kicked")
        def kicked(this, reason, loggedIn):
            if loggedIn:
                self.log(chalk.redBright(f"Kicked whilst trying to connect: {reason}"))

            # Chat event: Triggers on chat message
        @On(self.bot, "messagestr")
        def messagestr(this, message, messagePosition, jsonMsg, sender, verified=None):
            if messagePosition == "chat":
                if "quit" in message:
                    self.bot.chat("Goodbye!")
                    self.reconnect = False
                    this.quit()
                elif "flip a coin" in message:
                    if randint(1, 2) == 1:
                        self.bot.chat("Heads!")
                    else:
                        self.bot.chat("Tails!")
                elif "roll a dice" in message:
                    self.bot.chat(f"You rolled {randint(1, 6)}")

                elif "look at me" in message:
                    local_players = self.bot.players
                    for i in local_players:
                        player_data = local_players[i]
                        if player_data["uuid"] == sender:
                            vec3_temp = local_players[i].entity.position
                            player_location = vec3(
                                vec3_temp["x"], vec3_temp["y"] + 1, vec3_temp["z"]
                            )

                    # Feedback
                    if player_location:
                        self.log(chalk.magenta(vec3_to_str(player_location)))
                        self.bot.lookAt(player_location)
                    else:
                        self.log(f"Player not found.")
        # End event: Triggers on disconnect from server
        @On(self.bot, "end")
        def end(this, reason):
            self.log(chalk.red(f"Disconnected: {reason}"))

            # Turn off old events
            off(self.bot, "login", login)
            off(self.bot, "spawn", spawn)
            off(self.bot, "kicked", kicked)
            off(self.bot, "messagestr", messagestr)

            # Reconnect
            if self.reconnect:
                self.log(chalk.cyanBright(f"Attempting to reconnect"))
                self.start_bot()

            # Last event listener
            off(self.bot, "end", end)


ao_bot = Bot()