# IRC-animal-game
An IRC bot animal game: This bot generates animals in your IRC channel and users in the channel can either save or kill the generated animal. The object of the game is to be the first person in the channel to save or kill an animal and statistics are kept of the winners of the game.

## Configuring the bot

1. pip install irc
1. make a directory under your HOME directory called "data"
1. modify animal.py and:
1. change "server" to the host name of your IRC server
1. change "channel" to the channel you want the bot to connect to
1. decide on the nicks that you want to have adminstrative access to control the bot and add these nicks in "animal_admins" in lower case
1. change "animal_database" to the directory of your newly-created data directory

## Running the bot
After configuring the bot, on Linux type: ./animal.py &

## How the game is played.

* An animal is printed to the channel you have configured at the top of every hour and at a random interval between 10 minutes and 50 minutes past the hour.
* Users of the channel compete to see who can save or kill the animal the fastest.
* The first person to save or kill an animal wins and a count is added to their score. If you are not the first person to save or kill an animal, "TOO LATE" will be printed to the channel.
* To save an animal, type !save or !bef or !befriend to the channel.
* To kill an animal, type one of: !kill !bang, !club, !axe, !ak47, !shoot, !spear, !harpoon, !choke, !hang, !murder, !squash, !squish, !stomp, !nuke, !eat
* All users of the channel can print statistics to see who is the leader of saves and kills. The method of kills are also recorded in the stats.

## The commands

* To get a list of commands, type !ahelp (animal help). The list of commands will be sent to the user in direct messages from the bot.
* The list of save and kill commands is listed and described above.
* !stats : shows your statistics
* !stats NICK : shows the statistics for the user, NICK
* !animals : shows all statistics on all the animals. Since it generates a lot of output, it is sent in direct messages from the bot.
* !animal ANIMAL : shows the save and kill statistics of the animal, ANIMAL
* !winner or !win or !won : shows who won the save or kill of the last animal.

## Administrative commands

* Only the nicks you have configured in "animal_admins" can execute these commands:
* !aoff : turn off the animal game (stop generating animals)
* !aon : turn it back on again
* !afast : make the animal game run fast. Two animals will be generated per minute. The main purpose of this is for testing. Type !afast again to toggle it.
* !atrigger : generate an animal immediately for testing purposes.
* !arooster : make a rooster appear at the top of the hour instead of a random animal. (Note that a random animal always appear at other times). Type !arooster again to toggle it.
