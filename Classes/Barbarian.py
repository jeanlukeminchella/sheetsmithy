import Class as c
import featFunctions as feats

defaultRageTexts = ["• You take half physical damage.","• You may enter Rage as a Bonus Action.","• You have advantage on Athletics checks and Strength saving throws.","• You may add <strong>2</strong> to all Strength-based damage.","• Rages last for a maximum of 10 mins."]

class Barbarian(c.Sheet):
    def __init__(self, inp):
        
        rageTexts = defaultRageTexts[:]
        
        self.hitDie = 12
        self.saveProficiencies = [0,2]
        self.defaultMod = 0
        self.proficientWithShields = True
        
        self.loadScoresAndMods([15,14,13,10,10,10],inp)
        self.attributePriorityList = [0,2,1,4,3,0]
        self.preferredBackgrounds = ["Soldier","Farmer"]

        super().__init__(inp)
        

        self.gp+=75
        self.masteries+=2

        if self.wearingShield:
            c.item.buyItem(self,"Longsword")
        else:
            c.item.buyItem(self,"Maul")
            
        self.wishlist.append("Javelin")
        
        self.proficientWithShields = True
        self.lightArmorProficiency = True
        self.mediumArmorProficiency = True
        level = self.level
        
        self.addHighlightedEntry("Shove")
        self.addHighlightedEntry("Grapple")
        
        rageTitle = "RAGE"
        self.longRestEntries.append("Regain all your uses of <strong>RAGE</strong>")
        self.shortRestEntries.append("Regain one use of <strong>RAGE</strong>")
        self.bonusActionEntries.append(["Enter RAGE. ","See RAGE for the full effects."+" O"*getRageCount(level),""])
        self.bonusActionEntries.append(["Maintain RAGE. ","","Not required if you have attacked or caused a saving throw this turn."])
        
        subclassChoice = None
        
        if level>1:
            #get reckless
            recklessEntry = {"id":"reckless"}
            self.actionEntries.insert(0,recklessEntry)
            self.highlightedBlockIndex+=1
            # danger sense
            self.saveNotes.append([1," (advantage)"])
            self.showDodge = False
            self.actionEntries.append({"id":"Barbarian Dodge"})
                    
        if level>2:
            
            chosen=False
            
                
                
            if self.subclass  == "wildMagic" :
                self.actionEntries.append({"id":"senseMagicItem"})
                self.classAsString = "Barbarian (Wild Magic)"
                rageTexts.append("• When you enter rage, roll a d8 to unleash a magical effect. <em>(Wild Magic - see TCoE for effects)</em>")
                if level>5:
                    bolsterTitle = "<strong>Bolster.</strong> Add a d3 to target's ability checks and attack for 10 minutes, or have them regain a level d3 spell slot. O"+" O"*(self.profBonus-1)
                    self.actionEntries.append(bolsterTitle)

                wildMagicEntries = []

                prefix = ""
                for i in range(1,9):
                    wildMagicEntries.append({"id":prefix+str(i),"modifierIndex":2})
                    
                wildMagicEntries.append("<em>* You may repeat this with another Bonus Action during Rage.</em>")

                
                
                wildMagicBlock = c.e.Block(wildMagicEntries,"WILD MAGIC EFFECTS")
                self.rightColumnBlocks.append(wildMagicBlock)
            elif self.subclass  == "berserker":
                self.classAsString = "Barbarian (Berserker)"
                rageTexts.append("• Once per turn when hitting an enemy with a Strength-based attack, you can <strong>boost the damage roll by 2d6</strong>.")
                
                if level>5:
                    rageTexts.append("• You cannot be Charmed or Frightened while in a rage.")

                
            elif self.subclass  == "wildHeart" or not chosen:
                self.subclass = "wildHeart"
                chosen=True
                rageTexts.append("• Choose one effect from the <strong>Wild Rage Effects</strong>.")
                self.classAsString = "Barbarian (Wild Heart)"
                
                totems = []
                totems.append({"id":"bearWildHeart"})
                totems.append({"id":"wolfWildHeart"})
                totems.append({"id":"eagleWildHeart"})
                
                totemBlock = c.e.Block(totems,"WILD RAGE EFFECTS")
                self.rightColumnBlocks.append(totemBlock)
                
                if level>5:
                    self.rightColumnBlocks.append(c.e.Block([{"id":"wildHeartAspects"}],"WILD HEART ASPECT"))
                    
                    
        
        if level>4:
            extraAttackEntry = {"id":"extraAttackHighlighted"}
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            self.speed+=10
        
        
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,7,10,11,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,7,10,11,17]))
        # Animal Handling, Athletics, Intimidation, Nature, Perception, and Survival.
        
        #get the rage in there
        #get the entries first
        rageEntries = []
        for t in rageTexts:
            rageEntries.append(c.e.Entry(t))
        rageBlock = c.e.Block(rageEntries,rageTitle)
        #maybe dont put it at the bottom?
        self.rightColumnBlocks.insert(0,rageBlock)
        
        
        
        
        
        self.baseACOptions.append(10+self.modifiers[1]+self.modifiers[2])
        
def getRageCount(level):
    return c.gf.getNumberFromRange(level,[0,2,5,11,16])
    