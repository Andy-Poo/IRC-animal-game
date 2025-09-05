#!/usr/bin/env python3

# bot server specific settings
server = "irc.yourircserverdomain"
channel = "#yourchannel"
nickname = "AnimalBot"
port = 6667

# the nicknames of the users who administer the animal bot (in lower case)
animal_admins = ["mod1", "mod2"]

# animal "database" to save stats during bot restarts
animal_database = "/home/andy/data/animal.pickle"

# flags for turning on debugging diagnostics
test = False
debug = False

# when the animal was generated
animal_time = 0

# lists containing the aninal generation intervals
seconds_list = []
minutes_list = []

# command to save and kill animals. for example,
# !save
# !kill
animal_save_commands = ['save', 'befriend', 'bef']
animal_kill_commands = ['kill', 'bang', 'club', 'axe', 'ak47', 'shoot', 'spear', 'harpoon', 'choke', 'hang', 'murder', 'squash', 'squish', 'stomp', 'nuke', 'eat']

animal_help = [
"!ahelp : Display this help text",
"!stats : Display your stats and the winning stats",
"!stats <nick>: Display the stats of nickname <nick> and the winning stats",
"!animals : Display all the save and kill counts on all the animals",
"!animal <animal> : Display the save and kill counts on animal <animal>",
"!winner or !win or !won : Display the user who won the last save or kill command"
]

animal_help += [
".",        
"SAVE COMMANDS:"
]
save_command_text = ""
for i in range(len(animal_save_commands)):
    save_command = animal_save_commands[i]
    save_command_text += f'!{save_command} '
animal_help.append(save_command_text)

animal_help += [
".",        
"KILL COMMANDS:"
]
kill_command_text = ""
kill_commands_sorted = sorted(animal_kill_commands)
for i in range(len(kill_commands_sorted)):
    kill_command = kill_commands_sorted[i]
    kill_command_text += f'!{kill_command} '
animal_help.append(kill_command_text)

# the animal game is enabled
animal_enabled = False

# fast mode is enabled
animal_fast_mode = False

# rooster mode is enabled
animal_rooster_mode = False

color_codes = {
    'white' : '00',
    'black' : '01',
    'blue' : '02',
    'green' : '03',
    'red' : '04',
    'brown' : '05',
    'purple' : '06',
    'orange' : '07',
    'yellow' : '08',
    'lime' : '09',
    'teal' : '10',
    'cyan' : '11',
    'royal' : '12',
    'pink' : '13',
    'gray' : '14',
    'silver' : '15'
}


import os.path
import time
import re
import random
import pickle

"""
this is the list of animals we support in the animal game
the dictionary key is the animal emoji,
which will be inserted into the output in the
required surrounding colons.
The dictionary items consist of these objects:
[0] the sound the animal makes
[1] the number of times the animal was saved
[2] the number of times the animal was killed
[3] the method of killing
"""
animals = {
    'alien': ['screech', 0, 0, {}],
    'ant': ['scurry', 0, 0, {}],
    'bat': ['screech', 0, 0, {}],
    'bear': ['growl', 0, 0, {}],
    'bee': ['buzz', 0, 0, {}],
    'beetle': ['burrow', 0, 0, {}],
    'butterfly': ['flutter', 0, 0, {}],
    'camel': ['snort', 0, 0, {}],
    'cat2': ['meow', 0, 0, {}],
    'chipmunk': ['squeak', 0, 0, {}],
    'cockroach': ['pitter-patter', 0, 0, {}],
    'cow2': ['moo', 0, 0, {}],
    'crab': ['itch', 0, 0, {}],
    'dog2': ['woof', 0, 0, {}],
    'duck': ['quack', 0, 0, {}],
    'eagle': ['screech', 0, 0, {}],
    'elephant': ['trumpet', 0, 0, {}],
    'fish': ['splash', 0, 0, {}],
    'frog': ['ribbit', 0, 0, {}],
    'giraffe_face': ['chew', 0, 0, {}],
    'goat': ['bleat', 0, 0, {}],
    'hatched_chick': ['cheep', 0, 0, {}],
    'hedgehog': ['rustle', 0, 0, {}],
    'kangaroo': ['boing', 0, 0, {}],
    'koala': ['grunt', 0, 0, {}],
    'leopard': ['growl', 0, 0, {}],
    'monkey': ['chatter', 0, 0, {}],
    'mouse': ['squeak', 0, 0, {}],
    'octopus': ['blurp', 0, 0, {}],
    'owl': ['hoot', 0, 0, {}],
    'ox': ['moo', 0, 0, {}],
    'panda_face': ['nibble', 0, 0, {}],
    'penguin': ['coo', 0, 0, {}],
    'pig2': ['oink', 0, 0, {}],
    'poodle': ['yap', 0, 0, {}],
    'rabbit2': ['squeak', 0, 0, {}],
    'racehorse': ['neigh', 0, 0, {}],
    'rat': ['squeak', 0, 0, {}],
    'rooster': ['cock-a-doodle-do', 0, 0, {}],
    'sauropod': ['roar', 0, 0, {}],
    'sheep': ['baa', 0, 0, {}],
    'skunk': ['phew', 0, 0, {}],
    'snail': ['squirm', 0, 0, {}],
    'snake': ['hiss', 0, 0, {}],
    'spider': ['eek', 0, 0, {}],
    'tiger2': ['growl', 0, 0, {}],
    'turkey': ['gobble-gobble', 0, 0, {}],
    'turtle': ['snap', 0, 0, {}],
    'water_buffalo': ['moo', 0, 0, {}],
    'whale': ['blow', 0, 0, {}],
    'wolf': ['howl', 0, 0, {}]
}

animal_emojis = {
    'alien': '👽',
    'ant': '🐜',
    'bat': '🦇',
    'bear': '🐻',
    'bee': '🐝',
    'beetle': '🪲',
    'butterfly': '🦋',
    'camel': '🐫',
    'cat2': '🐈',
    'chipmunk': '🐿️',
    'cockroach': '🪳',
    'cow2': '🐄',
    'crab': '🦀',
    'dog2': '🐕',
    'duck': '🦆',
    'eagle': '🦅',
    'elephant': '🐘',
    'fish': '🐟',
    'frog': '🐸',
    'giraffe_face': '🦒',
    'goat': '🐐',
    'hatched_chick': '🐣',
    'hedgehog': '🦔',
    'kangaroo': '🦘',
    'koala': '🐨',
    'leopard': '🐆',
    'monkey': '🐒',
    'mouse': '🐭',
    'octopus': '🐙',
    'owl': '🦉',
    'ox': '🐂',
    'panda_face': '🐼',
    'penguin': '🐧',
    'pig2': '🐷',
    'poodle': '🐩',
    'rabbit2': '🐇',
    'racehorse': '🐎',
    'rat': '🐀',
    'rooster': '🐓',
    'sauropod': '🦕',
    'sheep': '🐑',
    'skunk': '🦨',
    'snail': '🐌',
    'snake': '🐍',
    'spider': '🕷️',
    'tiger2': '🐅',
    'turkey': '🦃',
    'turtle': '🐢',
    'water_buffalo': '🐃',
    'whale': '🐳',
    'wolf': '🐺'
}

# this is the stats per user and the user entries
# are created in the dictionary when the user
# makes his or her first save or kill
animal_stats = {}

# when the bot calls animal_game, save the animal's name
animal_last = None

# the nickname of the user who made the first save or kill.
# this gets reset back to None when the bot reports the winner.
animal_person = None

# also save the nickname before it gets cleared
animal_person_prev = None

# method used to kill the animal
animal_method = None

animal_commands = ['ahelp', 'stats', 'animal', 'animals', 'win', 'winner', 'won']
animal_commands += animal_save_commands 
animal_commands += animal_kill_commands 
animal_commands += ['aoff', 'aon', 'afast', 'atrigger', 'arooster']

def animal_enable(flag=True):
    """Enable the playing of the animal game.

    flag : bool
        True to enable, False to disable
    """
    global animal_enabled
    global seconds_list
    global minutes_list
    # reset the animal generation times
    seconds_list = []
    minutes_list = []
    animal_enabled = flag

def animal_fast(flag=False):
    """Sets or clears the animal_fast_mode flag on the animal module.

    flag : bool
        True to turn on fast mode
    """
    global animal_fast_mode
    global seconds_list
    global minutes_list
    # reset the animal generation times
    seconds_list = []
    minutes_list = []
    animal_fast_mode = flag

def animal_name(animal):
    """Converts the animal name into a human-readable name.

    animal : str
        the name of the animal

    Returns:
        str : the simplified name of the animal
    """
    animal = animal.strip('0123456789')
    if animal == 'hatched_chick': animal = 'chick'
    elif animal == 'water_buffalo': animal = 'water buffalo'
    elif animal == 'giraffe_face': animal = 'giraffe'
    elif animal == 'panda_face': animal = 'panda'
    return animal

def animal_match(animal):
    """This name of an animal that does not have to be an exact match.

    animal : str
        the name of the animal that does not have to be the full
        emoji name

    Returns:
        tuple : (emoji:str, item=list)
    """
    if animal.find("cat") != -1:
        animal = "cat2"
    item = (None, None)
    for emoji in animals.keys():
        if emoji.find(animal) != -1:
            item = (emoji, animals[emoji])
            break
    return item

def animal_info(animal):
    """This gets the stats info for a specific animal.

    animal : str
        the name of the animal.
        it does not have to be an exact match of the emoji name.

    Returns:
        tuple : (saved:int, kills:int)
    """
    result = (0, 0,)
    (emoji, item) = animal_match(animal)
    if emoji:
        result = (item[1], item[2])
    return result

def animal_pick():
    """Picks an animal for the animal list at random.

    Returns:
        tuple : (emoji:str, sound:str, saved:int, killed:int, method:dict)
    """
    keys = []
    for key in animals.keys():
        keys.append(key)
    #if debug: print(f'animal keys={keys}')
    emoji = random.choice(keys)
    sound = animals[emoji][0]
    saved = animals[emoji][1]
    killed = animals[emoji][2]
    try:
        method = animals[emoji][3]
    except:
        method = {}
    if debug: print(f'animal_pick: method={method}')
    return (emoji, sound, saved, killed, method)

def animal_game(item=None):
    """The output that is sent to the chat window by the bot
    at random on a timer.

    Returns:
        str : text
    """
    global animal_time, animal_person, animal_last
    if debug: print(f'animal_game: item(1)={item}') 
    if debug: print(f'animal_game: animal_person={animal_person}') 
    if debug: print(f'animal_game: animal_person_prev={animal_person_prev}') 
    if debug: print(f'animal_game: animal_last={animal_last}') 
    red = color_codes['red']
    green = color_codes['green']
    # set the time the animal was generated
    animal_time = time.time()
    # set the animal person for the new game
    animal_person = 'unknown'
    if item is None:
        item = animal_pick()
    if debug: print(f'animal_game: item(2)={item}') 
    (emoji, sound, saved, killed, method) = item
    animal_last = emoji
    animal = animal_name(emoji).upper()
    result = ""
    if emoji in animal_emojis:
        result = f"\x03{red}%s\x03 %s \x03{green}%s\x03\n" % (sound.upper(), animal_emojis[emoji], animal)
    return result

def animal_game_chime():
    """Called to chime the rooster at the top of the hour.
    
    Returns:
        str : the result of animal_game
    """
    item = ['rooster'] + animals['rooster']
    if debug: print(f'animal_game_chime: item={item}') 
    if len(item) <= 4:
        item.append({})
    return animal_game(item)
    
def animal_save(user):
    """Called when a user makes a save.

    user : str
        the nickname of the user
    """
    global animal_person, animal_person_prev, animal_last
    if debug: print(f'animal_save: user={user}') 
    if debug: print(f'animal_save: animal_person={animal_person}') 
    if debug: print(f'animal_save: animal_person_prev={animal_person_prev}') 
    if debug: print(f'animal_save: animal_last={animal_last}') 
    # if the animal was already saved, then do nothing
    #if animal_person is None or animal_person_prev is None:
    if animal_person is None:
        return None
    animal_person_prev = animal_person = user
    if user not in animal_stats:
        animal_stats[user] = [0, 0, {}]
    # first index is the save stats
    animal_stats[user][0] += 1
    # the second index is the save stats
    if animal_last in animals:
        animals[animal_last][1] += 1
    # clear the animal person for the next game
    animal_person = None
    if debug: print(f'animal_save: animal_person_prev(2)={animal_person_prev}') 
    return animal_person_prev

def animal_kill(command, user):
    """Called when a user makes a kill.

    command : str
        the method of killing
    user : str
        the nickname of the user
    """
    global animal_person, animal_person_prev
    if debug: print(f'animal_kill: command={command}')
    if debug: print(f'animal_kill: user={user}')
    if debug: print(f'animal_kill: animal_person={animal_person}')
    if debug: print(f'animal_kill: animal_person_prev={animal_person_prev}')
    # if the animal was already saved, then do nothing
    #if animal_person is None or animal_person_prev is None:
    if animal_person is None:
        return None
    animal_person_prev = animal_person = user
    if user not in animal_stats:
        animal_stats[user] = [0, 0, {}]
    # second index is the kill stats
    animal_stats[user][1] += 1
    # if the third index is missing, add it
    if len(animal_stats[user]) < 3:
        animal_stats[user].append({})
    # third index is the kill method
    if command in animal_stats[user][2]:
        animal_stats[user][2][command] += 1
    else:
        animal_stats[user][2][command] = 1
    if animal_last in animals:
        if debug: print(f'animal_kill: animals[animal_last]={animals[animal_last]}')
        # the third index is the kill stats
        animals[animal_last][2] += 1
        # the fourth index is the method of kill dictionary
        if len(animals[animal_last]) <= 3:
            animals[animal_last].append({})
        d = animals[animal_last][3]
        if command not in d:
            d[command] = 1
        else:
            d[command] += 1
        animals[animal_last][3] = d
    # clear the animal person for the next game
    animal_person = None
    if debug: print(f'animal_kill: animal_person_prev(2)={animal_person_prev}')
    return animal_person_prev

def animal_print_stats(animal=None):
    """Print the stats on a specific animal or all animals.

    animal : str
        the name of an animal or None if all animals

    Returns:
        str : the stats for the animal or animals
    """
    color = color_codes['red']
    if debug: print(f'animal_print_stats: animal={animal}')
    result = ''
    if animal:
        (emoji, item) = animal_match(animal)
        if debug: print(f'animal_print_stats: emoji={emoji}')
        if debug: print(f'animal_print_stats: item={item}')
        if emoji and emoji in animal_emojis:
            (sound, saved, killed) = (item[0].upper(), item[1], item[2])
            animal = animal_name(emoji).upper()
            result = f"\n%s \x03{color}*%s*\x03 (%s) %d saved and %d killed\n" % (
                animal_emojis[emoji], animal, sound, saved, killed)
            if debug: print(f'animal_print_stats: item[3]={item[3]}')
            # index 3 is the method of kill
            for method in sorted(item[3]):
                result += '%s=%d, ' % (method, item[3][method])
            result += '\n'
    else:
        for emoji in sorted(animals):
            if emoji in animal_emojis:
                sound = animals[emoji][0].upper()
                saved = animals[emoji][1]
                killed = animals[emoji][2]
                animal = animal_name(emoji).upper()
                result += f"\n%s \x03{color}*%s*\x03 (%s) %d saved and %d killed" % (
                    animal_emojis[emoji], animal, sound, saved, killed)
    return result

def animal_user_stats(user, arg):
    """Print the stats for a user.

    user : str
        the user nickname
    arg : str
        optional username argument
    
    Returns:
        str : the stats results for the user
    """
    if debug: print(f'animal_user_stats: user={user}')
    if debug: print(f'animal_user_stats: arg={arg}')
    result = '\n'
    if debug: print(f'animal_user_stats: animal_stats={animal_stats}')
    if arg:
        user = arg
    if user in animal_stats:
        item = animal_stats[user]
        # check there are enough items to unpack
        if len(item) > 2:
            (saves, kills, method) = item
        else:
            (saves, kills) = item
            method = None
        result = "%s has saved %d animals and killed %d animals.\n" % \
            (user, saves, kills)
        if method:
            for item in sorted(method):
                result += "%s=%d, " % (item, method[item])
        result += "\nTotal saved and killed: %d" % (saves + kills)
    else:
        result = "%s has neither saved or killed an animal." % user

    top_saves = 0
    top_saves_user = None
    top_kills = 0
    top_kills_user = None
    top_total = 0
    top_total_user = None
    for user in animal_stats:
        item = animal_stats[user]
        # check there are enough items to unpack
        if len(item) > 2:
            (saves, kills, method) = item
        else:
            (saves, kills) = item
            method = None
        if saves > top_saves:
            top_saves = saves
            top_saves_user = user
        if kills > top_kills:
            top_kills = kills
            top_kills_user = user
        if saves + kills > top_total:
            top_total = saves + kills
            top_total_user = user
    result += "\n\n%s has made %s saves and is a tree hugging animal lover." % (top_saves_user, top_saves)
    result += "\n%s has made %s kills and is a Ted Nugent wannabe mass animal slayer." % (top_kills_user, top_kills)
    result += "\n%s has made the most saves + kills: %d" % (top_total_user, top_total)
    return result

def animal_winner(user, action=None):
    """Prints who won the game.

    user : str
        the user nickname
    action : str
        None: the user did not win
        'save': the user saved an animal
        'kill': the user killed an animal
        'query': the user is querying to see who won
    
    Returns:
        str : the winner
    """
    if debug: print(f'animal_winner: user={user}')
    if debug: print(f'animal_winner: action={action}')
    if debug: print(f'animal_winner: animal_person={animal_person}')
    if debug: print(f'animal_winner: animal_person_prev={animal_person_prev}')
    result = ''
    # if animal_person is None, someone already won
    if animal_person:
        if user == animal_person_prev:
            result = "\nYOU WON!!!"
        else:
            if animal_person_prev is None:
                result = "\nThe game hasn't started yet."
            else:
                result = "\n`%s` WON" % animal_person_prev
    else:
        if animal_last:
            the_animal = animal_name(animal_last).upper()
            if action is None:
                result = "\nTOO LATE"
            elif action == 'query':
                result = "\n`%s` WON" % animal_person_prev
            elif action == 'save':
                result = "\n%s saved a %s. Good job!" % (animal_person_prev, the_animal)
            elif action == 'befriend':
                result = "\n%s befriended a %s. Good job!" % (animal_person_prev, the_animal)
            elif action == 'kill':
                method = animal_method
                if animal_method == 'kill': method = 'killed'
                elif animal_method == 'bang': method = 'shot'
                elif animal_method == 'club': method = 'clubbed'
                elif animal_method == 'axe': method = 'axed'
                elif animal_method == 'ak47': method = 'postalized'
                elif animal_method == 'shoot': method = 'shot'
                elif animal_method == 'spear': method = 'speared'
                elif animal_method == 'harpoon': method = 'harpooned'
                elif animal_method == 'choke': method = 'choked'
                elif animal_method == 'hang': method = 'hanged'
                elif animal_method == 'murder': method = 'murdered'
                elif animal_method == 'squash': method = 'squashed'
                elif animal_method == 'stomp': method = 'stomped'
                elif animal_method == 'nuke': method = 'nuked'
                elif animal_method == 'eat': method = 'ate'
                result = "\n%s %s a %s. You must be hungry." % (animal_person_prev, method, the_animal)
    return result

def animal_command_handler(user, userhost, command, query):
    """This function handles the animal commands.

    user : str
        the user nickname in lower case
    userhost : str
        the host the user is connecting from
    command : str
        the animal command
    query : str
        the animal command arguments

    Returns:
        str : the text result
    """
    global animal_method, animal_rooster_mode
    if debug: print(f'animal_command_handler: user={user}')
    if debug: print(f'animal_command_handler: userhost={userhost}')
    if debug: print(f'animal_command_handler: command={command}')
    if debug: print(f'animal_command_handler: query="{query}"')
    result = ''
    tokens = query.split(' ')
    if debug: print(f'animal_command_handler: tokens="{tokens}"')
    # is the name animal?
    if len(tokens) >= 1:
        arg = tokens[0]
    else:
        arg = ''
    if debug: print(f'animal_command_handler: arg="{arg}"')
    # enable or disable the animal game
    if command == 'aoff' and user in animal_admins:
        if debug: print('animal_command_handler: animal OFF')
        animal_enable(False)
    elif command == 'aon' and user in animal_admins:
        if debug: print('animal_command_handler: animal ON')
        animal_enable(True)
    elif command == 'afast' and user in animal_admins:
        if debug: print(f'animal_command_handler: afast, user={user}, animal_fast_mode={animal_fast_mode}')
        animal_fast(not animal_fast_mode)
    elif command == 'atrigger' and user in animal_admins:
        if debug: print('animal_command_handler: TRIGGER')
        result = animal_game()
    elif command == 'arooster' and user in animal_admins:
        if debug: print(f'animal_command_handler: arooster, user={user}, animal_rooster_mode={animal_rooster_mode}')
        animal_rooster_mode = not animal_rooster_mode
    elif command in animal_save_commands:
        if animal_save(user):
            if command == 'save':
                action = 'save'
            else:
                action = 'befriend'
        else:
            action = None
        result = animal_winner(user, action=action)
    elif command in animal_kill_commands:
        if command == 'squish':
            command = 'squash'
        if animal_kill(command, user):
            action = 'kill'
            animal_method = command
        else:
            action = None
            animal_method = None
        result = animal_winner(user, action=action)
    elif command == 'ahelp':
        result = ''
        for text in animal_help:
            result += f'{text}\n'
    elif command == 'stats':
        result = animal_user_stats(user, arg)
    elif command == 'animal' and arg:
        result = animal_print_stats(arg)
    elif command == 'animals':
        result = animal_print_stats()
    elif command == 'winner' or command == 'win' or command == 'won':
        result = animal_winner(user, action='query')
    return result

def animal_dump():
    """Save an animal in the "database".
    """
    if debug: print(f'animal_dump: {animal_database}')
    data = (animals, animal_stats)
    try:
        pickle.dump(data, open(animal_database, "wb"))
    except Exception as e:
        print(f'animal_dump: Error:{e}')

def animal_load():
    """Load the animal stats from the "database".
    """
    global animals, animal_stats
    if debug: print(f'animal_load: {animal_database}')
    if os.path.isfile(animal_database):
        try:
            animals_old = animals
            data = pickle.load(open(animal_database, "rb"))
            animals, animal_stats = data
            for animal in animals_old:
                if animal in animals:
                    # fixup the sounds the animal makes
                    animals[animal][0] = animals_old[animal][0]
                else:
                    # add any new animals
                    animals[animal] = animals_old[animal]
        except Exception as e:
            print(f'animal_load: Error:{e}')


def animal_generate_times():
    global seconds_list
    global minutes_list
    seconds_list = []
    minutes_list = []

    # the rooster is generated on the top of the hour,
    # so don't generate an animal within 10 minutes of it
    countdown = random.randint(10, 50)
    minutes_list.append(countdown)

    # make the seconds random
    if animal_fast_mode:
        countdown = random.randint(10, 50)
    else:
        countdown = random.randint(0, 59)
    seconds_list.append(countdown)

    # if in fast mode, generate animals every minute
    if animal_fast_mode:
        minutes_list = []
        for i in range(60):
            minutes_list.append(i)
    return (seconds_list, minutes_list)

import threading

# this class handles background processing of animal generation
class AnimalThread(threading.Thread):
    def __init__(self):
        self.die = False
        self.channel = None
        self.c = None
        self.e = None
        self.animal_dump_counter = 0
        animal_generate_times()
        # initialize the parent instance
        super(AnimalThread, self).__init__()

    def kill(self):
        self.die = True

    def set_irc_parameters(self, channel, c, e):
        self.channel = channel
        self.c = c
        self.e = e

    def run(self):
        nachat_prompt = "There's an animal loose in #off-topic"
        while not self.die:
            if animal_enabled:
                tm = time.localtime()
                # announce the rooster animal at the top of the hour
                # or top of the minute if fast mode
                if tm.tm_sec == 0 and (animal_fast_mode or tm.tm_min == 0):
                    # regenerate the times for the next hour
                    # or next minute if fast mode
                    animal_generate_times()
                    # usually display the rooster at the top of the hour
                    # or top of the minute in fast mode.
                    # If animal random mode has been selected,
                    # display an animal at random instead,
                    # unless the time is 15:00 or 20:00
                    # or Sunday at 11:00
                    # (these are meeting times)
                    # in which case the rooster is displayed.
                    rooster = True
                    if not animal_rooster_mode:
                        rooster = False
                        if animal_fast_mode:
                            if tm.tm_min in [0, 10, 20, 30, 40, 50]:
                                rooster = True
                        else:
                            if tm.tm_hour in [15, 20] or \
                               (tm.tm_wday == 6 and tm.tm_hour == 11):
                                rooster = True
                    if rooster:
                        result = animal_game_chime()
                    else:
                        result = animal_game()
                    lines = result.split('\n')
                    if self.channel is not None:
                        for text in lines:
                            self.c.privmsg(self.channel, text)
                    time.sleep(1)
                elif tm.tm_sec in seconds_list and \
                     tm.tm_min in minutes_list:
                    result = animal_game()
                    lines = result.split('\n')
                    if self.channel is not None:
                        for text in lines:
                            self.c.privmsg(self.channel, text)
                    time.sleep(1)
                if self.animal_dump_counter == 0:
                    # save the database often
                    animal_dump()
                    self.animal_dump_counter = 120
                self.animal_dump_counter -= 1
                time.sleep(0.5)

import irc.bot
class AnimalBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.user_list = {}
        animal_load()
        animal_enable()
        animal_fast()
        self.animalThread = AnimalThread()
        self.animalThread.start()

    def __del__(self):
        self.animal_dump()
        self.animalThread.kill()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        c.privmsg(self.channel, nickname + " started")
        self.animalThread.set_irc_parameters(self.channel, c, e)

    def on_pubmsg(self, c, e):
        nick = e.source.nick
        userhost = e.source.host
        user = nick.lower()
        message = e.arguments[0].lower()
        if debug: print(f"message={message}")
        # ignore everything else not in our channel
        if e.target != self.channel:
            return
        if message.startswith("!"):
            query = ""
            args = message.split(' ')
            command = args[0][1:]
            if len(args) > 1:
                query = ' '.join(args[1:])
            if debug: print(f"command={command}")
            if debug: print(f'query="{query}"')
            if command in animal_commands:
                result = animal_command_handler(user, userhost, command, query)
                if result is not None:
                    if command == 'animals':
                        c.privmsg(self.channel, f"{nick}: see your direct message (PM) from {nickname} for results")
                    lines = result.split('\n')
                    for text in lines:
                        if command == 'ahelp':
                            if query:
                                requester_nick = query
                            else:
                                requester_nick = nick
                            c.privmsg(requester_nick, text)
                            time.sleep(0.5)
                        # the animals command shows a lot of text,
                        # send it by direct message to the user, instead
                        elif command == 'animals':
                            c.privmsg(nick, text)
                            time.sleep(0.5)
                        else:
                            c.privmsg(self.channel, text)

    def on_privmsg(self, c, e):
        nick = e.source.nick
        c.privmsg(nick, "I am the animal bot")


def main():
    bot = AnimalBot(channel, nickname, server, port)
    bot.start()

def test_main():
    import sys
    user = 'test'
    while True:
        text = animal_game()
        print(text)
        line = input("? ")
        if not line:
            sys.exit()
        text = line.strip()
        if not text:
            sys.exit()
        if re.search("^!", text):
            words = text.split()
            tokens = []
            for word in words:
                w = word.strip()
                if w:
                    tokens.append(w)
            command = tokens[0][1:].lower()
            query = ' '.join(tokens[1:])
            if debug: print(f'command={command}')
            if debug: print(f'query={query}')
            text = animal_command_handler(user, None, command, query)
            print(text)

# are we running this script from the command line?
if __name__ == '__main__':
    if test:
        test_main()
    else:
        main()

