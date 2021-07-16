document.addEventListener('DOMContentLoaded', function() {

	console.log('loaded')  
	document.querySelector('#addButton').addEventListener('click', addName);


});


function addName(){
	const name_list = document.querySelector('#name_list')
	// name_list.innerHTML += 
	// var input = `<div class="input-group mb-3">
	// <input type="text" class="form-control" placeholder="Enter member" aria-label="Enter member" aria-describedby="basic-addon2">
	// <div class="input-group-append">
	// <button class="btn btn-outline-secondary" type="button" onclick="return this.parentNode.parentNode.remove()">Remove</button>
	// </div></div>`
	var input_div = document.createElement("DIV")
	input_div.setAttribute('class', "input-group mb-3")

	var input = document.createElement('INPUT')
	input.setAttribute('type', "text")
	input.setAttribute('name', "input")
	input.setAttribute('class', 'form-control names')
	input.setAttribute('placeholder', 'Enter member')
	input.setAttribute('aria-label', 'Enter member')
	input.setAttribute('aria-describedby', 'basic-addon2')

	input_div.appendChild(input)

	var remove_div = document.createElement("DIV")
	remove_div.setAttribute('class','input-group-append')

	var remove = document.createElement('BUTTON')
	remove.setAttribute('class', 'btn btn-outline-secondary')
	remove.setAttribute('type', 'button')
	remove.setAttribute('onclick', 'return this.parentNode.parentNode.remove()')
	remove.innerHTML = 'Remove'

	remove_div.appendChild(remove)
	input_div.appendChild(remove_div)



	name_list.appendChild(input_div)
}




