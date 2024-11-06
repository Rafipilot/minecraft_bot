from javascript import require, On, Once, AsyncTask, once, off
#from simple_chalk import chalk
from arch__minecraft import arch
import ao_core as ao
import time
import math


agent = ao.Agent(arch, notes="Default Agent")


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

    def data(self):
        """
        Gathers input data for the neural network by checking if there are obstacles in front, left, and right.
        """
        # Check for a block directly in front
        if self.block_in_front() == True:
            block_in_front = 1 
        else:
            block_in_front = 0

        # Check for a block slightly to the left
        self.bot.lookAt(vec3(self.bot.entity.position.x - 1, self.bot.entity.position.y, self.bot.entity.position.z))
        if self.block_in_front()  == True:
            block_left = 1 
        else:
            block_left = 0

        # Check for a block slightly to the right
        self.bot.lookAt(vec3(self.bot.entity.position.x + 1, self.bot.entity.position.y, self.bot.entity.position.z))
        if self.block_in_front()  == True:
            block_right = 1 
        else:
            block_right = 0

        # Return surroundings as a list
        surroundings = [block_in_front, block_left ,block_right]
        self.bot.lookAt(vec3(self.bot.entity.position.x, self.bot.entity.position.y, self.bot.entity.position.z))  # Reset the look direction

        return surroundings

    def block_in_front(self, distance=1):
        """
        Checks if there's a block in front of the bot within a range.
        The forward direction is flipped by reversing dx and dz to correct orientation issues.
        """
        # Bot's current position and yaw (viewing angle)
        position = self.bot.entity.position
        yaw = self.bot.entity.yaw

        # Flip the direction vector to correct orientation
        dx = math.sin(yaw) * distance
        dz = -math.cos(yaw) * distance

        # Calculate the target position directly in front of the bot
        target_position = vec3(position.x + dx, position.y, position.z + dz)

        # Check the block at the target position
        block_in_front = self.bot.blockAt(target_position)

        if block_in_front and block_in_front.displayName != "Air":
            print("Detected block in front:", block_in_front.displayName)
            return True

        print("No block detected in front.")
        return False




    def move(self, response):
        # Reset all movement directions first to avoid unwanted motion
        self.bot.setControlState('forward', False)
        self.bot.setControlState('back', False)
        self.bot.setControlState('left', False)
        self.bot.setControlState('right', False)


        # Define movement logic based on response values
        if response == [1, 1]:
            # Move forward
            self.bot.setControlState('forward', True)
            print("moving")
        elif response == [1, 0]:
            # Move right
            self.bot.setControlState('right', True)
            print("moving")
        elif response == [0, 1]:
            # Move left
            self.bot.setControlState('left', True)
            print("moving")
        elif response == [0, 0]:
            self.bot.setControlState('forward', True)
            print("moving")
        time.sleep(0.2)
        self.bot.setControlState('forward', False)
        self.bot.setControlState('back', False)
        self.bot.setControlState('left', False)
        self.bot.setControlState('right', False)

    def go_to_player(self, player):
    
        # Find all nearby players
        local_players = self.bot.players

        # Search for our specific player
        for i in local_players:
            player_data = local_players[i]
            if player_data["uuid"] == player:
                vec3_temp = local_players[i].entity.position
                player_location = vec3(
                    vec3_temp["x"], vec3_temp["y"] + 1, vec3_temp["z"]
                )

        # Feedback
        if player_location:
            self.log(
                (
                    f"Pathfinding to player at {vec3_to_str(player_location)}"
                )
            )
            self.pathfind_to_goal(player_location)
        else:
            self.log(f"Player not found.")

    def find_closest_block(self, block_name):
        #self.log("Searching for ", block_name)
        # Get the bot's current position
        print("finding", block_name)
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
            self.log((f"Closest {block_name} found at {vec3_to_str(closest_block)}"))
            return closest_block
        else:
            #self.log(f"{block_name} not found within radius {radius}.")
            print("unable to find", block_name)
            return None


    def get_surroundings(self):

        bot_position = self.bot.entity.position
        
        pos = [bot_position.x,  bot_position.y, bot_position.z]
        health = self.bot.health
        dis_to_wood = self.find_closest_block("spruce_log")

        surrondings = [pos, dis_to_wood, health, ]
        return surrondings
    
    def start_events(self):

        @On(self.bot, "login")
        def login(this):
            # Displays which server you are currently connected to
            self.bot_socket = self.bot._client.socket
            self.log(
                (
                    f"Logged in to {self.bot_socket.server if self.bot_socket.server else self.bot_socket._host }"
                )
            )

                # Spawn event: Triggers on bot entity spawn

        @On(self.bot, "spawn")
        def spawn(this):
            self.log("Bot spawned. Checking readiness to teleport...")

            # Make sure the bot is ready
            if this.entity:  # Check if the bot has an entity
                self.log("Teleporting to coordinates (8.5, -60, -3.5)...")
                # Use this.entity.position to teleport
                this.entity.position.set(8.5, -60, -3.5)
                this.chat("Hi!")
            else:
                self.log("Bot entity not ready for teleportation.")

            self.bot.lookAt(vec3(11.8, -58, -3.7))

                # Kicked event: Triggers on kick from server
        @On(self.bot, "kicked")
        def kicked(this, reason, loggedIn):
            if loggedIn:
                self.log((f"Kicked whilst trying to connect: {reason}"))


        @On(self.bot, "death")
        def death(this):
            self.log("Bot has died!")
            agent.next_state(INPUT=surroudings, print_result=False, Cpos=False, Cneg= 
                             True).tolist()

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
                        self.log((vec3_to_str(player_location)))
                        self.bot.lookAt(player_location)
                    else:
                        self.log(f"Player not found.")
                    
                # Look at coords
                elif "look at coords" in message:

                    # Find all nearby players
                    x, y, z = message.split(" ")[-3:]

                    # Feedback
                    block_vec3 = vec3(x, y, z)
                    self.log((vec3_to_str(block_vec3)))
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

                elif("wander") in message:
                    self.random_wander()
        # End event: Triggers on disconnect from server
        @On(self.bot, "end")
        def end(this, reason):
            self.log((f"Disconnected: {reason}"))

            # Turn off old events
            off(self.bot, "login", login)
            off(self.bot, "spawn", spawn)
            off(self.bot, "kicked", kicked)
            off(self.bot, "messagestr", messagestr)

            # Reconnect
            if self.reconnect:
                self.log((f"Attempting to reconnect"))
                self.start_bot()

            # Last event listener
            off(self.bot, "end", end)

bot = Bot()
time.sleep(5)


previous_distance_to_goal_x = None
while True:
    bot_position = bot.bot.entity.position

    
    surroudings = bot.data()
    print(surroudings)
    response = agent.next_state(INPUT=surroudings, print_result=False).tolist()
    bot.move(response)

    goal_pos_x = 15

    distance_to_goal_x = abs(goal_pos_x - bot_position.x)
    print("distanme", distance_to_goal_x)
    if previous_distance_to_goal_x!=None:
        print(previous_distance_to_goal_x)
        if previous_distance_to_goal_x> distance_to_goal_x:
            agent.next_state(INPUT=surroudings, print_result=False, Cneg=False, Cpos=True)
            print("Pleasure signal: Getting closer to goal!")

        else:
            agent.next_state(INPUT=surroudings, print_result=False, Cneg=True, Cpos=False)
            print("Pain signal: Moving away from goal!")
    else:
        print(previous_distance_to_goal_x)

    
    previous_distance_to_goal_x = distance_to_goal_x
    time.sleep(2)
    pass