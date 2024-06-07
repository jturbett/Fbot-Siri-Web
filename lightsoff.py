# lights_off python 3.8 script
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

def set_pin_and_disconnect(bot, handler):
    handler.connected.wait()  # Wait until the bot is connected
    try:
        bot.write_pin(pin_number=7, pin_value=0, pin_mode="digital")
        logging.info("Set pin 7 to OFF.")
        time.sleep(2)  # Wait a moment to ensure the command is processed
    except Exception as e:
        logging.error("Failed to set pin 7: {}".format(e))
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

    # Start the pin setting thread
    pin_thread = threading.Thread(target=set_pin_and_disconnect, args=(fb, handler))
    pin_thread.start()

    # Wait for the pin setting thread to complete
    pin_thread.join()

    print("Operation completed. Pin 7 set to OFF and disconnected.")
