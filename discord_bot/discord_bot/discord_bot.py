import discord
from logger import Logger
import roll_handler, ausgabe#, calendar_handler

client = discord.Client()
#Logger.default_log_level = Logger.LOG_LEVEL_WARNING
log = Logger.get_instance(Logger.LOG_LEVEL_WARNING)
entry_sign = '$'


## COMMANDS ##

def change_log_level(message : discord.Message):
    """
    Changes the Log level. Accepts 'fine', 'config', 'warn[ing]' and 'severe' as parameters.
    """
    lvl = message.content.split()[1].lower()
    
    levels = {
        'fine': Logger.LOG_LEVEL_FINE,
        'config': Logger.LOG_LEVEL_CONFIG,
        'warning': Logger.LOG_LEVEL_WARNING,
        'warn': Logger.LOG_LEVEL_WARNING,
        'severe': Logger.LOG_LEVEL_SEVERE
        }

    if lvl not in levels.keys():
        try:
            lvl = int(lvl)
            if 0 <= lvl <= Logger.LOG_LEVEL_SEVERE:
                log.set_log_level(lvl)
        except ValueError:
            pass
    else:
        log.set_log_level(levels[lvl])
        print("Log level set to: ", lvl)


def help(message : discord.Message):
    """
    Note: inactive!
    Outputs the help dialogue for the desired subject.
    """
    subject = message.content.split(" ", 2)

    help_subjects = {
        "roll": ausgabe.printHelp,
        "calendar": None
        }
    try:
        return help_subjects[subject]
    except Exception:
        pass

def roll(message : discord.Message):
    """
    Makes a roll request and returns its result.
    """
    rtn = roll_handler.rollDice(message.content.split(" ",2)[1].strip())
    if rtn[0] != 100:
        log.warning(message.content + "\n" + roll_handler.exitCodes[rtn[0]])

    output_calls = {
       100: ausgabe.printDiceValue,
       110: ausgabe.printFormatError,
       111: ausgabe.printNoDiceError
    }
    rtn = output_calls[rtn[0]](str(message.author),rtn[1])

    return rtn

def who_free(message : discord.Message):
    pass

def when_free(message : discord.Message):
    pass

## SDNAMMOC ##


## EVENTS ##

@client.event
async def on_ready():
    welcome_string = 'Bot active as user {0.user}'.format(client)
    print(welcome_string)
    log.config(welcome_string)
    await client.get_channel(808722679054073909).send(welcome_string)

@client.event
async def on_message(message : discord.Message):
    if message.author == client.user or not message.content.startswith(entry_sign):
        return

    command_map = {
        "$loglevel": change_log_level,
        "$help": help,
        "$roll": roll,
        "$freeon": who_free,
        "$freetimes": when_free
        }
    try:
        msg = command_map[message.content.split()[0].lower()](message)
        if msg != None:
            await message.channel.send(msg)
    except Exception as e:
        await message.channel.send(str(e))

    
## STNEVE ##


def get_token():
  TOKEN = "ODM3MjI5Mjg2MzUxOTYyMTQ5.YIpgiA.X9dv62KxiybBf8KyD_EFjrZlSuY"
#  TOKEN = os.getenv('RNGSUS_TOKEN')
  while TOKEN in ("",None):
    print("RNGSUS_TOKEN was not set in the environment")
    TOKEN = input("Enter your token: ")
  return TOKEN

try:
	client.run(get_token())
except Exception:
	print('Couldn\'t establish connection; is variable RNGSUS_TOKEN valid?')
