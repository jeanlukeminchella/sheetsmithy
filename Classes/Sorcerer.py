

import Class as c

class Sorcerer(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 6
        self.saveProficiencies = [2,5]
        self.defaultMod = 5
        
        self.loadScoresAndMods([10,15,13,8,14,12],inp)
        self.attributePriorityList = [5,2,1,4,0,3]
        
        self.preferredBackgrounds = ["Noble","Wayfarer","Merchant","Charlatan"]
        
        super().__init__(inp)

        self.wishlist.append("Wand")

        self.costDic["1sp"]="Sorcery Point"
        self.costDic["2sp"]="2 Sorcery Points"

        self.spellcasting = True

        self.spellPriorityList = ["Shield","Burning Hands","Detect Magic"]
        
        sp = "Sorcery Points"
        resourceDictionary = {
            1:[["Spell",2]],
            2:[["Spell",3],[sp,2]],
            3:[[self.costDic["1"],4],[self.costDic["2"],2],[sp,3]],
            4:[[self.costDic["1"],4],[self.costDic["2"],3],[sp,4]],
            5:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],2],[sp,5]],
            6:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],3],[sp,6]]
        }
        
        if self.level <3:
            self.costDic= {
                "1":"Spell"
            }
        spellKnownEachLevel = [0,2,4,6,7,9,10]
        self.spellsKnown = spellKnownEachLevel[self.level]
        self.spellSlotResourceTuples=resourceDictionary[self.level]
        self.notesForSpellCastingBlock.append(getMetamagicEntry("Careful Spell"))
        self.notesForSpellCastingBlock.append(getMetamagicEntry("Empowered Spell"))
        
        self.addEntry("Mind Sliver")

        self.skillProficiencies.append(self.pickSkillProficiency([2,4,6,7,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([2,4,6,7,13,14]))
        

carefulSpell = {"id":"Careful Spell","cost":"1sp","type":"spell","preSaveNormalText":"When you cast a spell that forces other creatures to make a saving throw, you can protect some of those creatures from the spell's full force. To do so, spend 1 Sorcery Point and choose a number of those creatures up to your Charisma modifier (minimum of one creature). A chosen creature automatically succeeds on its saving throw against the spell, and it takes no damage if it would normally take half damage on a successful save."}
distantSpell = {"id":"Distant Spell","cost":"1sp","type":"spell","preSaveNormalText":"When you cast a spell that has a range of at least 5 feet, you can spend 1 Sorcery Point to double the spell's range. Or when you cast a spell that has a range of Touch, you can spend 1 Sorcery Point to make the spell's range 30 feet."}
empoweredSpell = {"id":"Empowered Spell","cost":"1sp","type":"spell","preSaveNormalText":"When you roll damage for a spell, you can spend 1 Sorcery Point to reroll a number of the damage dice up to your Charisma modifier (minimum of one), and you must use the new rolls. You can use Empowered Spell even if you've already used a different Metamagic option during the casting of the spell."}
extendedSpell = {"id":"Extended Spell","cost":"1sp","type":"spell","preSaveNormalText":"When you cast a spell that has a duration of 1 minute or longer, you can spend 1 Sorcery Point to double its duration to a maximum duration of 24 hours. If the affected spell requires Concentration, you have Advantage on any saving throw you make to maintain that Concentration."}
hightenedSpell = {"id":"Heightened Spell","cost":"2sp","type":"spell","preSaveNormalText":"When you cast a spell that forces a creature to make a saving throw, you can spend 2 Sorcery Points to give one target of the spell Disadvantage on saves against the spell."}
quickenedSpell = {"id":"Quickened Spell","cost":"2sp","type":"spell","preSaveNormalText":"When you cast a spell that has a casting time of an action, you can spend 2 Sorcery Points to change the casting time to a Bonus Action for this casting. You can't modify a spell in this way if you've already cast a level 1+ spell on the current turn, nor can you cast a level 1+ spell on this turn after modifying a spell in this way."}
seekingSpell = {"id":"Seeking Spell","cost":"1sp","type":"spell","preSaveNormalText":"If you make an attack roll for a spell and miss, you can spend 1 Sorcery Point to reroll the d20, and you must use the new roll. You can use Seeking Spell even if you've already used a different Metamagic option during the casting of the spell."}
subtleSpell = {"id":"Subtle Spell","cost":"1sp","type":"spell","preSaveNormalText":"When you cast a spell, you can spend 1 Sorcery Point to cast it without any Verbal, Somatic, or Material components, except Material components that are consumed by the spell or that have a cost specified in the spell."}
transmutedSpell = {"id":"Transmuted Spell","cost":"1sp","type":"spell","preSaveNormalText":"When you cast a spell that deals a type of damage from the following list, you can spend 1 Sorcery Point to change that damage type to one of the other listed types: Acid, Cold, Fire, Lightning, Poison, Thunder."}
twinnedSpell = {"id":"Twinned Spell","cost":"1sp","type":"spell","preSaveNormalText":"When you cast a spell, such as Charm Person, that can be cast with a higher-level spell slot to target an additional creature, you can spend 1 Sorcery Point to increase the spell's effective level by 1."}

metamagicDictionary = {
    "Careful Spell":carefulSpell,
    "Distant Spell":distantSpell,
    "Empowered Spell":empoweredSpell,
    "Extended Spell":extendedSpell,
    "Heightened Spell":hightenedSpell,
    "Quickened Spell":quickenedSpell,
    "Seeking Spell":seekingSpell,
    "Subtle Spell":subtleSpell,
    "Transmuted Spell":transmutedSpell,
    "Twinned Spell":twinnedSpell
}

def getMetamagicEntry(command):
    if command in metamagicDictionary.keys():
        return metamagicDictionary[command]
    
