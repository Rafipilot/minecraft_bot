const mineflayer = require('mineflayer');
const { Client } = require('minecraft-protocol');

// Create the bot
const bot = mineflayer.createBot({
  host: 'Rafipilot.aternos.me', // Replace with your Aternos server address
  port: 25565, // Default port, change if necessary
  username: 'Rafipilot', // Replace with your Microsoft email
  auth: 'microsoft', // Use Microsoft authentication
  version: '1.21.1' // Specify your server version (e.g., '1.16.4')
});

// Event handlers
bot.on('spawn', () => {
  console.log('Bot has spawned and is online!');
});

bot.on('error', (err) => {
  console.log('Error:', err);
});

bot.on('end', () => {
  console.log('Bot has been disconnected. Attempting to reconnect...');
  // Optionally, you can try to reconnect after disconnection
  setTimeout(() => {
    reconnect();
  }, 5000); // 5 seconds delay before reconnecting
});

// Function to reconnect
function reconnect() {
  const newBot = mineflayer.createBot({
    host: 'Rafipilot.aternos.me', // Replace with your Aternos server address
    port: 25565, // Default port, change if necessary
    username: 'Rafipilot', // Replace with your Microsoft email
    auth: 'microsoft', // Use Microsoft authentication
    version: '1.21.1' // Specify your server version (e.g., '1.16.4')
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
