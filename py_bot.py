from javascript import require, On, Once, AsyncTask, once, off
from simple_chalk import chalk
from random import randint

mineflayer = require("mineflayer")
mineflayer_pathfinder = require("mineflayer-pathfinder")


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

        self.bot.loadPlugin(mineflayer_pathfinder.pathfinder)

        self.start_events()

        # Mineflayer: Pathfind to goal
    def pathfind_to_goal(self, goal_location):
        try:
            self.bot.pathfinder.setGoal(
                mineflayer_pathfinder.pathfinder.goals.GoalNear(
                    goal_location["x"], goal_location["y"], goal_location["z"], 1
                )
            )

        except Exception as e:
            self.log(f"Error while trying to run pathfind_to_goal: {e}")


    def go_to_player(self, player):
    
        # Find all nearby players
        local_players = self.bot.players

        # Search for our specific player
        for el in local_players:
            player_data = local_players[el]
            if player_data["uuid"] == player:
                vec3_temp = local_players[el].entity.position
                player_location = vec3(
                    vec3_temp["x"], vec3_temp["y"] + 1, vec3_temp["z"]
                )

        # Feedback
        if player_location:
            self.log(
                chalk.magenta(
                    f"Pathfinding to player at {vec3_to_str(player_location)}"
                )
            )
            self.pathfind_to_goal(player_location)
        else:
            self.log(f"Player not found.")

    def find_closest_block(self, block_name):
        #self.log("Searching for ", block_name)
        # Get the bot's current position
        current_position = self.bot.entity.position
        
        # Define search radius
        radius = 10  # You can adjust this as needed
        
        closest_block = None
        closest_distance = float('inf')

        # Scan for blocks in the vicinity
        for x in range(int(current_position.x) - radius, int(current_position.x) + radius + 1):
            for y in range(int(current_position.y) - radius, int(current_position.y) + radius + 1):
                for z in range(int(current_position.z) - radius, int(current_position.z) + radius + 1):
                    block = self.bot.blockAt(vec3(x, y, z))

                    if block and block.name == block_name:
                        # Calculate distance to the block
                        distance = current_position.distanceTo(block.position)
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_block = block.position

        if closest_block:
            self.log(chalk.magenta(f"Closest {block_name} found at {vec3_to_str(closest_block)}"))
            return closest_block
        else:
            self.log(f"{block_name} not found within radius {radius}.")
            return None


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
                    
                # Look at coords
                elif "look at coords" in message:

                    # Find all nearby players
                    x, y, z = message.split(" ")[-3:]

                    # Feedback
                    block_vec3 = vec3(x, y, z)
                    self.log(chalk.magenta(vec3_to_str(block_vec3)))
                    self.bot.lookAt(block_vec3, True)

                # Say which block the bot is looking at
                elif "what do you see" in message:
                    block = self.bot.blockAtCursor()
                    if block:
                        self.bot.chat(f"Looking at {block.displayName}")
                    else:
                        self.bot.chat("Looking at air")

                elif "come to me" in message:
                    self.go_to_player(sender)

                elif "find" in message:

                    words = message.split()
                    if len(words)>1:
                        block = words[2]
                        x = self.find_closest_block(block)
                        self.pathfind_to_goal(x)
                    else:
                        self.log("Please ask a block to find")

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


