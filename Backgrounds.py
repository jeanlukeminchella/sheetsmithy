import Feats
import globalFunctions as gf

def soldier(c,choice):
    Feats.savageAttacker(c)
    boostAbilityScores(c,choice,[0,1,2])
    c.skillProficiencies.extend([3,7])

def farmer(c,choice):
    Feats.tough(c)
    boostAbilityScores(c,choice,[0,2,4])
    c.skillProficiencies.extend([1,10])

def hermit(c,choice):
    Feats.healer(c)
    boostAbilityScores(c,choice,[2,4,5])
    c.skillProficiencies.extend([9,14])

def noble(c,choice):
    Feats.skilled(c)
    boostAbilityScores(c,choice,[0,3,5])
    c.skillProficiencies.extend([5,13])
    
def sage(c,choice):
    Feats.skilled(c)
    boostAbilityScores(c,choice,[2,3,4])
    c.skillProficiencies.extend([2,5])
    
def scribe(c,choice):
    Feats.skilled(c)
    boostAbilityScores(c,choice,[1,3,4])
    c.skillProficiencies.extend([8,11])

def charlatan(c,choice):
    Feats.skilled(c)
    boostAbilityScores(c,choice,[1,2,5])
    c.skillProficiencies.extend([4,15])

def criminal(c,choice):
    Feats.alert(c)
    boostAbilityScores(c,choice,[1,2,3])
    c.skillProficiencies.extend([15,16])

def guard(c,choice):
    Feats.alert(c)
    boostAbilityScores(c,choice,[0,3,4])
    c.skillProficiencies.extend([3,11])
    
def wayfarer(c,choice):
    Feats.lucky(c)
    boostAbilityScores(c,choice,[1,4,5])
    c.skillProficiencies.extend([6,16])
        
def merchant(c,choice):
    Feats.lucky(c)
    boostAbilityScores(c,choice,[2,2,5])
    c.skillProficiencies.extend([13,11])
    

def boostAbilityScores(c,choice,abilitiesToChooseFrom):
    
    boosted = gf.ASIboost(c, 2, abilitiesToChooseFrom)
    # this attribute will have been boosted by two if length is 1, so we cant add any more
    if len(boosted)==1:
        abilitiesToChooseFrom.remove(boosted[0])
    boostedAttribute = gf.ASIboost(c, 1, abilitiesToChooseFrom)[0]
    c.updateModifiers()
    if not boostedAttribute in boosted:
        boosted.append(boostedAttribute)
    buildLogString = gf.getStringFromBoosts(boosted,"background as a "+c.backgroundAsString)
    c.buildLog.append(buildLogString)
    
   
backgrounds = {
    "Charlatan":charlatan,
    "Farmer":farmer,
    "Sage":sage,
    "Noble":noble,
    "Criminal":criminal,
    "Hermit":hermit,
    "Merchant":merchant,
    "Soldier":soldier,
    "Scribe":scribe,
    "Wayfarer":wayfarer,
    "Guard":guard
}

    
