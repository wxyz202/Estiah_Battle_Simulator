var runeOptions = ["Null", "Axe", "Sword", "Mace", "Twinblades", "Spear", "Fist", "Earth", "Shadow", "Holy", "Lightning", "Frost", "Fire", "Spirit", "Armor", "Ward", "Willpower", "Summon", "Buff", "Debuff", "Tech"];
var targetOptions = ["Self", "Enimy", "All_Enimies", "All_Allies", "All"];
var termOptions = [
	"==Damage==", "Melee", "MeleeDrain", "Magic", "MagicDrain", "ShiftingDamage", "Spirit",
	"==Defense==", "Armor", "Ward", "ShiftingDefense", "Willpower",
	"==Projection==", "Projection",
	"==Life==", "Heal", "LifeLose",
	"==Defense Destroy==", "ArmorDestroy", "WardDestroy", "WillpowerDestroy",
	"==Extra Action==", "ExtraAction",
	"==Focus,Protect==", "FocusProtect",
	"==Vanish==", "Vanish",
	"==Stun==", "Stun",
	"==Booster==", "NextMelee", "NextMagic", "NextSpirit", "OngoingMelee", "OngoingMagic", "OngoingSpirit",
	"==State Reset==", "Cleanse", "Purge", "Normalize",
	"==Attach==", "Attach"
];

function addOptionsToSelect(selectObj, options) {
	for (var i = 0; i < options.length; i++) {
		var newOption = document.createElement("option");
		newOption.text = options[i];
		selectObj.appendChild(newOption);
	}
}

function getIndexFromOptionText(selectObj, optionText) {
	for (var i = 0; i < selectObj.options.length; i++) {
		if (selectObj.options[i].text == optionText) {
			return i;
		}
	}
	return 0;
}

function getOptionTextFromSelected(selectObj) {
	return selectObj.options[selectObj.selectedIndex].text;
}

function appendInputText(term, textId, defaultValue) {
	var termId = term.id;
	term.appendChild(document.createTextNode(" " + textId + ": "));
	var inputObj = document.createElement("input");
	inputObj.type = "text";
	inputObj.id = termId + "_" + textId;
	inputObj.style.width="40px"
	inputObj.value = defaultValue;
	term.appendChild(inputObj);
}

function appendInputBoolean(term, booleanId) {
	var termId = term.id;
	term.appendChild(document.createTextNode(" " + booleanId + ": "));
	var inputObj = document.createElement("select");
	inputObj.id = termId + "_" + booleanId;
	addOptionsToSelect(inputObj, ["False", "True"]);
	inputObj.selectedIndex = getIndexFromOptionText(inputObj, "False")
	term.appendChild(inputObj);
}

function appendInputSelect(term, selectId, options, defaulfValue) {
	var termId = term.id;
	term.appendChild(document.createTextNode(" " + selectId + ": "));
	var inputObj = document.createElement("select");
	inputObj.id = termId + "_" + selectId;
	addOptionsToSelect(inputObj, options);
	inputObj.selectedIndex = getIndexFromOptionText(inputObj, defaulfValue)
	term.appendChild(inputObj);
}

function appendTarget(term, defaultTarget) {
	var termId = term.id;
	appendInputSelect(term, "target", targetOptions, defaultTarget);
}

function loadParam(selectObj) {
	var term = selectObj.parentNode;
	var termId = term.id
	while (term.lastChild != selectObj) {
		term.removeChild(term.lastChild);
	}
	var i = selectObj.selectedIndex;
	while (!(selectObj.options[i].text.match("==.*=="))) {
		i--;
	}
	if (i == selectObj.selectedIndex) {
		return;
	}
	var text = selectObj.options[i].text;
	if (text == "==Damage==") {
		appendInputText(term, "damage", "");
		appendInputText(term, "penetrating", 0);
		appendTarget(term, "Enimy");
	}
	else if (text == "==Defense==") {
		appendInputText(term, "defense", "");
		appendInputBoolean(term, "is_cumul");
		appendTarget(term, "Self");
	}
	else if (text == "==Projection==") {
		appendInputText(term, "max_damage", "");
		appendInputSelect(term, "damage_type", ["Melee", "Magic"], "");
		appendInputSelect(term, "defense_type", ["Armor", "Ward"], "");
		appendTarget(term, "Enimy");
	}
	else if (text == "==Life==") {
		appendInputText(term, "life", "");
		appendTarget(term, "Self");
	}
	else if (text == "==Defense Destroy==") {
		appendInputText(term, "defense", "");
		appendTarget(term, "Enimy");
	}
	else if (text == "==Extra Action==") {
		appendInputText(term, "turn", 1);
		appendTarget(term, "Self");
	}
	else if (text == "==Focus,Protect==") {
		appendInputText(term, "turn", "");
		appendInputBoolean(term, "is_cumul");
		appendTarget(term, "Enimy");
	}
	else if (text == "==Vanish==") {
		appendTarget(term, "Self");
	}
	else if (text == "==Stun==") {
		appendInputText(term, "turn", 1);
		appendTarget(term, "Self");
	}
	else if (text == "==Booster==") {
		appendInputText(term, "boost", "");
		appendTarget(term, "Self");
	}
	else if (text == "==State Reset==") {
		appendTarget(term, "Self");
	}
	else if (text == "==Attach==") {
		appendInputSelect(term, "attachment", ["Aura", "Bane", "Curse", "Summon"], "");
		appendInputText(term, "turn", "");
		appendInputSelect(term, "long_time_type", ["LongTimeAfter", "LongTimeDuring"], "LongTimeDuring");
		appendTarget(term);
	}
}

function changeTerm(event) {
	var selectObj = event.target;
	loadParam(selectObj);
}

var termCount = 0;

function addTerm() {
	var newTerm = document.createElement("div");
	document.getElementById("charminput").appendChild(newTerm);
	var termId = "term" + termCount;
	termCount++;
	newTerm.id =  termId;
	var newSelect = document.createElement("select");
	newTerm.appendChild(newSelect);
	newSelect.id = termId + "_termType";
	addOptionsToSelect(newSelect, termOptions);
	for (var i = 0; i < newSelect.options.length; i++) {
		if (newSelect.options[i].text.match("==.*==")) {
			newSelect.options[i].style.fontStyle = "italic";
			newSelect.options[i].disabled = true;
		}
	}
	newSelect.selectedIndex = getIndexFromOptionText(newSelect, "Melee");
	newSelect.onchange = changeTerm;
	loadParam(newSelect);
}

function delTerm() {
	if (termCount > 0) {
		termCount--;
		var termId = "term" + termCount;
		document.getElementById("charminput").removeChild(document.getElementById(termId));
	}
}

function resetTerms() {
	for (var i = termCount-1; i >=0 ; i--) {
		var term = document.getElementById("term" + i);
		term.parentNode.removeChild(term);
	}
	termCount = 0;
}

function getInputText(term, textId) {
	var termId = term.id;
	var inputObj = document.getElementById(termId + "_" + textId);
	return inputObj.value;
}

function getInputSelect(term, selectId) {
	var termId = term.id;
	var inputObj = document.getElementById(termId + "_" + selectId);
	return getOptionTextFromSelected(inputObj);
}	

function damageTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var damage = getInputText(term, "damage");
	var penetrating = getInputText(term, "penetrating");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + damage + ", " + penetrating + "), TargetType." + target + ")])"
}

function defenseTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var defense = getInputText(term, "defense");
	var is_cumul = getInputSelect(term, "is_cumul");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + defense + ", " + is_cumul + "), TargetType." + target + ")])"
}

function projectionTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var max_damage = getInputText(term, "max_damage");
	var damage_type = getInputSelect(term, "damage_type");
	var defense_type = getInputSelect(term, "defense_type");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + max_damage + ", EffectType." + damage_type + ", EffectType." + defense_type + "), TargetType." + target + ")])"
}

function lifeTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var life = getInputText(term, "life");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + life + "), TargetType." + target + ")])"
}

function defenseDestroyTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var defense = getInputText(term, "defense");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + defense + "), TargetType." + target + ")])"
}

function extraActionTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var turn = getInputText(term, "turn");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + turn + "), TargetType." + target + ")])"
}

function focusProtectTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var turn = getInputText(term, "turn");
	var is_cumul = getInputSelect(term, "is_cumul");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + turn + ", " + is_cumul + "), TargetType." + target + ")])"
}

function vanishTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(), TargetType." + target + ")])"
}

function stunTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var turn = getInputText(term, "turn");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + turn + "), TargetType." + target + ")])"
}

function boosterTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var boost = getInputText(term, "boost");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(" + boost + "), TargetType." + target + ")])"
}

function stateResetTermToCode(term) {
	var termType = getInputSelect(term, "termType");
	var target = getInputSelect(term, "target");
	return "EffectTerm([(" + termType + "(), TargetType." + target + ")])"
}

function termToCode(term) {
	var termId = term.id;
	var selectObj = document.getElementById(termId + "_termType");
	var i = selectObj.selectedIndex;
	while (!(selectObj.options[i].text.match("==.*=="))) {
		i--;
	}
	if (i == selectObj.selectedIndex) {
		return;
	}
	var text = selectObj.options[i].text;
	if (text == "==Damage==") {
		return damageTermToCode(term);
	}
	else if (text == "==Defense==") {
		return defenseTermToCode(term);
	}
	else if (text == "==Projection==") {
		return projectionTermToCode(term);
	}
	else if (text == "==Life==") {
		return lifeTermToCode(term);
	}
	else if (text == "==Defense Destroy==") {
		return defenseDestroyTermToCode(term);
	}
	else if (text == "==Extra Action==") {
		return extraActionTermToCode(term);
	}
	else if (text == "==Focus,Protect==") {
		return focusProtectTermToCode(term);
	}
	else if (text == "==Vanish==") {
		return vanishTermToCode(term);
	}
	else if (text == "==Stun==") {
		return stunTermToCode(term);
	}
	else if (text == "==Booster==") {
		return boosterTermToCode(term);
	}
	else if (text == "==State Reset==") {
		return stateResetTermToCode(term);
	}
}

function createCharm() {
	var id = document.getElementById("charmId").value;
	var name = document.getElementById("charmName").value;
	var rune1 = getOptionTextFromSelected(document.getElementById("rune1"));
	var rune2 = getOptionTextFromSelected(document.getElementById("rune2"));
	var text = "\tcharm = Charm(\n";
	text = text + "\t\tid = \"" + id + "\",\n";
	text = text + "\t\tname = \"" + name + "\",\n";
	text = text + "\t\trune1 = RuneType." + rune1 + ",\n";
	text = text + "\t\trune2 = RuneType." + rune2 + ",\n";
	text = text + "\t\tcharm_terms = [\n";
	for (var i = 0; i < termCount; i++) {
		text = text + "\t\t\t" + termToCode(document.getElementById("term" + i));
		if (i+1 != termCount) {
			text = text + ",";
		}
		text = text + "\n";
	}
	text = text + "\t\t]\n";
	text = text + "\t)";
	var outputArea = document.getElementById("charmoutput");
	outputArea.value = text;
}

function myDebug() {
	var term = document.getElementById("term0");
	var selectedIndex = term.firstChild.selectedIndex;
	alert(term.firstChild.options[selectedIndex].text);
}
