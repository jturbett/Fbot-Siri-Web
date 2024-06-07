#This is the python script refrenced from the URL http://yourapachehost.org/webhook from the myflaskapp
import json
import logging
import time
from farmbot import Farmbot, FarmbotToken
import threading

# Setup logging
logging.basicConfig(filename='/var/log/farmbot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the existing authentication token from a file
try:
    with open('farmbot_authorization_token.json', 'r') as file:
        TOKEN = json.load(file)
except FileNotFoundError:
    logging.error("The file 'farmbot_authorization_token.json' was not found.")
    exit(1)
except json.JSONDecodeError:
    logging.error("The file 'farmbot_authorization_token.json' contains invalid JSON.")
    exit(1)
except Exception as e:
    logging.error("An unexpected error occurred while reading the token file: {}".format(e))
    exit(1)

# Serialize the token to a JSON string
raw_token = json.dumps(TOKEN)

# Create a Farmbot instance using the serialized token
fb = Farmbot(raw_token)

class MyHandler:
    def __init__(self, bot):
        self.bot = bot
        self.connected = threading.Event()

    def on_connect(self, bot, mqtt_client):
        logging.info("Connected to FarmBot.")
        self.connected.set()  # Set the event to indicate connection is established

    def on_log(self, _bot, log):
        logging.info("LOG: {}".format(log['message']))
        print("LOG: " + log['message'])

    def on_response(self, bot, response):
        logging.info("Response received: {}".format(response))
        print("Response received: {}".format(response))

    def on_error(self, _bot, response):
        logging.error("ERROR: {}".format(response.id))
        logging.error("Reason(s) for failure: {}".format(str(response.errors)))
        print("ERROR: " + response.id)
        print("Reason(s) for failure: " + str(response.errors))

    def on_change(self, bot, state):
        logging.info("State changed.")
        print("State changed.")

def set_pin_move_and_disconnect(bot, handler):
    handler.connected.wait()  # Wait until the bot is connected
    try:
        # Turn on pin 7 for watering
        bot.write_pin(pin_number=7, pin_value=1, pin_mode="digital")
        logging.info("Set pin 7 to ON.")
        time.sleep(2)  # Wait a moment to ensure the command is processed

        # Move to the specified coordinates
        bot.move_absolute(x=1000, y=400, z=-150)
        logging.info("Moved to position (x=1000, y=400, z=-150).")

        # Wait until the bot reaches the target position within a tolerance of ±10 units
        target_position = (1000, 400, -150)
        tolerance = 10
        while True:
            current_position = bot.position()
            logging.info(f"Current position: {current_position}")
            if all(abs(current - target) <= tolerance for current, target in zip(current_position, target_position)):
                break
            time.sleep(1)  # Wait before checking again

        # Pause for 15 seconds
        logging.info("Pausing for 15 seconds.")
        time.sleep(15)

        # Move back to the initial coordinates
        bot.move_absolute(x=0, y=0, z=0)
        logging.info("Moved back to position (x=0, y=0, z=0).")

        # Wait until the bot reaches the target position within a tolerance of ±10 units
        target_position = (0, 0, 0)
        while True:
            current_position = bot.position()
            logging.info(f"Current position: {current_position}")
            if all(abs(current - target) <= tolerance for current, target in zip(current_position, target_position)):
                break
            time.sleep(1)  # Wait before checking again

        # Turn off pin 7
        bot.write_pin(pin_number=7, pin_value=0, pin_mode="digital")
        logging.info("Set pin 7 to OFF.")
    except Exception as e:
        logging.error("Failed to set pin or move: {}".format(e))
    finally:
        bot._connection.mqtt.disconnect()
        logging.info("Disconnected from FarmBot.")

if __name__ == '__main__':
    # Create the Farmbot instance using the serialized token
    fb = Farmbot(raw_token)

    # Create the handler
    handler = MyHandler(fb)

    # Start the connection in a separate thread
    connect_thread = threading.Thread(target=fb.connect, name="connect_thread", args=[handler])
    connect_thread.start()

    # Start the pin setting and move thread
    move_thread = threading.Thread(target=set_pin_move_and_disconnect, args=(fb, handler))
    move_thread.start()

    # Wait for the move thread to complete
    move_thread.join()

    print("Operation completed. Pin 7 turned ON, moved to position (x=1000, y=400, z=-150), paused, moved back to (x=0, y=0, z=0), turned OFF, and disconnected.")
