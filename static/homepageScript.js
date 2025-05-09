
function showLanguages(){
    showIDList(["langs","hideLangsButton","languages"]);
    hideIDList(["showLangsButton"]);

};
function hideLanguages(){
    hideIDList(["langs","hideLangsButton","languages"]);
    showIDList(["showLangsButton"]);

};

function hideHelp(){
    showIDList(["showHelpButton"]);
    hideIDList(["help","hideHelpButton"]);
};

function showHelp(){
    hideIDList(["showHelpButton"]);
    showIDList(["help","hideHelpButton"]);
};

function showInventory(){
    showIDList(["hideInventoryButton", "inventory", "shoppingList", "gearList","bonusGold","bonusSilver","bonusCopper","goldPieceDecimal"]);
    hideIDList(["showInventoryButton"]);

};
function hideInventory(){
    hideIDList(["hideInventoryButton", "inventory", "shoppingList", "gearList","bonusGold","bonusSilver","bonusCopper","goldPieceDecimal"]);
    showIDList(["showInventoryButton"]);

};

function loadCoreOptions(){
    showIDList(["name","background","classAsString","race"]);
    const checkBoxes = ["showScores","hideShortRest","hideLongRest","hidePhysicalDamageTypes","shoppingList","gearList","bonusGold","bonusSilver","bonusCopper","goldPieceDecimal"]
    for (let i = 0; i < checkBoxes.length; i++) {
        
        document.getElementById(checkBoxes[i]).disabled=false 
        
    };
};

function showID(id){
    document.getElementById(id).style.display='block';
    document.getElementById(id).disabled=false;
}; 

function showIDList(l){
    l.forEach(showID)
}; 

function hideID(id){
    document.getElementById(id).style.display='none';
    document.getElementById(id).disabled=true;
};
function hideIDList(l){
    l.forEach(hideID)
}; 

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
};

function setSeed(){
    document.getElementById("seed").value=getRndInteger(0,10000);
};

function wrapUp(){
    ids = ["name","classAsString","race","background","shoppingList","gearList"];
    ids.forEach(disableIDIfBlank);
    console.log("wrapping up");

    
    let cp = document.getElementById("bonusCopper").value/100;
    let sp = document.getElementById("bonusSilver").value/10;
    let gp = document.getElementById("bonusGold").value;    
    console.log("gp, sp, cp is ",gp, sp,cp);
    gp = (gp*1)+(cp*1) + (sp*1);
    gp.toFixed(2);
    document.getElementById("goldPieceDecimal").value = gp.toFixed(2);
    console.log("document.getElementById('goldPieceDecimal').value is ",document.getElementById("goldPieceDecimal").value);

};



function disableIDIfBlank(id){
    if (document.getElementById(id).value==""){
        document.getElementById(id).disabled=true
    }
};

const abilityIDs = ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"];
function showAbilityScores(){
    showIDList(abilityIDs);
    showIDList(['abilityScores','hideScoresButton']); 
    hideIDList(['showScoresButton']);

};
function hideAbilityScores(){
    hideIDList(abilityIDs);
    hideIDList(['abilityScores','hideScoresButton']); 
    showIDList(['showScoresButton']);
    
};
function loadSpeciesOptions() {
    
    const racialChoicesIds = ["goliathSubrace","humanFeatChoice","tieflingSubrace","size","gnomeSubrace","elfSubrace"]
    racialChoicesIds.forEach(hideID);
    
    let racialChoices = {
        "goliath":["goliathSubrace"],
        "human":["humanFeatChoice"],
        "aasimar":["size"],
        "elf":["elfSubrace"],
        "gnome":["gnomeSubrace"],
        "tiefling":["size","tieflingSubrace"],
        "":[]
    };
    const race = document.getElementById("race").value;
    racialChoices[race].forEach(showID);

};
function loadClassChoices() {
    const classChoiceIDs = ["barbarianSubclass","clericSubclass","druidSubclass","fightStyle","l4-feat","l4-feat-label","l6-feat","monkSubclass","fighterSubclass","rogueSubclass","paladinSubclass","rangerSubclass","divineOrder","primalOrder"];
    classChoiceIDs.forEach(hideID);
    
    /* multi dimensional array, showing what to display at what level. */
    let allClassChoices = {
        "Cleric":[["divineOrder"],[],["clericSubclass"],["l4-feat","l4-feat-label"]],
        "Druid":[["primalOrder"],[],["druidSubclass"],["l4-feat","l4-feat-label"]],
        "Barbarian":[[],[],["barbarianSubclass"],["l4-feat","l4-feat-label"]],
        "Fighter":[["fightStyle"],[],["fighterSubclass"],["l4-feat","l4-feat-label"],[],["l6-feat"]],
        "Rogue":[[],[],["rogueSubclass"],["l4-feat","l4-feat-label"]],
        "Ranger":[[],["fightStyle"],["rangerSubclass"],["l4-feat","l4-feat-label"]],
        "Paladin":[[],["fightStyle"],["paladinSubclass"],["l4-feat","l4-feat-label"]],
        "Monk":[[],[],["monkSubclass"],["l4-feat","l4-feat-label"]],
        "Warlock":[],
        "":[]
    };
    const level = document.getElementById("level").value;
    const cls = document.getElementById("classAsString").value;
    
    const thisClassChoices = allClassChoices[cls]
    
    thisClassChoices.forEach(considerShowingClassChoices)

    function considerShowingClassChoices(value,index){
        if (index<level){
            

            value.forEach(showID);
            
        }
    }
}
