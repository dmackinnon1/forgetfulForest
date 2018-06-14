#
# Script to generate puzzles based on Raymond Smullyan's 
# 'Alice in the Forest of Forgetfulness' puzzles from 
# 'What is the Name of this Book?'
#

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

def validPuzzle(lionStatement, unicornStatement):
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
    puzzle['explanation'] = explanation1("Lion",lionStatement['days'], lionLying, lionPositive, lionNegative, lionDays)
    puzzle['explanation'] = puzzle['explanation'] + " "
    puzzle['explanation'] = puzzle['explanation'] + explanation1("Unicorn",unicornStatement['days'], unicornLying, unicornPositive, unicornNegative, unicornDays)
    puzzle['explanation'] = puzzle['explanation'] + " Based on what both are saying, the only day it could be is " + validDays[0] +"."
    return puzzle

def prettyList(list, conj):
    isFirst = True;
    result = ""
    count = 1
    size = len(list)
    for s in list:
        if not isFirst and size > 2:
            result += ", "
        isFirst  = False
        if count == size and size > 1:
            if (size == 2):
                result += " "
            result += conj + " "
        count = count +1
        result += s
    return result

def explanation1(actor, statement, lieDays, daysIfTrue, daysIfFalse, unionDays):    
    exp1 = actor +" says today"
    if len(statement) == 1:
        exp1 += " is " + statement[0]
    else:
        exp1 += " could be " + prettyList(statement, "or")      
    exp1 += ". We know that " + actor + " lies on " + prettyList(lieDays, "and")
    exp1 += ". So if "+ actor + " is telling the truth it can"
    if (len(daysIfTrue) == 0):
        exp1 += " not be any day (so they must be lying)"
    elif (len(daysIfTrue) == 1):
        exp1 += " only be " + daysIfTrue[0]    
    else:
        exp1 += " be " + prettyList(daysIfTrue, "or")
    exp1 += ", and if "+ actor + " is lying, it can"
    if (len(daysIfFalse) == 0):
        exp1 += " not be any day (so they must be telling the truth)"
    elif (len(daysIfFalse) == 1):
        exp1 += " only be " + daysIfFalse[0]    
    else:
        exp1 += " be " + prettyList(daysIfFalse, "or")
    exp1 += ". All told, from what " + actor + " says, it could"
    if (len(unionDays) == 1):
        exp1 += " only be " + unionDays[0]    
    else:
        exp1 += " be " + prettyList(unionDays, "or")
    exp1 += "."
    return exp1
     

def jsonForPuzzle(puzzle):
    json = '{"lion": "' + puzzle['lion'] +'",' + "\n"
    json += '"unicorn": "' + puzzle['unicorn'] +'",' + "\n"
    json += '"solution": "' + puzzle['solution'] +'",' + "\n"
    json += '"explanation": "' + puzzle['explanation'] +'",' + "\n"
    json += '"id": "' + str(puzzle['id']) +'"}'
    return json

counter = 0
validPuzzles = []
for s1 in allAnnotated:
    for s2 in allAnnotated:
        puzzle = validPuzzle(s1,s2)        
        if(len(puzzle) > 0):
            counter = counter + 1
            puzzle['id'] = counter
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
