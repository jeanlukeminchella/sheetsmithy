
function showLanguages(){
    console.log("SHOWING LANGUAGES");
    showIDList(["langs","hideLangsButton"]);
    hideIDList(["showLangsButton"]);

};
function hideLanguages(){
    hideIDList(["langs","hideLangsButton"]);
    showIDList(["showLangsButton"]);

};


function showInventory(){
    showIDList(["hideInventoryButton", "inventory", "shoppingList", "gearList"]);
    hideIDList(["showInventoryButton"]);

};
function hideInventory(){
    hideIDList(["hideInventoryButton", "inventory", "shoppingList", "gearList"]);
    showIDList(["showInventoryButton"]);

};

function showID(id){
    document.getElementById(id).style.display='block';
    document.getElementById(id).disabled=false;
}; 

function showIDList(l){
    l.forEach(showID)
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
    const classChoiceIDs = ["barbarianSubclass","clericSubclass","fightStyle","l4-feat","l4-feat-label","l6-feat","monkSubclass","fighterSubclass","rogueSubclass","paladinSubclass","rangerSubclass","divineOrder","primalOrder"];
    classChoiceIDs.forEach(hideID);
    
    console.log("loading class choices");
    /* multi dimensional array, showing what to display at what level. */
    let allClassChoices = {
        "Cleric":[["divineOrder"],[],["clericSubclass"],["l4-feat","l4-feat-label"]],
        "Druid":[["primalOrder"],[],[],["l4-feat","l4-feat-label"]],
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
