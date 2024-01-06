# Installation

To install, simply run the "setup.bat" file with elevated privileges/administrator permissions. This will install the
necessary components required for the scripts to run.
It'll also install all the required python packages.

You'll need to get a twitch API token. This can be received from https://twitchtokengenerator.com/ . It is a good
idea to give the bot as little permissions as possible just in case your API keys get stolen somehow. These tokens
should go into [./DO NOT OPEN ON CAM/.env.account_details](./DO NOT OPEN ON CAM/.env.account_details). Note that this
file does not exist, but will need to be made. To make this simple, there is a
[./DO NOT OPEN ON CAM/.env.account_details_copy](./DO NOT OPEN ON CAM/.env.account_details_copy) file which contains
all the details you'll need. You'll just need to put in the API tokens and channel name in the right spot.

Note that you can allow these scripts to look at multiple channels. To do this, simply separate the channels with a 
comma (","), but do not put any spaces in!

You'll also need to tell it what channels it is allowed to do commands from. 

# Configuration
Configuration can be done in the [configs.json](./configs.json) file. This allows for enabling and disabling different
components of the app.

There may be more configurations added in future versions.

You'll also need to tell it what channels it is allowed to do commands from. This is done from the
[./DO NOT OPEN ON CAM/.env.account_details](./DO NOT OPEN ON CAM/.env.account_details) which was made in the 
installation step.

# Running
To run the script, simply run the "main.py" file. A command window should be opened. It will load all the modules and
configs, and then try to connect to twitch using the API token. If the connection is successful, a message should appear
in the command window stating that "We have connected as {twitch account name here}", where the {twitch account name
here} is replaced with the name of twitch account the API token is generated for.

Please note that the stream does not have to be live for the scripts to work! Any command that is entered while the
scripts are active will trigger the relevant events. Similarly, it will work on messages sent on any of the channels
the scripts are looking at. This means that a command doesn't have to be sent in your chat for something to happen as
long as a command is sent in a channel which you have allowed the scripts to respond to messages from.


It is also worth noting that at any point while the script is running, it can be updated. This means that at any point
what the scripts can do may change. This is to my discretion and may or may not help **or** hinder you.


## Possible actions
In theory, these scripts can do absolutely anything on your computer. Every option will have configs to enable/disable
each individual components. No harm is intended by these scripts, and I will not intentionally add anything which may
cause harm to a user or a computer. 

Additionally, anything which may cause changes to your device will always reset their changes before the script ends.
There may be certain circumstances in which this does not happen, for example if your computer crashes or if the script
is forcefully closed, however this is untested.
