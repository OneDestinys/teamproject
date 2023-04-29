# Welcome to our Discord Bot!
## Installation Requirements:
1) Installation of Python 3.9 
2) Go to file directory, right click and open terminal
3) Run `pip install -r requirements.txt` (Credit: https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt)
4) Put your discord bot token (accessible under discord developer portal), transcript channel id, and mongodb url (accessible through mongodb atlas) in settings.py file
5) Invite the bot to your server (discord developer portal -> oauth2 -> url)
6) Then run `python discord_bot.py` 

# Bot Commands
!ban {user} or /ban {user}: Will ban the user from your guild

!ping or /ping: Will respond with pong

!panel: Will open up a panel where users can click on a button to create a ticket

!add {user} or /add {user}: Will add a user to your ticket

!close or /close: Will close the ticket, send a transcript to the user and the transcript channel

!cat or /cat: Will send an embed with a cat image and inspirational quote