
import Class as c
import globalFunctions as gf


class Warlock(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [4,5]
        self.defaultMod = 5
        
        self.loadScoresAndMods([10,13,14,10,10,15],inp)


        strengthOverDex = False
        if self.scores[0]>self.scores[1]:
            self.attributePriorityList = [5,2,0,1,4,3]
            strengthOverDex = True
        else:
            self.attributePriorityList = [5,2,1,0,4,3]
        
        if strengthOverDex:
            self.preferredBackgrounds = ["Merchant","Charlatan","Noble"]
        else:
            self.preferredBackgrounds = ["Wayfarer","Merchant","Charlatan"]
            

        super().__init__(inp)
        
        
        
        c.item.buyItem(self,"Wand")
        
        self.gp+=100
        self.spellcasting = True
        self.lightArmorProficiency = True
        
        eldritchBlast = {"id":"Eldritch Blast"}
        self.highlightedEntries.append(eldritchBlast)
        if self.level>4:
            eldritchBlast["note"]="x2"
        self.highlightedEntries.append({"id":"Mind Sliver"})

        command = {"id":"Command"}
        bane = {"id":"Bane"}
        invisibility = {"id":"Invisibility"}
        

        # upcasting all the spells
        if self.level >4:
            bane["preSaveNormalText"]="Up to five targets must subtract a d4 from attacks and saving throws. CHAR"
            command["preSaveNormalText"]="One word command obeyed by three targets. WIS"
            invisibility["preSaveNormalText"]="Two creatures you touch have the Invisible condition until the spell ends. The spell ends early immediately after the target makes an attack roll, deals damage, or casts a spell."
        elif self.level>2:
            bane["preSaveNormalText"]="Up to four targets must subtract a d4 from attacks and saving throws. CHAR"
            command["preSaveNormalText"]="One word command obeyed by two targets. WIS"

        if self.level in [1,2]:
            self.spellPriorityList = [command,bane]
        elif self.level in [3,4]:
            self.spellPriorityList = [command,bane,invisibility]
        elif self.level in [5,6]:
            self.spellPriorityList = [command,bane,invisibility]
        
        self.costDic= {
                "1":"Spell",
                "2":"Spell",
                "3":"Spell"
            }
        
        resourceDictionary = {
            1:[["Spell",1]],
            2:[["Spell",2]],
            3:[["Spell",2]],
            4:[["Spell",2]],
            5:[["Spell",2]],
            6:[["Spell",2]]

        }
        
        if self.level <3:
            self.costDic= {
                "1":"Spell"
            }
        
        self.spellsKnown = self.level+1
        self.spellSlotResourceTuples=resourceDictionary[self.level]
        
        self.showReady=False
        self.shortRestEntries.append("You regain all your spell slots.")

        if self.level>1:
            pass
            
        if self.level>2:
            subclassChosen = False

            
            if self.subclass == "fiend" or not subclassChosen:
                
                self.subclass = "fiend"
                self.classAsString="Warlock (Pact of the Fiend)"
                subclassChosen = True

                self.actionEntries.append(command)
                if self.level>4:
                    self.actionEntries.append({"id":"Scorching Ray","note":"x4"})
                    self.actionEntries.append({"id":"Burning Hands","preSaveNormalText":"Unleash a 15ft cone of 5d6 fire damage. "})
                else:
                    self.actionEntries.append({"id":"Burning Hands","preSaveNormalText":"Unleash a 15ft cone of 4d6 fire damage. "})
                    self.actionEntries.append({"id":"Scorching Ray"})

                if self.level>5:
                    pass    
                if self.level>4:
                    self.actionEntries.append({"id":"Fireball"})


        # Arcana, Deception, History, Intimidation, Investigation, Nature, or Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([2,4,5,7,8,10,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([2,4,5,7,8,10,14]))
        
        

        # add a weapon for the opp attacks.
        
        if self.martialProficiency:
            if strengthOverDex:
                self.wishlist.append("Longsword")
            else:
                self.wishlist.append("Rapier")
        else:
            if strengthOverDex:
                self.wishlist.append("Mace")
            else:
                self.wishlist.append("Dagger")
        

         
