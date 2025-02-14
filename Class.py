
import globalFunctions as gf
import Entry as e
import Armor as armor
import characterCreationChoices as ccc
import featFunctions as feats
import Item as item
import random as rand

equipmentTitle = "INVENTORY"
bonusActionTitle = "BONUS ACTIONS (1 per turn)"
skillsAsStrings = ["Acrobatics",   "Animal Handling",  "Arcana",  "Athletics",  "Deception",  "History",  "Insight",  "Intimidation",  "Investigation",  "Medicine",  "Nature",  "Perception","Performance",  "Persuasion",  "Religion",  "Sleight of Hand",  "Stealth",  "Survival",  "Thieves' Tools"]
savesAsStrings = gf.attributes
skillModifierIndex =[1,4,3,0,4,3,4,5,3,4,3,4,5,5,3,1,1,4,1]
armors = ["Studded Leather","Leather","Splint","Scale Mail","Ring Mail","Plate","Hide","Half Plate","Chain Shirt","Chain Mail","Breastplate"]
languages = ["elven","draconic","gnomish","dwarven","sign","orc","giant","halfling"]



class Sheet:
    
    #inp is of type Input
    def __init__(self, inp):
        

        #cosmetics stuff & variants
        self.showScores = inp.showScores
        self.buildLog = []
        self.showBuildLog = inp.showScores
        self.showShortRest = inp.showShortRest
        self.showLongRest = inp.showLongRest
        self.showPhysicalDamageTypes = False
        
        self.skillProficiencies = []
        self.skillExpertises = []
        
        # these are tuples with [index,modifier/note]
        # we should check for duplicates in the notes if possible here :)
        self.skillBoosts = []
        self.skillNotes = []
        self.saveBoosts = []
        self.saveNotes = []
        # saveProficiencies is not initaliased here, type of sheet has already initalised it
        # freeSkills are proficiencies that can be picked at the end, in ANY skill, may come from race, feat or other
        self.freeSkills = 0
        
        self.level = inp.level
        self.profBonus = gf.getNumberFromRange(self.level,[0,4,8,12,16])
        self.speed = 30
        self.raceString = ""
        self.classAsString = inp.classAsString
        self.choices = inp.choices
        self.subclass = None
        if "subclass" in self.choices.keys():
            self.subclass = self.choices["subclass"]
        self.resistances = ""
        self.name= inp.name
        self.spellcastingMod = self.defaultMod
        
        self.stuff = ""
        
        self.wishlist = []
        self.usersWishlist = []
        if inp.shoppingList != "" and inp.shoppingList!=" ":
            self.usersWishlist = inp.shoppingList.split(", ")
        self.languages = ["common"]
        self.userLanguages = inp.languages
        self.preferredLanguages = []
        self.numberOfLanguages = 3
        
        # class specific booleans
        self.ritualCaster = False
        self.proficientWithShields = False
        self.spellcasting = False
        self.spellsKnown = 0    
        self.notesForSpellCastingBlock = []
        self.spellPriorityList = []
        self.martialProficiency = False
        self.heavyArmorProficiency = False
        self.mediumArmorProficiency = False
        self.lightArmorProficiency = False
        self.showDash = True
        self.showDodge = True
        self.showDisengage = True
        self.showReady = True
        self.showUseObject = True
        self.masteries = 0
        
        # this includes things like defence fighting style, cloaks of protection ect.
        self.cumulativeACBonus = 0
        # these are static AC options without shield / other stacking bonuses. eg. warforged / tortle
        self.baseACOptions = []
        self.equippedArmor = None
        self.wearingShield = "shield" in inp.shoppingList.lower()
        # just because we want to wear a shield though doesnt mean we can afford it and are proficient
        self.addedShield = False
        
        
        self.costDic = {
            "1": "1st-level-spell",
            "2": "2nd-level-spell",
            "3": "3rd-level-spell",
        }
        
        
        # dynamic sections of blocks that build the page, at the very end
        self.leftColumnBlocks = []
        self.middleColumnBlocks = []
        self.rightColumnBlocks = []
        
        # dynamic blocks that are in every class, and customisable attributes for each
        self.charInfos = []
        self.highlightedEntries = []
        self.highlightedBlockIndex = 0
        self.reactions=[]
        self.bonusActionEntries = []
        self.actionEntries = []
        self.shortRestEntries = []
        self.longRestEntries = []
        
        self.darkvision = 0
        self.size = None
        # all backgrounds get 50gp
        self.gp = 50
            
        self.hp = 0
        if self.level>3:
            featChoice = None
            if "l4-feat" in self.choices.keys():
                featChoice = self.choices["l4-feat"]
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                feats.asi(self)
                
        ccc.applyBackground(self, inp.background)
        # this sets self.backgroundAsString
        ccc.applyRace(self, inp.race)
        # hitDie is not initaliased here, type of sheet has to have already initalised it
        self.hp += getHp(self.hitDie,self.level,self.modifiers[2])
         
        self.reactions.append(e.TextEntry("oppAttack"))
        hitDiceString = "Regain "+str(max(1,int(self.level/2)))+" hit di"
        if self.level>3:
            hitDiceString+="ce"
        else:
            hitDiceString+="e"
            
        hitDiceString+=", and all your hp"
        self.longRestEntries.append(e.Entry(hitDiceString))
        
        class HitDiceEntry(e.Entry):
            
            def getHTML(self,char):
                bold = ""
                mid = "<strong>Heal</strong> d"+str(char.hitDie)+gf.getSignedStringFromInt(char.modifiers[2],True)+" hp for each hit die you spend."
                if char.level>1:
                    mid += "<br>"
                for i in range(char.level):
                    mid += " O"
                it = ""
                return e.getHTMLfromThruple([bold,mid,it])
        hitDiceEntry = HitDiceEntry("")
        self.shortRestEntries.append(hitDiceEntry)

        if inp.gearList != "" and inp.gearList!=" ":
            gear = inp.gearList.split(", ")
            for g in gear:
                item.buyItem(self,g,False)

    
    # returns True if added successfully
    # doesnt handle text entries very well - loses it when comparing "cost"
    def addEntry(self,command,highlight=True):
        
        if type(command)==str:
            command = e.getEntryWithSpellCommand(command)
            
        weHaveThisEntryAlready = False

        allEntries = self.actionEntries[:]
        allEntries.extend(self.bonusActionEntries[:])
        allEntries.extend(self.highlightedEntries[:])
        allEntries.extend(self.reactions[:])

        for ent in allEntries:
            if "Entry" in str(type(ent)):

                if ent.title == command.title:
                    weHaveThisEntryAlready = True
            elif type(ent)==dict:
                if not "id" in ent.keys():
                    ent = e.ne.getExpandedDictionary(ent)
                if ent["id"]==command.title:
                    weHaveThisEntryAlready = True
                if "title" in ent.keys():
                    if ent["title"]==command["title"]:
                        weHaveThisEntryAlready = True
        if not weHaveThisEntryAlready:
            if command.castTime=="a":
                if command.cost=="" and highlight:
                    self.highlightedEntries.append(command)
                else:
                    self.actionEntries.append(command)

            elif command.castTime=="ba":
                self.bonusActionEntries.append(command)
            elif command.castTime=="re":
                self.reactionEntries.append(command)
            else:
                print("This cast time confused me: ",command)
                return False
            return True
        else:
            print("We already have ",command.title," in class ",self.classAsString)
            return False            


    def makeSpellcastingBlock(self):
        
        spellcastingTitle = "SPELLCASTING"
        
        if self.spellcasting:
            
            self.longRestEntries.append(e.TextEntry("regainSpellSlots"))
            
            # lets load in the spells - ones we dont have already of course
            l = self.actionEntries[:]
            l.extend(self.reactions)
            l.extend(self.bonusActionEntries)
            
            spellTitlesKnownAlready = []
            
            for action in l:
                if type(action) == e.SpellEntry or type(action)==e.AttackRollEntry or type(action)==e.HealingEntry:
                    spellTitlesKnownAlready.append(action.title)
            
            # for debugging
            pr = False
            if pr:

                print("spellTitlesKnownAlready is ",spellTitlesKnownAlready)
                print("self.spellsKnown is ",self.spellsKnown)
                print("spellPriorityList is ",self.spellPriorityList)

            spellPriorityList = self.spellPriorityList
            spellsAdded = 0
            nextSpellIndexToConsider = 0
            
            while spellsAdded<self.spellsKnown and nextSpellIndexToConsider<len(spellPriorityList):
                
                spell = spellPriorityList[nextSpellIndexToConsider]
                if type(spell)==str:
                    spell = e.getEntryWithSpellCommand(spell)
                    # handle an error here?
                
                
                if not spell.title in spellTitlesKnownAlready:
                    if pr:
                        print("now trying to add ", spell.title," as we dont have it yet")

                    if spell.castTime=="a":
                        self.actionEntries.append(spell)
                    elif spell.castTime=="ba":
                        self.bonusActionEntries.append(spell)
                    elif spell.castTime=="re":
                        self.reactionEntries.append(spell)
                    else:
                        print("This cast time confused me: ",spellPriorityList[nextSpellIndexToConsider].castTime," in spell ",spellPriorityList[nextSpellIndexToConsider].title)
                        # dont incriment spells added 
                        spellsAdded=spellsAdded-1
                    nextSpellIndexToConsider+=1
                    spellsAdded+=1
                else:
                    nextSpellIndexToConsider+=1
            
            
            resourceEntry = e.Entry(gf.getSpellSlotHTMLString(self.spellSlotResourceTuples))
            spellcastingBlockEntries = [resourceEntry]
            spellcastingBlockEntries.extend(self.notesForSpellCastingBlock)
            
            #scan the actions,bonusactions, and reactions for a concentration mark
            
            weNeedToConcentrate = False
            weNeedToExplainRituals= False
            
            l = self.actionEntries[:]
            l.extend(self.reactions)
            l.extend(self.bonusActionEntries)
            
            for action in l:
                if type(action) == e.SpellEntry or type(action)==e.AttackRollEntry:
                    if action.conc:
                        weNeedToConcentrate=True
                    if action.ritual:
                        weNeedToExplainRituals=True
            
            if weNeedToConcentrate:
                spellcastingBlockEntries.append(e.TextEntry("conc"))
            
            if weNeedToExplainRituals and self.ritualCaster:
                spellcastingBlockEntries.append(e.TextEntry("ritual"))
            
            spellBlock = e.Block(spellcastingBlockEntries,spellcastingTitle)
            self.rightColumnBlocks.append(spellBlock)
    
    def addResistance(self,r):
        
        if not r in self.resistances:
            if self.resistances == "":
                self.resistances = r
            else:
                self.resistances += ", "+r
                
    def calculateAC(self):
        
        options = self.baseACOptions
        options.append(10+self.modifiers[1])
        
        armorsThatWeHave = []
        bestArmor = None
        bestArmorAC = max(options)
        bestArmorObject = None
        
        for a in armors:
            if a in self.stuff:
                armorsThatWeHave.append(a)
        
        for a in armorsThatWeHave:
            armorObject = armor.Armor()
            armorObject.loadArmor(a)
            ac = armorObject.base
            if armorObject.addDex:
                if armorObject.maxTwo:
                    ac=ac+min(2,self.modifiers[1])
                else:
                    ac=ac+self.modifiers[1]
            if ac>bestArmorAC:
                bestArmor = a
                bestArmorAC = ac
                bestArmorObject = armorObject
        ac = None
        
        if max(options)<bestArmorAC:
            
            #lets get that armor on its great
            self.equippedArmor = bestArmorObject
            ac = bestArmorAC
            if bestArmorObject.stealthDisadvantage:
                self.skillNotes.append([16,"(disadavantage)"])
            
        else:
            ac = max(options)
        
        if self.wearingShield and self.proficientWithShields and "Shield" in self.stuff:
            ac = ac+2
            print("adding shield")
            self.addedShield = True
        
        self.AC = ac  + self.cumulativeACBonus
        
    def addItemToInventory(self, item):
        if self.stuff == "":
            self.stuff=item
        else:
            self.stuff+=", "+item

    def updateModifiers(self):
        
        scores = self.scores

        if scores==None:
            print("Ive been asked to update modifiers and scores have not been set")
        elif len(scores) != 6:
            print("Theres a problem with the scores when trying to update modifiers: ",scores)
        else:
            self.modifiers = [0]*6
            for i in range(6):
                score = scores[i]
                score = score-10
                if score<0:
                    score = score-1
                self.modifiers[i]=int(score/2)
    
    
    
    def addHighlightedEntry(self,entry):
        if type(entry)==str:
            entry = e.getEntryWithSpellCommand(entry)
            # handle an error here?    
        self.highlightedEntries.append(entry)
            
    # takes an input and gives the class their scores and modifiers, also takes as input the default scores
    def loadScoresAndMods(self,preferredScores,inp):
        
        if inp.scores == None:
            self.scores = preferredScores
        else:
            self.scores = inp.scores
        self.updateModifiers()
    
    # returns None if there are no languages left to pick
    def pickRandomLanguage(self):

        languagesToPickFrom = []
        for l in languages:
            if not l.lower() in self.languages:
                languagesToPickFrom.append(l)
        
        if len(languagesToPickFrom)>0:
            chosenIndex = rand.randint(0,len(languagesToPickFrom)-1)
            return languagesToPickFrom[chosenIndex]
        else:
            return None

    def pickSkillProficiency(self,skillsToChooseFrom=list(range(17))):
        
        #this has to be cloned or changes are carried next time function is called
        skillsToChooseFrom=skillsToChooseFrom[:]
        
        def w(l):
            k=[]
            for i in l:
                k.append(skillsAsStrings[i])
            return k 
        
        #This checks were not already proficient in everything to choose from
        skillsToChooseFromWeHaveAlready = []
        for s in skillsToChooseFrom:
            if s in self.skillProficiencies:
                skillsToChooseFromWeHaveAlready.append(s)
                
        if len(skillsToChooseFromWeHaveAlready)==len(skillsToChooseFrom):
            return None
        
        #lets take out the ones were proficient in already from our choices
        for s in skillsToChooseFromWeHaveAlready:
            skillsToChooseFrom.remove(s)
            
        #lets give each skill a score.
        #["Acrobatics",   "Animal Handling",  "Arcana",  "Athletics",  "Deception",  "History",  "Insight",  "Intimidation",  "Investigation",  "Medicine",  
        skillScores = [7,10,5,10,5,0,18,5,15,3]
        # "Nature",  "Perception","Performance",  "Persuasion",  "Religion",  "Sleight of Hand",  "Stealth",  "Survival",  "Thieves' Tools"]
        skillScores.extend([0,28,11,8,0,4,25,7,6])
        
        # Some skills are going to be more valuable to certain classes
        # for example, medicine isnt useful for classes who can heal
        healingClasses = ["Cleric","Druid","Ranger","Paladin"]
        if self.classAsString in healingClasses:
            skillScores[9]-=50
        ourSkillScores = []
        
        for s in skillsToChooseFrom:
            value = skillScores[s]
            value += int(self.modifiers[skillModifierIndex[s]]*10)
            ourSkillScores.append(value)
        
        return skillsToChooseFrom[ourSkillScores.index(max(ourSkillScores))]
            
    def generateClassHTML(self):
        
        # bit of compiling to do at the start
        
        self.makeSpellcastingBlock()

        if self.showUseObject:
            self.actionEntries.append(e.TextEntry("useObject"))
        
        if self.showReady:
            self.actionEntries.append(e.TextEntry("Ready"))
            
        if self.showDisengage:
            self.actionEntries.append(e.TextEntry("Disengage"))
            
        if self.showDash:
            self.actionEntries.append(e.TextEntry("Dash"))
        if self.showDodge:
            self.actionEntries.append(e.TextEntry("Dodge"))    
            
        self.buildLog.insert(0,self.classAsString)
        if self.showBuildLog:
            for i in self.buildLog:
                print(i)
            print()
        
        for i in range(self.freeSkills):
            p = self.pickSkillProficiency()
            self.skillProficiencies.append(p)
            
        if self.showShortRest:
            shortRestBlock = e.Block(self.shortRestEntries,"ON A SHORT REST")
            self.leftColumnBlocks.append(shortRestBlock)
        
        if self.showLongRest:
            longRestBlock = e.Block(self.longRestEntries,"ON A LONG REST")
            self.leftColumnBlocks.append(longRestBlock)

        

        userLanguages = []
        if self.userLanguages != "" and not self.userLanguages.isspace():
            userLanguages = self.userLanguages.split(", ")

        while len(self.languages)<self.numberOfLanguages:
            
            if len(userLanguages)>0:
                self.languages.append(userLanguages.pop())
            elif len(self.preferredLanguages)>0:
                self.languages.append(self.preferredLanguages.pop())
            else:
                l = self.pickRandomLanguage()
                if l != None:
                    self.languages.append(l)
                else:
                    #weve learned all the languages in the world it seems
                    self.numberOfLanguages = -1

        
        
        

        #lets do the stuff
        
        preferredArmor = None
        if self.lightArmorProficiency:
            if self.mediumArmorProficiency:
                
                if self.modifiers[1]<2:
                    # then our ac would benefit from heavy armor 

                    if self.modifiers[1]>=0 and 16 in self.skillProficiencies:
                        # we have proficiency in stealth and are still not that undexterous so lets stay stealthy
                        preferredArmor = "Chain Shirt"
                    else:

                        if self.heavyArmorProficiency:
                            preferredArmor = "Chain Mail"
                        else:
                            # oh dear, weve got dex<2 and were not proficient in heavy armor            
                            preferredArmor = "Scale Mail"

                else:
                    # weve got DEX>1, so medium armor will be as good as heavy
                    if 16 in self.skillProficiencies or self.modifiers[1]>1:
                        # we have proficiency in stealth or are otherwise fairly dexterous so lets stay stealthy
                        if self.modifiers[1]>3:
                            preferredArmor = "Studded Leather Armor"
                        else:

                            preferredArmor = "Chain Shirt"
                    else:
                        # we dont have proficiency in stealth and are dex is 2
                        preferredArmor = "Chain Mail"
            else:
                #prof in light armor but not medium 
                preferredArmor = "Studded Leather Armor"
        else:
            #not proficient in any armors 
            pass
                        
        if preferredArmor !=None:
            self.wishlist.insert(0,preferredArmor)

        self.wishlist.append("Traveler's Clothes")
        self.wishlist.append("rope")

        for i in self.wishlist:
            item.buyItem(self,i)
        for i in self.usersWishlist:
            item.buyItem(self,i)

        gold = int(self.gp)
        silver = self.gp%1
        if silver >0:
            silver = silver * 10
            silver+=0.0001
        copper = silver%1
        copper=copper*10
        copper=int(copper)

        if gold>0:   
            self.addItemToInventory(str(gold)+"gp")
        if silver>0:   
            self.addItemToInventory(str(int(silver))+"sp")
        if copper >0:
            self.addItemToInventory(str(int(copper))+"cp")
        
        if self.stuff!="":
            stuffEntry = e.Entry(self.stuff)
            stuffBlock = e.Block([stuffEntry],equipmentTitle)
            self.rightColumnBlocks.append(stuffBlock)
        self.calculateAC()
        
        # generate the bit before the highlighted Block, the bits after it, and add it to middle col at the index in class parameter
        # this is for things like extra attack, reckless attack ect which should be listed before weapon
        blockBeforeHighlightedActions = e.Block([])
        for i in range(self.highlightedBlockIndex):
            blockBeforeHighlightedActions.addEntry(self.actionEntries[i])
        self.middleColumnBlocks.insert(0,blockBeforeHighlightedActions)
        
        highLightedBlock = e.Block(self.highlightedEntries, "","attack01")
        self.middleColumnBlocks.insert(1,highLightedBlock)
        
        blockAfterHighlightedStuff = e.Block([])
        for i in range(self.highlightedBlockIndex,len(self.actionEntries)):
            blockAfterHighlightedStuff.addEntry(self.actionEntries[i])
        self.middleColumnBlocks.insert(2,blockAfterHighlightedStuff)
        
        #generateReactionBlock, add it to the (end of the) chosen column, as per parameter at start
        reactionBlock = e.Block(self.reactions,"REACTIONS (1 per round)")
        self.leftColumnBlocks.append(reactionBlock)
        
        #generate charinfos Block, and put it at the top of right column
        if len(self.charInfos)>0:
            
            charInfoBlock = e.Block(self.charInfos,"ABILITIES")
            self.rightColumnBlocks.insert(0,charInfoBlock)
        
        # generateBonusActionBlock
        if len(self.bonusActionEntries)>0:
            
            bonusActionBlock = e.Block(self.bonusActionEntries,bonusActionTitle)
            self.rightColumnBlocks.append(bonusActionBlock)

        result=""
        result += "<!DOCTYPE html>\n"
        result += "<html>\n"
        result += "<head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>\n"
        result += "<title>"+self.classAsString+"</title>\n"
        result += writeStyle()
        result += self.generateHeaderHTML()
        result += self.generatemodifierHTML()
        result += "<div id='leftCol'>"
        result += self.generateSaveHTML()
        result += self.generateSkillHTML()
        result +="</div>"
        
        result +="<div id='reactions'>"
        for block in self.leftColumnBlocks:
            result += block.getHTML(self)
        result +="</div>"
        
        result+= "<div id='upperCentralColumn'>\n"
        result+= "<div class='armor keyValueLabel'>AC</div><div class='armor keyValue'>"+str(self.AC)+"</div>\n"
        result+= "<div class='speed keyValueLabel'>SPEED</div><div class='speed keyValue'>"+gf.getDistanceString(self.speed)+"</div>\n"
        result+= "<div class='hitpoints keyValueLabel'>HP</div>\n"
        result+= "<div class='hitpoints keyValue'>"+str(self.hp)+"</div>\n"
        result+= "</div>\n"

        result +="<div id='actions'>\n"
        result +="<div id='sectionTitle' class='header'>ACTIONS (1 per turn)</div>\n"
        
        for block in self.middleColumnBlocks:
            result += block.getHTML(self)
        result +="</div >\n"
        result +="<div id='rightCol'>\n"
        
        for block in self.rightColumnBlocks:
            result += block.getHTML(self)
        
        result +="</div>\n"
        result +="</div>\n"
        result +="</div>\n"
        result +="</body>\n"
        result +="</html>\n"

        return result

    def generateSkillHTML(self):
    
        mods = self.modifiers[:]
        profs = self.skillProficiencies
        p = self.profBonus
        result = "<div id='sectionTitle' class='header'>SKILL CHECKS</div>\n"
        
        result += "<div id='skills'>\n"
        
        skillMods = []

        if 18 in profs:
            skillMods = [0]*len(skillsAsStrings)
        else:
            skillMods = [0]*(len(skillsAsStrings)-1)
        
        for i in range(len(skillMods)):
            skillMods[i] = mods[skillModifierIndex[i]]
        
        for prof in profs:
            if prof in range(19):
                skillMods[prof]+=p
        for expertise in self.skillExpertises:
            skillMods[expertise]+=p
        for skillBoost in self.skillBoosts:
            skillMods[skillBoost[0]]+=skillBoost[1]
            
        lines = []
        
        
        for i in range(len(skillMods)):
            line = skillsAsStrings[i]+" "
            line+=gf.getSignedStringFromInt(skillMods[i],True)
            if i in profs:
                line+=" *"
            if i in self.skillExpertises:
                line+="*"
            lines.append(line)
        
        for note in self.skillNotes:
            lines[note[0]]=lines[note[0]]+" <em>"+note[1]+"</em>"
                
        for i in range(len(lines)):
            lines[i]=lines[i]+" <br>\n"
        
        for line in lines:
            result+=line
        
        result+="\n<p id='prof'>* <em>proficient</em><br>\n"
        if len(self.skillExpertises)>0:
            result+="** <em>expert</em><br></p>\n"
        result+="</div>\n\n"
        
        
        return(result)
        
    def generateSaveHTML(self):
    
        result = "<div id='sectionTitle' class='header'>SAVING&nbsp;THROWS</div>\n"
        
        mods = self.modifiers[:]
        profs = self.saveProficiencies
        p = self.profBonus
        
        result += "<div id='savingthrows'>\n"
        
        saveMods = [0]*len(savesAsStrings)
        
        
        for i in range(len(saveMods)):
            saveMods[i] = mods[i]
        
        for prof in profs:
            saveMods[prof]+=p
            
        for saveBoost in self.saveBoosts:
            saveMods[saveBoost[0]]+=saveBoost[1]
            
        lines = []
        
        for i in range(len(saveMods)):
            line = savesAsStrings[i]+" "
            line+=gf.getSignedStringFromInt(saveMods[i],True)
            if i in profs:
                line+=" *"
            lines.append(line)
        
        for note in self.saveNotes:
            lines[note[0]]=lines[note[0]]+" <em>"+note[1]+"</em>"
                
        for i in range(len(lines)):
            lines[i]=lines[i]+" <br>\n"
        
        for line in lines:
            result+=line
        
        
        result+="</div>\n\n"
        
        
        return(result)
    
    def generatemodifierHTML(self):
        modifiers = self.modifiers
        
        strScoreString = " <br>"
        dexScoreString = " <br>"
        conScoreString = " <br>"
        intScoreString = " <br>"
        wisScoreString = " <br>"
        chaScoreString = " <br>"
        
        if self.showScores:
            strScoreString = "<div id='STRscore' class='abilityscore'>"+str(self.scores[0])+"</div>"
            dexScoreString = "<div id='DEXscore' class='abilityscore'>"+str(self.scores[1])+"</div>"
            conScoreString = "<div id='CONscore' class='abilityscore'>"+str(self.scores[2])+"</div>"
            intScoreString = "<div id='INTscore' class='abilityscore'>"+str(self.scores[3])+"</div>"
            wisScoreString = "<div id='WISscore' class='abilityscore'>"+str(self.scores[4])+"</div>"
            chaScoreString = "<div id='CHAscore' class='abilityscore'>"+str(self.scores[5])+"</div>"
        
        result = "\n"
        result+= "<div id='mods'>"
        result+= "<div id='labelSTR' class='abilityLabel'>STR</div><div id='STRmodf' class='abilityMod'>"+gf.getSignedStringFromInt(modifiers[0])+"</div>"+strScoreString+"<br>\n"
        result+= "<div id='labelDEX' class='abilityLabel'>DEX</div><div id='DEXmodf' class='abilityMod'>"+gf.getSignedStringFromInt(modifiers[1])+"</div>"+dexScoreString+"<br>\n"
        result+= "<div id='labelCON' class='abilityLabel'>CON</div><div id='CONmodf' class='abilityMod'>"+gf.getSignedStringFromInt(modifiers[2])+"</div>"+conScoreString+"<br>\n"
        result+= "<div id='labelINT' class='abilityLabel'>INT</div><div id='INTmodf' class='abilityMod'>"+gf.getSignedStringFromInt(modifiers[3])+"</div>"+intScoreString+"<br>\n"
        result+= "<div id='labelWIS' class='abilityLabel'>WIS</div><div id='WISmodf' class='abilityMod'>"+gf.getSignedStringFromInt(modifiers[4])+"</div>"+wisScoreString+"<br>\n"
        result+= "<div id='labelCHA' class='abilityLabel'>CHA</div><div id='CHAmodf' class='abilityMod'>"+gf.getSignedStringFromInt(modifiers[5])+"</div>"+chaScoreString+"<br>\n\n"
        result+= "</div>"
        return result
    
    def generateHeaderHTML(self):
    
        result = ""
        result+= "<body><div class='wrp'><div id='charsheet01'>\n\n"
        result+= "<div id='charactername'>"+self.name+"</div>\n"
        result+= "\n"
        result+= "<div id='topBanner'>\n"
        result+= "\n"
        result+= "<div class='topBanner middleBanner bannerLabel' id='classlabel'>CLASS</div>\n"
        result+= "<div class='topBanner middleBanner bannerValue' id='class'>"+self.classAsString+"</div>\n"

        result+= "<div class='topBanner leftBanner bannerLabel' id='labelrace'>RACE</div>\n"
        result+= "<div class='topBanner leftBanner bannerValue' id='race'>"+self.raceString+"</div>\n"
        
        if self.darkvision>0:
            result+= "<div class='topBanner rightBanner bannerLabel' id='labelbackground'>BACKGROUND</div>\n"
            result+= "<div class='topBanner rightBanner bannerValue' id='background'>"+self.backgroundAsString+"</div>\n"
            
            result+= "<div class='topBanner farRightBanner bannerLabel' id='labeldarkvision'>DARKVISION</div>\n"
            result+= "<div class='topBanner farRightBanner bannerValue' id='darkvision'>"+gf.getDistanceString(self.darkvision)+"</div>\n"
        

            
        else:

            result+= "<div class='topBanner wholeRightBanner bannerLabel' id='labelbackground'>BACKGROUND</div>\n"
            result+= "<div class='topBanner wholeRightBanner bannerValue' id='background'>"+self.backgroundAsString+"</div>\n"
        if len(self.languages)>0:
            print(self.languages)
            languagesString = self.languages[0].title()
            for i in range(1,len(self.languages)):
                languagesString+=", "+self.languages[i].title()
            if len(languagesString)>37:
                languagesString = languagesString.replace(",","")
                if len(languagesString)>34:
                    l = languagesString.split(" ")
                    if "Orc" not in languagesString:
                        languagesString = languagesString.replace(l[-1],"Orc")
            result+= "<div class='bottomBanner leftBanner bannerLabel' id='labelLanguage'>LANGUAGES</div>\n"
            result+= "<div class='bottomBanner leftBanner bannerValue' id='language'>"+languagesString+"</div>\n"
            

        if self.resistances!="":
            
            if self.size != None:
                result+= "<div class='bottomBanner rightBanner bannerValue' id='size'>"+str(self.size)+"</div>\n"
                result+= "<div id='sizeLabel' class='bottomBanner rightBanner bannerLabel' >SIZE</div>\n"
            result+= "<div class='bottomBanner farRightBanner bannerValue' id='topRightText'>"+self.resistances+"</div>\n"
            result+= "<div class='bottomBanner farRightBanner bannerLabel' id='topRightLabel'>"+"RESISTANCES"+"</div>\n"
        else:
            if self.size != None:
                result+= "<div class='bottomBanner wholeRightBanner bannerValue' id='size'>"+str(self.size)+"</div>\n"
                result+= "<div id='sizeLabel' class='bottomBanner wholeRightBanner bannerLabel' >SIZE</div>\n"
        
        #result+= "<div id='bottomRightLabel'>"+""+"</div>\n"
        #result+= "<div id='bottomRightText'>"+""+"</div>\n"
        # top banner is done
        result+= "</div>\n"
        result+= "\n"
    
        
        return result

def getHp(hitDie,level, conMod):
    hp = hitDie+conMod
    hpPerLevel = int((hitDie/2)+1)+conMod
    hp+=hpPerLevel*(level-1)
    return hp

def writeStyle():
    f = open(gf.pathToSource+"styleText.html", "r")
    return f.read()

