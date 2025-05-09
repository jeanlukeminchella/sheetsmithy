import os 

pathToSource = "/home/sheetsmithy/mysite/"
if "cabinhammer" in os.getcwd():
    pathToSource = "./"


attributes =  ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"]

def getStringFromBoosts(boostList,originOfBoost):
   
    buildLogString = ""
    buildLogString+="From your "+originOfBoost+" you received bonuses to "
    for a in boostList:
        buildLogString+=attributes[a]+" "
    return buildLogString
    

# boosts some ability scores, returns a list of attributes boosted.
# boosts of more than two just get set to two
def ASIboost(c, amountToBoost, attributesToChooseFrom=list(range(6)),canSplitBoosts=True):
    
    amountToBoost = validateInt(amountToBoost,2,0,2)
    
    boostedAttributes = []
    priorityList = c.attributePriorityList[:]
    priorityList = [x for x in priorityList if x in attributesToChooseFrom ]
    
    allocated = 0
    
    if amountToBoost==2:
        # if our top priority attribute is even, or we cant split boosts lets just increase that by two
        if (c.scores[priorityList[0]]%2==0 or not canSplitBoosts):
            
            c.scores[priorityList[0]]+=2
            allocated+=2
            boostedAttributes.append(priorityList[0])
                
        else:
            c.scores[priorityList[0]]+=1
            allocated+=1
            boostedAttributes.append(priorityList[0])
            
    if allocated<amountToBoost:
        
        highestOddPriority = None
        highestOddPriorityIndex = None
        foundOne = False
        i = 0
        
        # lets go through each attribute in terms of priority and record the first one thats odd
        for a in priorityList:
            
            if not foundOne and c.scores[a]%2!=0 :
                foundOne = True
                highestOddPriority = a
                highestOddPriorityIndex = i
            i = i+1
            
        # if none of them are odd, lets add the +1 to our top priority
        # or if weve got an odd score in an attribute that is only a fourth priority, lets forget about it and boost main stat instead
        if highestOddPriority == None or highestOddPriorityIndex > 2:
            c.scores[priorityList[0]]+=1
            allocated+=1
            if priorityList[0] not in boostedAttributes:
                boostedAttributes.append(priorityList[0])
            
        else:
            c.scores[priorityList[highestOddPriorityIndex]]+=1
            allocated+=1
            if priorityList[highestOddPriorityIndex] not in boostedAttributes:
                
                boostedAttributes.append(priorityList[highestOddPriorityIndex])
                
    return boostedAttributes

def getNumberFromRange(level,indents,start=1):
    results = [start]*20
    
    for indent in indents:
        for i in range(indent,20):
            results[i]=results[i]+1

    return results[level-1]
    
def getSignedStringFromInt(i,ignoreZeros=False):
    if i == 0 and ignoreZeros:
        return ""
    
    if i > -1:
        return("+"+str(i))
    else:
        return(str(i))

def getDistanceString(distance,style=1):
    if distance>0:
        if style==1:
            return str(distance)+"ft"
        elif style==2:
            return str(int(distance/5))+" sqs."
    else:
        return ""


def getDefaultGrappleTexts(meleeVerb="Punch"):
    return ["• You must have a free hand for grappling.","• Target attacks other foe with disadvantage","• You move at half speed, and the grappled creature moves with you.","• The grappled creature's speed becomes 0","• You may release the target at any time."]

# listOfResourcesAndCounts is list of tuples, ordered
def getSpellSlotHTMLString(listOfResourcesAndCounts):
    s = "\n"
    for resourceAndCountTuple in listOfResourcesAndCounts:
        resourceLabel =  resourceAndCountTuple[0]
        resourceCount = resourceAndCountTuple[1]
        s+="<strong>"+resourceLabel+"s </strong>- "
        for i in range(resourceCount):
            s+="O "
        s+="<br>\n"
    #s+="<br>\n"
    return s

def validateInt(i, defaultValue, minimum=None,maximum=None):
    try:
        a = int(i)
        if minimum!=None:
            if a<minimum:
                a = defaultValue
        if maximum!=None:
            if a>maximum:
                a = defaultValue
        return a
    except:
        a = defaultValue

def validateString(s, defaultValue=""):
    
    result = ""
    if type(s)==str:
        result = s
    else:
        try:
            result = str(s)
            
        except:
            result = defaultValue
            
    return result


def validateIntList(l, defaultValue, length=None, minimum=None,maximum=None):

    result = []
    for i in l:
        result.append(validateInt(i,defaultValue,minimum,maximum))
    
    if length==None:
        return result
    elif len(result)==length:
        return result
    else:
        return [defaultValue]*length
    


 
