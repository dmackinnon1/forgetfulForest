"use strict"
/*
 * Forest of forgetfulness puzzle display
 */

// The forest object tracks the status of the selected puzzle
let forest = {}; 
forest.puzzles = []; 
forest.activeSet = []; 
forest.selected = null; //the puzzle selected for the user 
// UI must initialize display elements
let display = {};
display.versionDescription = null;
display.puzzleTitle = null;
display.puzzleIntro = null;
display.puzzleDescription = null;
display.explanationDisplay = null;
display.disabled = false;
display.solutionDisplay = null;
display.dayDisplay = null;

// the initial page layout, populating the display elements
function formatPuzzle(pc) {
	let pi = display.puzzleIntro;
	let pd = display.puzzleDescription;
	let pt = display.puzzleTitle;
	let dd = display.dayDisplay;
	dd.innerHTML = pc.dayDisplay();
	pt.innerHTML = pc.puzzleTitle()
	pi.innerHTML = pc.puzzleIntro();
	let solD = display.solutionDisplay;
	solD.innerHTML ="";
	let ed = display.explanationDisplay;
	ed.innerHTML = "";
}

// called from UI to reset the puzzle
function puzzleReset(url = null) {	
	let id = null;
	if (url != null){
		id = getQueryParameter(url, 'id');
	}
	if  (forest.activeSet.length == 0) {
	 forest.activeSet = forest.puzzles;
	}
	let p = null;
	if (id != null) {
		p = getPuzzleWithId(id);
 	}
 	if (p == null) {
		p = randomElement(forest.activeSet);	
 	}
 	forest.selected = new PuzzleController(p);
 	forest.activeSet = removeElement(forest.activeSet,p);
	formatPuzzle(forest.selected);	
  	forest.answered = false;
	display.disabled = false;
	updateAllButtons();
	console.log(forest.selected)
}

function getPuzzleWithId(id) {
	let x = null;
	for (x in forest.activeSet){
		let p = forest.activeSet[x];
		 if (p.id == id){
		 	return p;
		 }
	}
	console.log('No puzzle with provided id was found in active set: ' + id);
	return null;
}

/*
* Renders the selected puzzle and tracks puzzle data.
*/
class PuzzleController {
	constructor(p){
		this.puzzle = p;
		this.day = null;
	}
	
	puzzleIntro() {
		let txt = "<ul><li>" + this.puzzle.lion + "</li>";
		txt +="<li>" + this.puzzle.unicorn + "</li>";
		txt += "</ul>";
		return txt;
	}

	dayDisplay(){
		let days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
		let text = "<table>"
		for (let d in days){
			let dc = new DayController(days[d]);
			text += "<tr>"
			text += dc.display();
			text += "</tr>"
		}
		text += "</table>"
		return text;
	}

	explanationDisplay(){
		let txt = "<br><p> Here is one way to think about it:<br>"
		txt += this.puzzle.explanation;
		txt += "</br>";
		return txt;
	}

	puzzleTitle(){
		return "Puzzle " + this.puzzle.id
	}

}

/*
* Renders UI element for day selectors, updates the PuzzleController
* using the associated selectDay() function.
*/
class DayController {
	constructor(name) {
		this.name = name;
	}

	display() {
		let txt = "glyphicon glyphicon-unchecked";
		let btn = "<td>"+ this.name+"</td>"; 
		btn +=  "<td><button type='button' id='day_"+ this.name + "' class='day-btn btn btn-secondary', onclick='selectDay(event)'>";
		btn += "<span class='glypicon " + txt + " lrg-font'></span>"
		btn += "</button></td>";
		return btn;		
	}	
}
//used with DayController
function selectDay(event) {
	if (display.disabled) return;
	let id = event.currentTarget.id;
	let day = id.substring(id.indexOf('_')+1, id.length);
	forest.selected.day = day;
	updateAllButtons(day)
};

//used with DayController and puzzleReset
function updateAllButtons(day){
	$(".day-btn").removeClass("btn-primary");	
	$(".day-btn").addClass("btn-secondary");	
	$(".day-btn").html("<span class='glypicon glyphicon glyphicon-unchecked lrg-font'></span>");

	$("#day_" + day).removeClass("btn-secondary");
	$("#day_" + day).addClass("btn-primary");
	$("#day_" + day).html("<span class='glypicon glyphicon glyphicon-ok lrg-font'></span>");	
};

//called from UI to solve the puzzle
function solvePuzzle(){
	display.disabled = true;
	let solD = display.solutionDisplay;
	let txt = ""
	if (forest.selected.day == forest.selected.puzzle.solution){
		txt = "You said today is " + forest.selected.day + ".";
		txt += " <em> You were right. </em>";
	} else if (forest.selected.day == null){
		txt = "You did not pick a day. It turns out that today is ";
		txt += forest.selected.puzzle.solution + ".";
	} else {
		txt = "You said today is " + forest.selected.day + ".";
		txt += "<em> You were wrong</em>, it is actually " + forest.selected.puzzle.solution + ".";
	}
	solD.innerHTML = txt;
}; 

//called from UI to explain the puzzle
function explainPuzzle(){
	let ed = display.explanationDisplay;
	ed.innerHTML = forest.selected.explanationDisplay();
};

