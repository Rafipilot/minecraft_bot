import requests

def send_message(message):
    url = 'http://localhost:3000/chat'
    response = requests.post(url, json={'message': message})
    if response.status_code == 200:
        print('Message sent successfully:', response.json())
    else:
        print('Failed to send message:', response.json())


message = input("Enter a message for the bot: ")
send_message(message)
