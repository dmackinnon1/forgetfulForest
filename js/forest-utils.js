'use strict'
// url parsing - simplified (no encoded paramss)
function getQueryParameter(url, key){
    let regex = new RegExp("[?&]" + key + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url); //an array with 3 elements, last is param value
    if (results == null){
    	return null;
    } else {
    	if (results.length < 3) {
    		return null;
    	}
    	return results[2];	
    }
}


function removeElement(array, e) {
	let newArray = [];
	let x;
	for (x in array) {
		if (e !== array[x]) {
			newArray.push(array[x]);
		}
	}
	return newArray;
}

/**
* Randomization Utilities
*/

function randomInt(lessThan){
	return Math.floor(Math.random()*lessThan);
};

/**
* returns a pseudo-random integer in the range 
* [greaterThan, lessThan]
*
*/
function randomRange(greaterThan, lessThan){
	let shifted = randomInt(lessThan - greaterThan + 1);
	return lessThan - shifted; 
};

function randomElement(array) {
	let res =randomRange(0, array.length-1);
	return array[res];
};
