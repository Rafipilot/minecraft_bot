import time
from mineflayer import Bot

# Function to create the bot
def create_bot():
    bot = Bot(
        host='Rafipilot.aternos.me',
        port=25565,
        username='Rafipilot',
        auth='microsoft',
        version='1.21.1'
    )

    @bot.event
    def spawn():
        print('Bot has spawned and is online!')
        bot.chat('Hello, I am a bot!')  # Print a message in Minecraft chat

    @bot.event
    def error(err):
        print('Error:', err)

    @bot.event
    def end():
        print('Bot has been disconnected. Attempting to reconnect...')
        reconnect()

    return bot

# Function to reconnect
def reconnect():
    time.sleep(5)  # Wait for a moment before reconnecting
    create_bot()

# Start the bot
if __name__ == "__main__":
    create_bot()
