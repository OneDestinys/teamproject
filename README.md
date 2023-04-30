# We Built a Discord Bot

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Evolution](#project-evolution)
- [Results](#results)
- [Contributing](#contributing)


## Overview
Summary of the project, goals and who did we build this for. any unique feature.

## Installation
1. Install Python 3.9 
2. Go to file directory, right click and open terminal
3. Run `pip install -r requirements.txt` (Credit: https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt)
4. Put your discord bot token (accessible under discord developer portal), transcript channel id, and mongodb url (accessible through mongodb atlas) in settings.py file
5. Invite the bot to your server (discord developer portal -> oauth2 -> url)
6. Then run `python discord_bot.py` 

## Usage


### Commands
!ban {user} or /ban {user}: Will ban the user from your guild

!ping or /ping: Will respond with pong

!panel: Will open up a panel where users can click on a button to create a ticket

!add {user} or /add {user}: Will add a user to your ticket

!close or /close: Will close the ticket, send a transcript to the user and the transcript channel

!cat or /cat: Will send an embed with a cat image and inspirational quote


## Project Evolution
We started the project by really talking to each other and pinpointing the key things that we wanted from this project, and developing a project timeline that will help us get to there. We broke the project into various steps,

1. Create a Discord account and a new application
2. Choose frameworks that best represents the project, suits the needs of our bot and something we are most comfortable working with



## Results
Upon installation, our bot should help you perform the following tasks:

1. Moderation commands (e.g. kick, ban, mute)
2. A ticket system that saves transcripts as text files
3. Can be used to automate repetitive tasks. For example welcome new members , assign tasks to them
4. It also entertains the users by sending funny cat photos


## Contributing
We used some help from ChatGPT, individuals, and internet sources such as Reddit.
