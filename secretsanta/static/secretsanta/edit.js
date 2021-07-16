function add(){

	// add new pill with a unique class name like newpill
	console.log('ADD!')
	var pill = document.createElement('SPAN')

	var name = document.getElementById("add_name").value

	pill.setAttribute('class',"badge badge-pill badge-danger new-mem") 
	pill.innerHTML = name
	pill.setAttribute('style', 'padding: 6px; margin-left: 5px;')
	pill.setAttribute('name','mem')
	// pill.style.display = "inline-block"
	// pill.style.padding = "6px"
	// pill.style.marginLeft = "5px"

	var button = document.createElement('BUTTON')
	button.class = "astext"
	button.style.background = "none"
	button.style.border = "none"
	button.style.margin = "0"
	button.style.marginLeft = "5px"
	button.style.padding = "0"
	button.style.cursor = "pointer"
	button.style.color = "white"
	button.style.fontWeight = "bold"
	button.addEventListener("click", ()=>{
		return button.parentNode.style.display = 'none'
	});

	button.innerHTML = "&times"
	
	pill.appendChild(button)


	var div = document.getElementById("participants")
	div.appendChild(pill)

	document.getElementById("add_name").value = ""

	var new_pill = document.createElement("INPUT")
	new_pill.setAttribute('name','mem')
	new_pill.value = name
	new_pill.style.display = "none"

	var form = document.getElementById("edit_form")
	form.appendChild(new_pill)
}


function remove_pill(el){
	el.parentNode.style.display = 'none'
	// el.setAttribute('name','not_mem')
	el.children[0].name = 'non-mem'
	console.log(el.children[0].type)
	return false
}


function show(){


	// get all the values of the different components
	var title = document.querySelector("#group_title");
	var exchange_date = document.querySelector("#exchangeDate")
	var note = document.querySelector("#note")
	var budget = document.querySelector("#budget")


	console.log(title.getAttribute('value'))
	console.log(exchange_date.getAttribute('value'))
	console.log(note.getAttribute('value'))
	console.log(budget.getAttribute('value'))

	// delete all the new pills 

	var edit_title = document.querySelector("#edit-group-name");
	var edit_exchange_date = document.querySelector("#edit-exchange-date")
	var edit_note = document.querySelector("#edit-note")
	var edit_budget = document.querySelector("#edit-budget")


	edit_title.value = title.getAttribute('value')
	edit_exchange_date.value = exchange_date.getAttribute('value')
	edit_note.value = note.getAttribute('value')
	edit_budget.value = budget.getAttribute('value')



	var pills = document.querySelectorAll(".mem-edit");
	for (var i = 0; i < pills.length; i++) {
			pills[i].style.display = 'initial'
			pills[i].style.marginLeft = '5px'
			console.log('edit!!!')
			
	}

	var inputs = document.querySelectorAll(".memb");
	for (var i = 0; i < inputs.length; i ++){
		inputs[i].name = "mem"
	}

	var new_mem = document.querySelectorAll(".new-mem");
	for (var i = 0; i < new_mem.length; i++) {
			new_mem[i].remove()
			
	}
	return false
 
}


