# Fbot-Siri-Web
python code for manipulating Farmbot with Siri
Siri to Farmbot Automation Project (Fbotweb)

Overview
This project aims to automate and demonstrate the functionalities of a Farmbot using a combination of Siri, Python, MQTT, Flask, Microsoft Teams, and Azure. The primary motivation behind this project was to address the inconvenience of manually operating the Farmbot in front of neighbors, family members, and friends. By leveraging existing technologies and integrating various tools, this project allows for seamless control and demonstration of the Farmbot through simple commands.

Motivation
Out of an abundance of frustration when neighbors, family members, and friends wanted to see the Farmbot in action, I decided to create a more efficient solution. I hated having to run to the house, get my phone or iPad, and navigate through the bright sun to initiate a sequence or manually manipulate the Farmbot. With some experience in AI work using my Nvidia AGX sidecar over the last two seasons, I leveraged Python interactions with MQTT and built on the webhook work I did with Microsoft Teams for tracking and other external workflows.

Project Description
This project integrates the following components:

MQTT: Used for communication between the Farmbot and the Python scripts.
Python Flask: A web framework used to create a local server that handles POST requests.
Apache: Used as the WSGI server to host the Flask app.
Azure Docker Container: The Flask app and Python scripts are hosted on Azure in a Docker container.
Microsoft Teams: Sends notifications for tracking interactions and workflows.
iOS Shortcuts: Created shortcuts that Siri voice commands trigger the Flask app, which then initiates the desired Farmbot actions.
Farmbot: is an open-source, autonomous farming robot that uses computer numerical control (CNC) to help people grow food. 
Features
Remote Operation: Allows remote operation of the Farmbot using iOS shortcuts.
Automated Demonstrations: Demonstrates Farmbot functionalities with commands like "exercise the farmbot", "show off the farmbot", "demo the bot", and "water the rock".
Integration with Teams: Sends messages to Microsoft Teams to notify of actions taken.
Local Logging: Logs interactions with MQTT/Farmbot for tracking and debugging purposes.
External Control: Handles external solenoids for irrigation, enabling control over additional garden tasks.
Usage
Setup: Ensure the Python Flask app is hosted on an accessible to Siri using a WSGI such as NGINX Apache alternativly one could run this on Django.
iOS Shortcuts: Use the provided iOS shortcuts to interact with the Farmbot that can be shared to other family members who need to show off the Farmbot.
Commands:
Exercise the Farmbot: Moves the Farmbot tool to a specified coordinate, drops water, and returns to the home position.
Show Off the Farmbot:  " " 
Demo the Bot:  " "
Water the Rock: " "
Irrigation Control: Activates an external solenoid for 10 minutes to handle garden irrigation.
Future Enhancements
Integration with Nvidia Cameras: Explore the possibility of integrating Nvidia ecosystems cameras with Apple Vision Pro for an immersive garden experience.
Extended Automation: Add more automation scripts to handle additional tasks and scenarios.
Contribution
Feel free to contribute to this project by submitting issues or pull requests on GitHub. Suggestions for improvements and new features are always welcome.

Acknowledgments:
Special thanks to John Simmonds for his guidance on Python with MQTT and to everyone who provided support and feedback throughout the development of this project as well as the Farmbot team for pushing technology and engineering for the greater good.
MIT License 
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
