import requests

def move_bot(direction):
    url = 'http://localhost:3000/move'
    payload = {'direction': direction}
    response = requests.post(url, json=payload)
    print(response.text)

# Example usage
move_bot('forward')  # Moves the bot forward
move_bot('right')    # Moves the bot to the right
