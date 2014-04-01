TwitchTVChatBot
===============

A simple IRC chat bot for the twitch.tv platform


To get started you will need your UserName, Channel (mine is my username in lowercase preceded by a '#'), and your OAuth token (http://twitchapps.com/tmi/)

botLoop is the function you want: param 's' can be gotten through the connectToTwitch function, 'channel' is the same channel as above.

Current Supported Commands:
!version -> Python version running
!count -> Current count (each invocation increases it by one)

To add your own, put some command keywords in the if-else statements, and fill in what they should do!
