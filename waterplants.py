import json
import logging
import time
import threading
import requests
from farmbot import Farmbot, FarmbotToken

# Setup logging
log_file_path = '/home/joe.dockeroktapip/myflaskapp/wateritall.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define the path to the authentication and webhook files
auth_file_path = '/home/joe.dockeroktapip/myflaskapp/farmbot_authorization_token.json'
webhook_file_path = '/home/joe.dockeroktapip/myflaskapp/webhook_token.json'

# Load the existing authentication token from a file
try:
    with open(auth_file_path, 'r') as file:
        TOKEN = json.load(file)
except FileNotFoundError:
    logging.error(f"The file '{auth_file_path}' was not found.")
    exit(1)
except json.JSONDecodeError:
    logging.error(f"The file '{auth_file_path}' contains invalid JSON.")
    exit(1)
except Exception as e:
    logging.error(f"An unexpected error occurred while reading the token file: {e}")
    exit(1)

# Load the webhook URL from the JSON file
try:
    with open(webhook_file_path, 'r') as file:
        webhook_data = json.load(file)
        webhook_url = webhook_data['webhook_url']
except FileNotFoundError:
    logging.error(f"The file '{webhook_file_path}' was not found.")
    exit(1)
except json.JSONDecodeError:
    logging.error(f"The file '{webhook_file_path}' contains invalid JSON.")
    exit(1)
except Exception as e:
    logging.error(f"An unexpected error occurred while reading the webhook file: {e}")
    exit(1)

# Function to send a message to Microsoft Teams channel
def send_teams_message(message):
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "FarmBot Status",
        "text": message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        logging.info("Message sent successfully.")
    else:
        logging.error(f"Failed to send message: {response.status_code} - {response.text}")

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

def move_to_locations_and_water(bot, handler, locations):
    handler.connected.wait()  # Wait until the bot is connected
    try:
        for location in locations:
            # Move to the specified coordinates
            bot.move_absolute(x=location[0], y=location[1], z=0)
            logging.info(f"Moved to position (x={location[0]}, y={location[1]}, z=0).")
            send_teams_message(f"Moved to position (x={location[0]}, y={location[1]}, z=0).")

            # Wait until the bot reaches the target position within a tolerance of ±10 units
            target_position = (location[0], location[1], 0)
            tolerance = 10
            while True:
                current_position = bot.position()
                logging.info(f"Current position: {current_position}")
                if all(abs(current - target) <= tolerance for current, target in zip(current_position, target_position)):
                    break
                time.sleep(1)  # Wait before checking again

            # Turn on pin 8 for 1 second
            bot.write_pin(pin_number=8, pin_value=1, pin_mode="digital")
            logging.info("Set pin 8 to ON.")
            send_teams_message("Set pin 8 to ON.")
            time.sleep(1)
            bot.write_pin(pin_number=8, pin_value=0, pin_mode="digital")
            logging.info("Set pin 8 to OFF.")
            send_teams_message("Set pin 8 to OFF.")

            # Pause before moving to the next location
            time.sleep(2)

        # Move back to the initial coordinates
        bot.move_absolute(x=0, y=0, z=0)
        logging.info("Moved back to position (x=0, y=0, z=0).")
        send_teams_message("Moved back to position (x=0, y=0, z=0).")
    except Exception as e:
        logging.error("Failed to set pin or move: {}".format(e))
        send_teams_message(f"Failed to set pin or move: {e}")
    finally:
        try:
            bot._connection.mqtt.disconnect()
            logging.info("Disconnected from FarmBot.")
            send_teams_message("Disconnected from FarmBot.")
        except Exception as e:
            logging.error(f"Failed to disconnect: {e}")
            send_teams_message(f"Failed to disconnect: {e}")

def main():
    # Send start message to Teams
    start_message = "Started webhook watering it all"
    logging.info(start_message)
    send_teams_message(start_message)

    try:
        # List of plant locations
        plant_locations = [
            (1200, 1040), (1200, 800), (2400, 1100), (1630, 750), (2000, 800),
            (2400, 240), (2700, 160), (2000, 200), (2700, 600), (2200, 600),
            (860, 900), (10, 1240), (500, 1240), (1700, 1240), (1800, 1240),
            (1900, 1240), (2700, 1000), (150, 980)
        ]

        # Create the Farmbot instance using the serialized token
        fb = Farmbot(raw_token)

        # Create the handler
        handler = MyHandler(fb)

        # Start the connection in a separate thread
        connect_thread = threading.Thread(target=fb.connect, name="connect_thread", args=[handler])
        connect_thread.start()

        # Start the movement and watering thread
        move_thread = threading.Thread(target=move_to_locations_and_water, args=(fb, handler, plant_locations))
        move_thread.start()

        # Wait for the move thread to complete
        move_thread.join()

        print("Operation completed. Moved to each location, turned pin 8 ON for 1 second at each, moved back to (x=0, y=0, z=0), and disconnected.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        send_teams_message(f"An error occurred: {e}")
    finally:
        # Ensure disconnection
        try:
            fb._connection.mqtt.disconnect()
            logging.info("Ensured disconnection from FarmBot.")
            send_teams_message("Ensured disconnection from FarmBot.")
        except Exception as e:
            logging.error(f"Failed to ensure disconnection: {e}")
            send_teams_message(f"Failed to ensure disconnection: {e}")

        # Send completion message to Teams
        stop_message = "Completed the webhook /water watering it all"
        logging.info(stop_message)
        send_teams_message(stop_message)

if __name__ == '__main__':
    main()
