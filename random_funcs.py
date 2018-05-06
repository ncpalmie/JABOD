import random

def playOdds(message):
    message_text = message.content[9:]
    str_array = message_text.split(', ')
    low = str_array[0]
    high = str_array[1]
    number = random.randint(int(low), int(high))
    return [low, high, str(number)]
    