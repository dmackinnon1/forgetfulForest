
#
# Script to generate puzzles based on Raymond Smullyan's 'Alice in the Forest of Forgetfulness' 
#
#########################

# first we define the days of the week
daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# if we say one of several days was yesterday, return the possible days for 'today'
def fromYesterdays(yesterdays):
    return [daysOfWeek[(daysOfWeek.index(day) + 1) % (len(daysOfWeek))] for day in yesterdays]

# if we say one of several days will be tomorrow, return the possible days for 'today'
def fromTomorrows(tomorrows):
    return [daysOfWeek[(daysOfWeek.index(day) - 1) % (len(daysOfWeek))] for day in tomorrows]

# The Lion and the Unicorn lie on certain days
lionLying =['Monday', 'Tuesday', 'Wednesday']
unicornLying = ['Thursday', 'Friday','Saturday'] 

# given a list of days, what are the other days of the week?
def otherDays(days):
    return [day for day in daysOfWeek if day not in days]

# we can find when the Lion and Unicorn are truthful
lionTruthful = otherDays(lionLying)
unicornTruthful = otherDays(unicornLying)

# return the days of the week that are common to both lists
def intersect(a, b):
    return [item for item in a if item in b]
    
# return the days of the week that appear in either list
def union(a, b):
    return list(a) + [item for item in b if item not in a]

# create sets of statements that the creatures can make
def annotatedVariations(base):
    today = {'description': base['actor'] + ' told ' + base['state'] + ' today', 'days': base['days']}
    tomorrow = {'description': base['actor'] + ' will tell ' + base['state'] + ' tomorrow', 'days': fromTomorrows(base['days'])}
    yesterday = {'description': base['actor'] +' told ' + base['state'] + ' yesterday', 'days': fromYesterdays(base['days'])}
    return [today, tomorrow, yesterday]

def individualDays():
    return [{'description': 'Today is ' + d, 'days':[d]} for d in daysOfWeek]

def weekAndWeekend():
    weekend = ['Saturday', 'Sunday']
    return [{'description': 'Today is a weekday', 'days': otherDays(weekend)},
            {'description': 'It is the weekend', 'days': weekend}]

allAnnotated = [];
allAnnotated.extend(annotatedVariations({'actor': 'Lion', 'state': 'lies', 'days': lionLying}))
allAnnotated.extend(annotatedVariations({'actor': 'Lion', 'state': 'truths', 'days': lionTruthful}))
allAnnotated.extend(annotatedVariations({'actor': 'Unicorn', 'state': 'lies', 'days': unicornLying}))
allAnnotated.extend(annotatedVariations({'actor': 'Unicorn', 'state': 'truths', 'days': unicornTruthful}))
allAnnotated.extend(individualDays())
allAnnotated.extend(weekAndWeekend())

def validPuzzle(lionStatement, unicornStatement, counter):
    puzzle = {};
    lionPositive = intersect(lionStatement['days'], lionTruthful)
    lionNegative = intersect(otherDays(lionStatement['days']), lionLying)
    lionDays = union(lionPositive, lionNegative)
    unicornPositive = intersect(unicornStatement['days'], unicornTruthful)
    unicornNegative = intersect(otherDays(unicornStatement['days']),unicornLying)
    unicornDays = union(unicornPositive, unicornNegative)
    validDays = intersect(lionDays, unicornDays)
    if (len(validDays) != 1):
        return  puzzle
    if ('Lion' in lionStatement['description']):
        puzzle['lion'] = ("The Lion says: " + lionStatement['description'].replace("Lion", "I") + '.')
    else:
        puzzle['lion'] = ("The Lion says: " + lionStatement['description'] + '.')
    if ('Unicorn' in unicornStatement['description']):
        puzzle['unicorn'] = ("The Unicorn says: " + unicornStatement['description'].replace("Unicorn", "I") + '.')
    else:
        puzzle['unicorn'] = ("The Unicorn says: " + unicornStatement['description'] + '.')
    puzzle['solution'] = validDays[0]
    puzzle['id'] = counter
    return puzzle

def jsonForPuzzle(puzzle):
	json = '{"lion": "' + puzzle['lion'] +'",' + "\n"
	json += '"unicorn": "' + puzzle['unicorn'] +'",' + "\n"
	json += '"solution": "' + puzzle['solution'] +'",' + "\n"
	json += '"id": "' + str(puzzle['id']) +'"}'
	return json

counter = 0
validPuzzles = []
for s1 in allAnnotated:
	for s2 in allAnnotated:
		counter = counter + 1
		puzzle = validPuzzle(s1,s2,counter)
		if(len(puzzle) > 0):
			validPuzzles.append(jsonForPuzzle(puzzle))
result = "["
first = True
for p in validPuzzles:
	if not first:
		result += ", \n"
	else:
		first = False
	result += p
result += "]"

f = open("../data/forest.json","w")
f.write( result )
f.close()
