const mineflayer = require('mineflayer');

// Create the bot
const bot = mineflayer.createBot({
  host: 'Rafipilot.aternos.me', 
  port: 25565, 
  username: 'Rafipilot', 
  auth: 'microsoft', 
  version: '1.21.1' 
});

// Event handlers
bot.on('spawn', () => {
  console.log('Bot has spawned and is online!');
  bot.chat('Hello, I am a bot!'); // Print a message in minecraft chat
});

bot.on('error', (err) => {
  console.log('Error:', err);
});

bot.on('end', () => {
  console.log('Bot has been disconnected. Attempting to reconnect...');
  reconnect();
});

// Function to reconnect
function reconnect() {
  // Use the same credentials to reconnect
  const newBot = mineflayer.createBot({
    host: 'Rafipilot.aternos.me', 
    port: 25565,
    username: 'Rafipilot',
    auth: 'microsoft',
    version: '1.21.1' 
  });

  newBot.on('spawn', () => {
    console.log('Reconnected successfully!');
  });

  newBot.on('error', (err) => {
    console.log('Error during reconnection:', err);
  });

  newBot.on('end', () => {
    console.log('Reconnection attempt failed. Retrying...');
    setTimeout(reconnect, 5000); // Retry every 5 seconds
  });
}


