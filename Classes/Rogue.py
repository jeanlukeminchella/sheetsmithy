import Class as c
import Feats as feats


class Rogue(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [1,3]
        self.defaultMod = 1

        self.preferredBackgrounds = ["Charlatan","Criminal","Scribe","Soldier","Wayfarer"]

        arcane = False
        self.attributePriorityList = [1,2,4,5,3,0]
        try:
            if "subclass" in inp["choices"].keys():
                if "arcane" == inp["choices"]["subclass"]:
                    self.attributePriorityList = [1,2,3,4,5,0]
                    arcane = True
                    self.preferredBackgrounds = ["Criminal","Scribe"]
        except:
            pass
        
        if arcane:
            self.loadScoresAndMods([8,15,14,13,12,10],inp)
        else:

            self.loadScoresAndMods([8,15,14,10,13,12],inp)

        
        
        super().__init__(inp)
        self.gp+=100
        
        self.lightArmorProficiency = True
        self.masteries+=2
        level = self.level
        
        self.buyItem("Shortbow")
        self.wishlist.append("Shortsword")
        self.wishlist.append("offhand shortsword")
        self.wishlist.append("thieves' tools")
        
        # thieves tools
        if not 18 in self.skillProficiencies:
            self.skillProficiencies.append(18)

        evasiveMoveEntry = "Take an <strong>"+"Evasive Action."+"</strong> <em>See Evasive Action Options.</em>"
        evasiveMoveTitle="EVASIVE ACTION OPTIONS"
        evasiveMoves = []
        
        if self.level ==1:
            
            self.actions.append({"id":"Hide"})
        
        
        sneakAttackString = "Once per turn when you hit a target, you may add "
        sneakAttackString += "<strong>"+getSneakAttackString(self.level)+"</strong>"
        sneakAttackString += " to the damage if you have advantage on the attack roll or the target is distracted (has a hostile within 5ft)."
        
        sneakAttackEntries = [sneakAttackString]

        if level>1:
            
            self.showDisengage = False
            self.showDash = False

            
            self.bonusActionEntries.append(evasiveMoveEntry)
            

            
            evasiveMoves.append({"id":"Dash"})
            evasiveMoves.append({"id":"Disengage"})
            evasiveMoves.append({"id":"Hide"})
            
        if level>2:
            
            self.bonusActionEntries.append({"id":"steadyAim"})

            subclasses = ["assassin","thief","soul"]
            
            if self.subclass== "" or self.subclass==None:
                self.subclass = subclasses[(self.seed%19)%len(subclasses)]

            
            if self.subclass == "assassin":
                
                self.classAsString ="Rogue (Assassin)"
                self.charInfos.append("On the first round of combat, you have adv. vs enemies that have not yet taken a turn, and your sneak attack deals +"+str(self.level)+" damage")
                self.buyItem("Disguise Kit",False)
                self.buyItem("Poisoner's Kit",False)
            
            # legacy subclass from XGE, initiative needs fixing to be used again
            elif self.subclass == "swash":

                self.classAsString ="Rogue (Swashbuckler)"
                if self.modifiers[5]>0:
                    self.charInfos.append("Your intiative rolls are "+c.gf.getSignedStringFromInt(self.modifiers[1]+self.modifiers[5])+" <em>(Swashbuckler)</em>")
                sneakAttackString = "Once per turn when you hit a target, you may add "
                sneakAttackString += "<strong>"+getSneakAttackString(level)+"</strong>"
                sneakAttackString += "  to the damage if you have advantage on the attack roll, the target is distracted (has a hostile within 5ft), or you are in a duel <em>(Swashbuckler)</em>."
                self.charInfos.append("Targets of your Shortsword cannot make Opportunity Attacks on you for one turn. <em>(Swashbuckler)</em>")
            
            elif self.subclass == "soul":
                self.classAsString ="Rogue (Soul Knife)"
                soulKnifeTitle = "PSIONIC POWER"
                soulKnifeEntries = []
                if self.level>4:
                    soulKnifeEntries.append("<strong>Energy Dice</strong> - O O O O O O - (d8) ")
                else:
                    soulKnifeEntries.append("<strong>Energy Dice</strong> - O O O O - (d6)")
                self.shortRestEntries.append("Regain one <strong>Energy Die</strong>")
                self.longRestEntries.append("Regain all of your <strong>Energy Dice</strong> and your free casting of <strong>Psychic Whispers</strong>")
                soulKnifeEntries.append("If you fail an ability check using a skill or tool with which you have proficiency, you can roll one Psionic Energy Die and add the number rolled to the check, potentially turning failure into success. The die is expended only if the roll then succeeds.")
                self.actions.append(["Psychic Whispers (Psionic).","Choose up to "+str(self.profBonus)+" and then roll one Psionic Energy Die. For a number of hours equal to the number rolled, the chosen creatures can speak telepathically with you, and you can speak telepathically with them. To send or receive a message, you and the other creature must be within 1 mile of each other. A creature can end the telepathic connection at any time.","One free casting per Long Rest - </em>O<em>"])
                
                self.highlightedEntries.append({"id":"Psychic Blade"})
                self.bonusActionEntries.append(["Psychic Blade (60ft).","Make a Psychic Blade attack.","You must have already attacked with Psychic Blades this turn."])
                
                self.rightColumnBlocks.append(c.e.Block(soulKnifeEntries,soulKnifeTitle))

                                              

            elif self.subclass == "arcane":

                self.classAsString ="Rogue (Arcane Trickster)"
                resourceDictionary = {
                3:[["Spell",2]],
                4:[["Spell",3]],
                5:[["Spell",3]],
                6:[["Spell",3]],
                }
                self.costDic["1"]="Spell"
                self.spellSlotResourceTuples=resourceDictionary[self.level]
                self.spellsKnown = 3
                if self.level>5:
                    self.spellsKnown=4
                self.spellcasting = True
                self.spellcastingMod = 3
                self.spellPriorityList = ["Disguise Self","Sleep","Feather Fall","Fog Cloud"]
                addedMindSliver = self.addEntry("Message",False)
                evasiveMoves.append({"id":"Mage Hand","note":"Hand is invisible."})
                addedMinorIllusion = self.addEntry("Create Minor Illusion",False)
                self.wishlist.append("Wand")
                if not (addedMindSliver and addedMinorIllusion):
                    self.addEntry("Mind Sliver")
                

            else:
                self.classAsString ="Rogue (Thief)"
                self.charInfos.append("Climbing costs you no extra movement <em>(Thief)</em>")
                self.showUseObject=False
                evasiveMoves.append({"id":"useObject"})
                evasiveMoves.append({"id":"sleightOfHandThief"})
                self.subclass = "thief"

                
        if level>4:
            
            self.reactions.append({"id":"uncannyDodge"})
            dc = str(8+self.profBonus+self.modifiers[1])
            sneakAttackEntries.append(["","Alternatively, deal <strong>2d6</strong> extra damage and move up to half your speed without provoking Opportunity Attacks."])
            sneakAttackEntries.append(["","Alternatively, deal <strong>2d6</strong> extra damage and trip the target Prone. DEX"+dc+" to resist.","Target must be Large or smaller."])
            sneakAttackEntries.append(["","Alternatively, deal <strong>2d6</strong> extra damage and inflict the Poisoned condition on target for 1 min. CON"+dc+" to resist.","Target repeats saves at the end of their turns. Requires a Poisoner's Kit to use."])
            if self.subclass != "assassin":
                self.wishlist.append("Poisoner's Kit")

        #  Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion, Sleight of Hand, and Stealth.
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
    
        expertisePriority = [15,11,0,16,18]
        
        numberOfExpertisesToChoose = 2
        if level>5:
            numberOfExpertisesToChoose = 4
        
        numberChosen = 0
        
        for expertisePreference in expertisePriority:
            if numberChosen <  numberOfExpertisesToChoose and expertisePreference in self.skillProficiencies and not expertisePreference in self.skillExpertises:
                self.skillExpertises.append(expertisePreference)
                numberChosen+=1
        # if our preferences list wasnt long enough lets go through character skills and see if we can add any of them
        if numberChosen < numberOfExpertisesToChoose:
            for p in self.skillProficiencies:
                if not p in self.skillExpertises and numberChosen < numberOfExpertisesToChoose:
                    self.skillExpertises.append(p)
                    numberChosen+=1
        
        
        sneakBlock = c.e.Block(sneakAttackEntries,"SNEAK ATTACK")
        self.rightColumnBlocks.append(sneakBlock)
        
        if len(evasiveMoves)>0:
            self.actions.append(evasiveMoveEntry)
            evasiveBlock=c.e.Block(evasiveMoves,evasiveMoveTitle)
            actionHeavyRaces = ["Drow","Tiefling (Infernal)","Wood Elf","Tiefling (Abyssal)","Tiefling (Chthonic)"]
            if self.raceString in actionHeavyRaces:
                self.rightColumnBlocks.append(evasiveBlock)
            else:
                self.middleColumnBlocks.append(evasiveBlock)

def getSneakAttackString(level):
    d6count = c.gf.getNumberFromRange(level,[2,4,6,8,10,12,14,18,20])
    return str(d6count)+"d6"