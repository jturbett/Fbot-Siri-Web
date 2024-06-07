# This sets pins for lights and irrigation on for 1 minute, and turns off while notifying msft teams of the status.
import json
import logging
import time
import threading
import requests
from farmbot import Farmbot, FarmbotToken

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
    logging.error(f"An unexpected error occurred while reading the token file: {e}")
    exit(1)

# Serialize the token to a JSON string
raw_token = json.dumps(TOKEN)

# Load the webhook URL from the JSON file
try:
    with open('webhook_token.json', 'r') as file:
        webhook_data = json.load(file)
        webhook_url = webhook_data['webhook_url']
except FileNotFoundError:
    logging.error("The file 'webhook_token.json' was not found.")
    exit(1)
except json.JSONDecodeError:
    logging.error("The file 'webhook_token.json' contains invalid JSON.")
    exit(1)
except Exception as e:
    logging.error(f"An unexpected error occurred while reading the webhook file: {e}")
    exit(1)

# Function to send a message to Microsoft Teams channel
def send_teams_message(message, image_url):
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "FarmBot Status",
        "sections": [{
            "activityTitle": message,
            "activityImage": image_url
        }]
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        logging.info("Message sent successfully.")
    else:
        logging.error(f"Failed to send message: {response.status_code} - {response.text}")

# Create a Farmbot instance using the encrypted token
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

def set_pins_and_disconnect(bot, handler):
    handler.connected.wait()  # Wait until the the bot is connected
    image_url = "https://forum.farmbot.org/uploads/default/original/2X/3/3644d5941650ef4a0e9b91eb44d46c7d05faea05.png"
    try:
        bot.write_pin(pin_number=7, pin_value=1, pin_mode="digital")
        bot.write_pin(pin_number=10, pin_value=1, pin_mode="digital")
        logging.info("Set pin 7 (lights) and pin 10 (irrigation) to ON.")
        send_teams_message("FarmBot: Lights (pin 7) and irrigation (pin 10) have been set to ON.", image_url)
        
        time.sleep(60)  # wait for 1 minute
        
        bot.write_pin(pin_number=7, pin_value=0, pin_mode="digital")
        bot.write_pin(pin_number=10, pin_value=0, pin_mode="digital")
        logging.info("Set pin 7 (lights) and pin 10 (irrigation) to OFF.")
        send_teams_message("FarmBot: Lights (pin 7) and irrigation (pin 10) have been set to OFF.", image_url)
    except Exception as e:
        logging.error("Failed to set pins: {}".format(e))
        send_teams_message(f"FarmBot: Failed to set pins: {e}", image_url)
    finally:
        bot._connection.mqtt.disconnect()
        logging.info("Disconnected from FarmBot.")
        send_teams_message("FarmBot: Disconnected.", image_url)

if __name__ == '__main__':
    # Create the Farmbot instance using the encrypted token
    fb = Farmbot(raw_token)

    # Create the handler
    handler = MyHandler(fb)

    # Start the connection in a separate thread
    connect_thread = threading.Thread(target=fb.connect, name="connect_thread", args=[handler])
    connect_thread.start()

    # Start the pin setting thread
    pin_thread = threading.Thread(target=set_pins_and_disconnect, args=(fb, handler))
    pin_thread.start()

    # Wait for the pin setting thread to complete
    pin_thread.join()

    print("Operation completed. The Lights (pin 7) and irrigation (pin 10) are set to ON, waited 1 minute, and then set to OFF.")
