const mineflayer = require('mineflayer');
const express = require('express');
const bodyParser = require('body-parser');

// Create the bot
const bot = mineflayer.createBot({
  host: 'Rafipilot.aternos.me',
  port: 25565,
  username: 'Rafipilot',
  auth: 'microsoft',
  version: '1.21.1'
});

// Set up a simple Express server
const app = express();
app.use(bodyParser.json());

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
  setTimeout(() => {
    bot = mineflayer.createBot({
      host: 'Rafipilot.aternos.me',
      port: 25565,
      username: 'Rafipilot',
      auth: 'microsoft',
      version: '1.21.1'
    });
  }, 5000); // Retry every 5 seconds
}

// API endpoint to send a message
app.post('/chat', (req, res) => {
  const message = req.body.message;
  if (message) {
    bot.chat(message);
    res.status(200).send({ status: 'Message sent', message });
  } else {
    res.status(400).send({ status: 'Error', message: 'No message provided' });
  }
});

// Start the server
app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
