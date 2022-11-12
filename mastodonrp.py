from random import randrange
from msvcrt import getch

# Score variables
confusion = 0
damages = 0
thinking = 0

# Game state variables
sitDeath = False
clarity = False
extDice = False

# Ending condition constants
maxScore = 10

dayEvents = {
	1: {'text': 'The mastodon tells you a secret about your family it could not possibly know.',
		'confusion': 1,
		'damages': 0,
		'thinking': 0
	},
	2: {'text': 'Your mastodon decentralizes all over the carpet.',
		'confusion': 0,
		'damages': 1,
		'thinking': 0
	},
	3: {'text': 'You take the mastodon on a walk in your gated neighbourhood.',
		'confusion': 0,
		'damages': 0,
		'thinking': 1
	},
	4: {'text': 'The mastodon federates violently through a window, which now needs replacing.',
		'confusion': 1,
		'damages': 1,
		'thinking': 0
	},
	5: {'text': 'The mastodon won\'t move unless you know the password. You do not know the password.',
		'confusion': 2,
		'damages': 0,
		'thinking': 0
	},
	6: {'text': 'The mastodon bashes a hole in your roof, and now claims to have a much better view of other mastodons.',
		'confusion': 0,
		'damages': 2,
		'thinking': 0
	}
}

eveningEvents = {
	1: {'text': 'The mastodon trumpets ERROR at you. You ponder your mistake.',
		'confusion': 0,
		'damages': 0,
		'thinking': 1
	},
	2: {'text': 'It wears so many hats. How will you wash all those hats?',
		'confusion': 1,
		'damages': 0,
		'thinking': 0
	},
	3: {'text': 'It reads moral philosophy and particle physics. All day. It will not let you read with it.',
		'confusion': 1,
		'damages': 0,
		'thinking': 0
	},
	4: {'text': 'Your friends tell you how wonderful their mastodons are. You burn with envy.',
		'confusion': 1,
		'damages': 0,
		'thinking': 1
	},
	5: {'text': 'Before the mastodon will sleep, you must clean its many whistles and gears.',
		'confusion': 1,
		'damages': 0,
		'thinking': 1
	},
	6: {'text': 'During the night, your mastodon holds not one, not two, but a third party. There is a platform. And servers.',
		'confusion': 0,
		'damages': 1,
		'thinking': 0
	}
}

def rolld6(verbose=True) -> int:
	if extDice:
		print('Roll a d6.')

		while True:
			inp = input('Enter roll: ')
			# Perform input validity check
			if inp.isdigit():
				roll = int(inp)
				if roll >= 1 and roll <=6:
					return roll
			print('Invalid input! Result of roll must be an integer from 1-6.')
	
	roll = randrange(6) + 1
	if verbose:
		wait('Press any key to roll a d6.')
		print(f'You rolled a {roll}.')
	return roll

def endConditions() -> bool:
	return confusion >= maxScore or damages >= maxScore or thinking >= maxScore

def printScores(roundNum, endGame=False, bars=True):
	if not endGame:
		print(f'ROUND {roundNum}')
	if bars:
		print('Confusion: ', end='')
		printBar(confusion)
		
		print('Damages:   ', end='')
		printBar(damages)

		print('Thinking:  ', end='')
		printBar(thinking)
	else:
		print(f'Confusion: {confusion}, Damages: {damages}, Thinking: {thinking}')
	print()

def printBar(num, lim=maxScore):
	print('|', end='')
	[print('=', end='') for _ in range(num)]
	[print('-', end='') for _ in range(lim - num)]
	print('|')

def updateScores(cnfAdd, dmgAdd, thkAdd):
	global confusion, damages, thinking		# Don't cancel me for this
	if cnfAdd > 0:
		confusion += cnfAdd
		print(f'+{cnfAdd} Confusion')
	if dmgAdd > 0:
		damages += dmgAdd
		print(f'+{dmgAdd} Damages')
	if thkAdd > 0:
		thinking += thkAdd
		print(f'+{thkAdd} Thinking')

def wait(text=None):
	if text:
		print(text)
	getch()

roundNum = 0

# Start the game
print('--- I DO NOT WANT A MASTODON ---')
print('Original one-page RPG created by @deathbybadger.')
print('Automated by @jinthespaceguy.')
print()
print('Due to the unwanted (and ill-judged) generosity of a late relative\'s will and testament, you are now the owner of a large, bad tempered proboscidean. No, you did not necessarily want a mastodon, but life gave you one anyway. And now it\'s in your house. Touching all your things.')
print()

# Option to use own dice and manually input roll result
inp = input('Would you like to use your own dice? [Y/n] ')
if inp == 'Y':
	extDice = True

wait('Settings have been entered. Press any key to play.')

# Game loop
while not endConditions():
	print()

	# New round
	roundNum += 1
	printScores(roundNum)

	# Generate Mastodon event
	roll = rolld6()

	print()
	if roll == 6:
		print('You anger your mastodon with your questions, and it sits on you. Roll a d6. On a 6, you never emerge.')
		if rolld6() == 6:
			sitDeath = True
			break
		else:
			wait('You escape. Press any key to continue.')
			continue
	elif roll in [1, 2, 3]:
		print('A DAY WITH YOUR MASTODON...')
		roll = rolld6()
		event = dayEvents[roll]
	else:
		print('AN EVENING AT HOME...')
		roll = rolld6()
		event = eveningEvents[roll]

	# Event consequences
	print(event['text'])
	print()
	updateScores(event['confusion'], event['damages'], event['thinking'])

	# Clarity check
	if event['confusion'] > 0:
		print()
		wait('You gained Confusion. Roll three d6. If they are all the same, you experience a feverish moment of dire clarity. Press any key to continue.')
		rolls = [rolld6(verbose=False) for _ in range(3)]
		print(f'You rolled: {rolls[0]} {rolls[1]} {rolls[2]}')
		if rolls[0] == rolls[1] == rolls[2]:
			clarity = True
			break
		else:
			print('Nothing happened.')

	print()
	wait('Press any key to continue.')

# Endgame
print()
print('--- GAME OVER! ---')
if sitDeath:
	print('You never emerge from under the mastodon.')
elif clarity:
	print('A FEVERISH MOMENT OF DIRE CLARITY')
	print('You finally decipher what the mastodon was trying to tell you. You live the rest of your life in a state of blissful enlightenment, in harmony with your new friend. You\'re also a vegan now.')
else:
	if confusion >= maxScore:
		print('You finally lose your temper with the wretched creature and confront it. The argument is brief, because you have no idea what it is trying to tell you, and eventually it crushes you to death using its trunk.')
	elif damages >= maxScore:
		print('You lose all your money and your livelihood is destroyed, reduced to gigantic footprints in the ashes. The mastodon abandons you in search of someone else to inconvenience.')
	else:
		print('You decide that mastodons are not for you. You slip away into the night with the last of your remaining savings, faking your death. Perhaps you\'ll build a gigantic pillowfort. Or collect tumblers. Something quiet.')

print()
print(f'You survived {roundNum} rounds and achieved these scores:')
printScores(-1, endGame=True, bars=False)